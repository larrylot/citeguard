"""HTTP(S) resolve with HEAD→GET fallback and offline fixtures mode."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Optional
from urllib.parse import urlparse

import requests

from citeguard.models import ResolveResult

DEFAULT_UA = "CiteGuard/0.1 (+https://github.com/larrylot/citeguard; local citation checker)"
TIMEOUT = 12


class FixtureStore:
    """Maps URL → planted status/body for offline CI."""

    def __init__(self, catalog: dict[str, Any], pages_dir: Path):
        self.catalog = catalog
        self.pages_dir = pages_dir

    @classmethod
    def load(cls, fixtures_root: Path) -> "FixtureStore":
        catalog_path = fixtures_root / "catalog.json"
        with open(catalog_path, encoding="utf-8") as f:
            catalog = json.load(f)
        return cls(catalog, fixtures_root / "pages")

    def get(self, url: str) -> Optional[ResolveResult]:
        entry = self.catalog.get(url)
        if entry is None:
            # Also try without trailing slash variance
            alt = url.rstrip("/") if url.endswith("/") else url + "/"
            entry = self.catalog.get(alt)
        if entry is None:
            return ResolveResult(
                url=url,
                ok=False,
                error="not_in_fixtures",
                from_fixtures=True,
            )
        raw_status = entry.get("status", 200)
        status = int(raw_status) if raw_status is not None else None
        final_url = entry.get("final_url", url)
        body = None
        page = entry.get("page")
        if page:
            path = self.pages_dir / page
            if path.exists():
                body = path.read_text(encoding="utf-8", errors="replace")
        err = entry.get("error")
        ok = status is not None and 200 <= status < 400 and not err
        return ResolveResult(
            url=url,
            ok=ok,
            status=status,
            final_url=final_url,
            error=err,
            body=body,
            content_type=entry.get("content_type", "text/html"),
            from_fixtures=True,
        )


def resolve_url(
    url: str,
    *,
    session: Optional[requests.Session] = None,
    fixtures: Optional[FixtureStore] = None,
    timeout: float = TIMEOUT,
) -> ResolveResult:
    """Resolve a URL. Uses fixtures store when provided (offline)."""
    if fixtures is not None:
        return fixtures.get(url)

    sess = session or requests.Session()
    headers = {"User-Agent": DEFAULT_UA, "Accept": "text/html,application/xhtml+xml,*/*;q=0.8"}

    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https"):
        return ResolveResult(url=url, ok=False, error=f"unsupported_scheme:{parsed.scheme}")

    # HEAD first
    try:
        r = sess.head(url, headers=headers, allow_redirects=True, timeout=timeout)
        # Some servers dislike HEAD
        if r.status_code in (405, 501) or (r.status_code >= 400 and r.status_code != 404):
            raise requests.RequestException(f"HEAD status {r.status_code}")
        if r.status_code == 404:
            return ResolveResult(
                url=url,
                ok=False,
                status=404,
                final_url=str(r.url),
                error="http_404",
            )
        # For success HEAD, still GET body for title/overlap when HTML likely
        ctype = (r.headers.get("Content-Type") or "").lower()
        need_body = "html" in ctype or not ctype
        if need_body and 200 <= r.status_code < 400:
            try:
                g = sess.get(url, headers=headers, allow_redirects=True, timeout=timeout)
                return ResolveResult(
                    url=url,
                    ok=200 <= g.status_code < 400,
                    status=g.status_code,
                    final_url=str(g.url),
                    body=g.text if g.ok else None,
                    content_type=g.headers.get("Content-Type"),
                    error=None if g.ok else f"http_{g.status_code}",
                )
            except requests.RequestException:
                # HEAD succeeded; return without body
                return ResolveResult(
                    url=url,
                    ok=True,
                    status=r.status_code,
                    final_url=str(r.url),
                    content_type=r.headers.get("Content-Type"),
                )
        return ResolveResult(
            url=url,
            ok=200 <= r.status_code < 400,
            status=r.status_code,
            final_url=str(r.url),
            content_type=r.headers.get("Content-Type"),
            error=None if 200 <= r.status_code < 400 else f"http_{r.status_code}",
        )
    except requests.RequestException:
        pass

    # GET fallback
    try:
        g = sess.get(url, headers=headers, allow_redirects=True, timeout=timeout)
        return ResolveResult(
            url=url,
            ok=200 <= g.status_code < 400,
            status=g.status_code,
            final_url=str(g.url),
            body=g.text if "html" in (g.headers.get("Content-Type") or "").lower() or g.ok else None,
            content_type=g.headers.get("Content-Type"),
            error=None if 200 <= g.status_code < 400 else f"http_{g.status_code}",
        )
    except requests.RequestException as e:
        return ResolveResult(url=url, ok=False, error=f"network:{type(e).__name__}")
