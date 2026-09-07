"""Orchestrate extract → resolve → classify for a Markdown report."""

from __future__ import annotations

from collections import Counter
from pathlib import Path
from typing import Optional

import requests

from citeguard.classify import classify
from citeguard.extract import extract_from_path
from citeguard.models import ReportResult
from citeguard.resolve import FixtureStore, resolve_url


def check_report(
    path: str | Path,
    *,
    fixtures_root: Optional[str | Path] = None,
    check_overlap: bool = True,
    timeout: float = 12.0,
) -> ReportResult:
    path = Path(path)
    _text, citations = extract_from_path(str(path))

    store = FixtureStore.load(Path(fixtures_root)) if fixtures_root else None
    session = None if store else requests.Session()

    verdicts = []
    for cit in citations:
        resolved = resolve_url(
            cit.url,
            session=session,
            fixtures=store,
            timeout=timeout,
        )
        verdicts.append(classify(cit, resolved, check_overlap=check_overlap))

    summary = dict(Counter(v.verdict for v in verdicts))
    summary["total"] = len(verdicts)
    return ReportResult(path=str(path), citations=verdicts, summary=summary)
