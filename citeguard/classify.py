"""Classify a resolved citation into a verdict."""

from __future__ import annotations

from urllib.parse import urlparse

from citeguard.models import Citation, CitationVerdict, ResolveResult
from citeguard.overlap import overlap_score, soft_title_match
from citeguard.title import parse_html

TITLE_MATCH_THRESHOLD = 0.34
OVERLAP_THRESHOLD = 0.25
HOST_DRIFT_OK_PREFIXES = ("www.",)


def _host(url: str) -> str:
    try:
        h = (urlparse(url).hostname or "").lower()
    except Exception:
        return ""
    for p in HOST_DRIFT_OK_PREFIXES:
        if h.startswith(p):
            h = h[len(p) :]
    return h


def classify(
    citation: Citation,
    resolved: ResolveResult,
    *,
    check_overlap: bool = True,
) -> CitationVerdict:
    reasons: list[str] = []
    page_title = None
    title_score = None
    o_score = None
    claim = citation.claim

    if resolved.error == "not_in_fixtures":
        return CitationVerdict(
            url=citation.url,
            link_text=citation.link_text,
            kind=citation.kind,
            line=citation.line,
            verdict="unresolved",
            error=resolved.error,
            claim=claim,
            reasons=["URL not present in fixtures catalog"],
        )

    if not resolved.ok:
        verdict = "dead" if resolved.status == 404 or (resolved.error or "").endswith("404") else "http_error"
        if resolved.error and resolved.error.startswith("network:"):
            verdict = "dead"
        return CitationVerdict(
            url=citation.url,
            link_text=citation.link_text,
            kind=citation.kind,
            line=citation.line,
            verdict=verdict,
            status=resolved.status,
            final_url=resolved.final_url,
            error=resolved.error,
            claim=claim,
            reasons=[resolved.error or f"status {resolved.status}"],
        )

    page_title, page_text = parse_html(resolved.body)

    host_drift = bool(
        resolved.final_url and _host(resolved.final_url) != _host(citation.url)
    )
    if host_drift:
        reasons.append(
            f"host redirect {_host(citation.url)} → {_host(resolved.final_url)}"
        )

    if citation.link_text and page_title:
        title_score = soft_title_match(citation.link_text, page_title)
    elif citation.link_text or page_title:
        title_score = 0.0 if (citation.link_text and page_title is not None) else None

    # Cross-host redirects are a distinct class (even when title also mismatches).
    if host_drift and (title_score is None or title_score < 0.5):
        return CitationVerdict(
            url=citation.url,
            link_text=citation.link_text,
            kind=citation.kind,
            line=citation.line,
            verdict="redirect_suspect",
            status=resolved.status,
            final_url=resolved.final_url,
            page_title=page_title,
            title_score=round(title_score, 3) if title_score is not None else None,
            claim=claim,
            reasons=reasons or ["cross-host redirect without strong title match"],
        )

    if citation.link_text and page_title and title_score is not None:
        if title_score < TITLE_MATCH_THRESHOLD:
            reasons.append(
                f"title soft-match {title_score:.2f} < {TITLE_MATCH_THRESHOLD}"
            )
            return CitationVerdict(
                url=citation.url,
                link_text=citation.link_text,
                kind=citation.kind,
                line=citation.line,
                verdict="title_mismatch",
                status=resolved.status,
                final_url=resolved.final_url,
                page_title=page_title,
                title_score=round(title_score, 3),
                claim=claim,
                reasons=reasons,
            )

    if check_overlap and claim and page_text:
        o_score = overlap_score(claim, page_text)
        # Strong title match softens claim gate (link text already grounded in <title>).
        threshold = OVERLAP_THRESHOLD
        if title_score is not None and title_score >= 0.5:
            threshold = 0.12
        if o_score < threshold:
            reasons.append(f"claim–source overlap {o_score:.2f} < {threshold}")
            return CitationVerdict(
                url=citation.url,
                link_text=citation.link_text,
                kind=citation.kind,
                line=citation.line,
                verdict="claim_weak",
                status=resolved.status,
                final_url=resolved.final_url,
                page_title=page_title,
                title_score=round(title_score, 3) if title_score is not None else None,
                overlap_score=round(o_score, 3),
                claim=claim,
                reasons=reasons,
            )

    return CitationVerdict(
        url=citation.url,
        link_text=citation.link_text,
        kind=citation.kind,
        line=citation.line,
        verdict="clean",
        status=resolved.status,
        final_url=resolved.final_url,
        page_title=page_title,
        title_score=round(title_score, 3) if title_score is not None else None,
        overlap_score=round(o_score, 3) if o_score is not None else None,
        claim=claim,
        reasons=reasons or ["resolved; title/claim checks passed"],
    )
