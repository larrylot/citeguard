"""Orchestrate citation checks and reuse HTTP results for repeated URLs."""

from __future__ import annotations

from collections import Counter
from pathlib import Path
from typing import Optional

import requests

from citeguard.classify import classify
from citeguard.extract import extract_from_path
from citeguard.models import ReportResult, ResolveResult
from citeguard.resolve import FixtureStore, resolve_url


def check_report(
    path: str | Path,
    *,
    fixtures_root: Optional[str | Path] = None,
    check_overlap: bool = True,
    timeout: float = 12.0,
    allow_private: bool = False,
    max_html_bytes: int = 2 * 1024 * 1024,
) -> ReportResult:
    path = Path(path)
    _text, citations = extract_from_path(str(path))
    store = FixtureStore.load(Path(fixtures_root)) if fixtures_root else None

    verdicts = []
    cache: dict[str, ResolveResult] = {}
    with requests.Session() as session:
        for citation in citations:
            resolved = cache.get(citation.url)
            if resolved is None:
                resolved = resolve_url(
                    citation.url,
                    session=None if store else session,
                    fixtures=store,
                    timeout=timeout,
                    allow_private=allow_private,
                    max_html_bytes=max_html_bytes,
                )
                cache[citation.url] = resolved
            verdicts.append(classify(citation, resolved, check_overlap=check_overlap))

    summary = dict(Counter(v.verdict for v in verdicts))
    summary["total"] = len(verdicts)
    return ReportResult(path=str(path), citations=verdicts, summary=summary)
