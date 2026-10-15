"""Resolve HTTP citations with conservative network and size boundaries.

This is a local CLI safety layer, not a sandbox for multi-tenant URL fetching.
Deployment against arbitrary users' URLs still requires network-level egress rules.
"""

from __future__ import annotations

import ipaddress
import json
import socket
from pathlib import Path
from typing import Any, Optional
from urllib.parse import urljoin, urlsplit

import requests

from citeguard.models import ResolveResult

DEFAULT_UA = "CiteGuard/0.2 (+https://github.com/larrylot/citeguard)"
TIMEOUT = 12.0
MAX_HTML_BYTES = 2 * 1024 * 1024
MAX_REDIRECTS = 5


class FixtureStore:
    """Map URLs to deterministic fake responses; never make network requests."""

    def __init__(self, catalog: dict[str, Any], pages_dir: Path):
        self.catalog = catalog
        self.pages_dir = pages_dir.resolve()

    @classmethod
    def load(cls, fixtures_root: Path) -> "FixtureStore":
        with open(fixtures_root / "catalog.json", encoding="utf-8") as f:
            catalog = json.load(f)
        return cls(catalog, fixtures_root / "pages")

    def get(self, url: str) -> Optional[ResolveResult]:
        entry = self.catalog.get(url)
        if entry is None:
            alt = url.rstrip("/") if url.endswith("/") else url + "/"
            entry = self.catalog.get(alt)
        if entry is None:
            return ResolveResult(url=url, ok=False, error="not_in_fixtures", from_fixtures=True)
        raw_status = entry.get("status", 200)
        status = int(raw_status) if raw_status is not None else None
        body = None
        page = entry.get("page")
        if page:
            # Fixture catalogs are data. Do not permit traversal outside pages/.
            path = (self.pages_dir / page).resolve()
            if path.is_relative_to(self.pages_dir) and path.is_file():
                body = path.read_text(encoding="utf-8", errors="replace")
        error = entry.get("error")
        ok = status is not None and 200 <= status < 300 and not error
        return ResolveResult(
            url=url, ok=ok, status=status,
            final_url=entry.get("final_url", url),
            error=error, body=body,
            content_type=entry.get("content_type", "text/html"),
            from_fixtures=True,
        )


def _validate_target(url: str, *, allow_private: bool = False) -> str | None:
    """Reject non-web schemes, URL credentials and non-public DNS resolutions.

    DNS can change between validation and connection. Use egress firewall rules
    before exposing this checker as a network-facing service.
    """
    try:
        parsed = urlsplit(url)
        host, port = parsed.hostname, parsed.port
    except ValueError:
        return "invalid_url"
    if parsed.scheme not in {"http", "https"} or not host:
        return "unsupported_url"
    if parsed.username is not None or parsed.password is not None:
        return "embedded_credentials"
    if allow_private:
        return None
    try:
        addresses = socket.getaddrinfo(
            host, port or (443 if parsed.scheme == "https" else 80),
            type=socket.SOCK_STREAM,
        )
        if not addresses:
            return "dns_no_results"
        ips = {ipaddress.ip_address(item[4][0].split("%", 1)[0]) for item in addresses}
    except (OSError, ValueError):
        return "dns_failure"
    if any(not addr.is_global for addr in ips):
        return "blocked_private_address"
    return None


def resolve_url(
    url: str,
    *,
    session: Optional[requests.Session] = None,
    fixtures: Optional[FixtureStore] = None,
    timeout: float = TIMEOUT,
    allow_private: bool = False,
    max_html_bytes: int = MAX_HTML_BYTES,
) -> ResolveResult:
    """Retrieve up to max_html_bytes of HTML, validating every redirect target."""
    if fixtures is not None:
        return fixtures.get(url)
    if timeout <= 0 or max_html_bytes <= 0:
        raise ValueError("timeout and max_html_bytes must be positive")

    owned = session is None
    sess = session if session is not None else requests.Session()
    # Environment HTTP_PROXY can route validation past our target checks.
    sess.trust_env = False
    headers = {
        "User-Agent": DEFAULT_UA,
        "Accept": "text/html,application/xhtml+xml;q=0.9,*/*;q=0.1",
    }
    current = url
    try:
        for hop in range(MAX_REDIRECTS + 1):
            blocked = _validate_target(current, allow_private=allow_private)
            if blocked is not None:
                return ResolveResult(
                    url=url, ok=False, final_url=current, error=blocked
                )
            try:
                with sess.get(
                    current, headers=headers, timeout=timeout,
                    stream=True, allow_redirects=False,
                ) as response:
                    status = response.status_code
                    if 300 <= status < 400:
                        location = response.headers.get("Location")
                        if not location:
                            return ResolveResult(
                                url=url, ok=False, status=status, final_url=current,
                                error="redirect_missing_location",
                            )
                        if hop == MAX_REDIRECTS:
                            return ResolveResult(
                                url=url, ok=False, status=status, final_url=current,
                                error="too_many_redirects",
                            )
                        current = urljoin(current, location)
                        continue
                    if not 200 <= status < 300:
                        return ResolveResult(
                            url=url, ok=False, status=status, final_url=current,
                            error=f"http_{status}",
                        )

                    ctype = response.headers.get("Content-Type", "")
                    if ctype and "html" not in ctype.lower():
                        return ResolveResult(
                            url=url, ok=True, status=status, final_url=current,
                            content_type=ctype,
                        )
                    size_hint = response.headers.get("Content-Length")
                    if size_hint:
                        try:
                            if int(size_hint) > max_html_bytes:
                                return ResolveResult(
                                    url=url, ok=False, status=status, final_url=current,
                                    content_type=ctype, error="body_too_large",
                                )
                        except ValueError:
                            pass
                    chunks: list[bytes] = []
                    size = 0
                    for chunk in response.iter_content(chunk_size=65536):
                        if not chunk:
                            continue
                        size += len(chunk)
                        if size > max_html_bytes:
                            return ResolveResult(
                                url=url, ok=False, status=status, final_url=current,
                                content_type=ctype, error="body_too_large",
                            )
                        chunks.append(chunk)
                    encoding = response.encoding or "utf-8"
                    body = b"".join(chunks).decode(encoding, errors="replace")
                    return ResolveResult(
                        url=url, ok=True, status=status, final_url=current,
                        content_type=ctype, body=body,
                    )
            except (requests.RequestException, UnicodeError) as exc:
                return ResolveResult(
                    url=url, ok=False, final_url=current,
                    error=f"network:{type(exc).__name__}",
                )
    finally:
        if owned:
            sess.close()
    return ResolveResult(url=url, ok=False, final_url=current, error="too_many_redirects")
