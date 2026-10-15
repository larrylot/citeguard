"""Conservative, explainable citation heuristics (not factual entailment)."""

from __future__ import annotations

from urllib.parse import urlsplit

from citeguard.models import Citation, CitationVerdict, ResolveResult
from citeguard.overlap import overlap_score, soft_title_match, tokenize
from citeguard.title import parse_html

TITLE_MATCH_THRESHOLD = 0.34
OVERLAP_THRESHOLD = 0.25
GENERIC_LABELS = frozenset({
    "source", "here", "link", "read more", "click here", "reference",
    "citation", "website", "documentation", "paper", "article",
})


def _host(url: str) -> str:
    try:
        h = (urlsplit(url).hostname or "").lower()
    except ValueError:
        return ""
    return h.removeprefix("www.")


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

    def verdict(name: str) -> CitationVerdict:
        return CitationVerdict(
            url=citation.url,
            link_text=citation.link_text,
            kind=citation.kind,
            line=citation.line,
            verdict=name,
            status=resolved.status,
            final_url=resolved.final_url,
            page_title=page_title,
            title_score=round(title_score, 3) if title_score is not None else None,
            overlap_score=round(o_score, 3) if o_score is not None else None,
            claim=claim,
            error=resolved.error,
            reasons=reasons.copy(),
        )

    if resolved.error == "not_in_fixtures":
        reasons.append("URL is absent from the offline fixtures catalog")
        return verdict("unresolved")

    if not resolved.ok:
        error = resolved.error or f"http_{resolved.status}"
        reasons.append(error)
        if error in {
            "blocked_private_address", "embedded_credentials",
            "unsupported_url", "invalid_url",
        }:
            return verdict("blocked")
        if resolved.status in (404, 410):
            return verdict("dead")
        if error.startswith("network:") or error in {
            "dns_failure", "dns_no_results", "body_too_large",
            "too_many_redirects", "redirect_missing_location",
        }:
            return verdict("unverifiable")
        return verdict("http_error")

    if resolved.body is None:
        reasons.append("URL reachable but content type cannot be checked as HTML")
        return verdict("unchecked")

    page_title, page_text = parse_html(resolved.body)
    if not page_text:
        reasons.append("URL reachable but has no readable HTML content")
        return verdict("unchecked")

    host_drift = bool(
        resolved.final_url and _host(resolved.final_url) != _host(citation.url)
    )
    if host_drift:
        reasons.append(
            f"cross-host redirect: {_host(citation.url)} to {_host(resolved.final_url)}"
        )

    label = citation.link_text.strip()
    descriptive_label = bool(label and label.lower() not in GENERIC_LABELS)
    checked_title = False
    if descriptive_label and page_title:
        title_score = soft_title_match(label, page_title)
        checked_title = True

    if host_drift and (title_score is None or title_score < 0.5):
        reasons.append("redirect to another host without a strong title match")
        return verdict("redirect_suspect")

    if descriptive_label and not page_title:
        reasons.append("cannot compare descriptive citation label: missing HTML title")
        return verdict("unchecked")

    if checked_title and title_score is not None and title_score < TITLE_MATCH_THRESHOLD:
        reasons.append(f"title overlap {title_score:.2f} below {TITLE_MATCH_THRESHOLD}")
        return verdict("title_mismatch")

    checked_claim = bool(check_overlap and len(tokenize(claim)) >= 3)
    if checked_claim:
        o_score = overlap_score(claim, page_text)
        threshold = 0.12 if (title_score is not None and title_score >= 0.5) else OVERLAP_THRESHOLD
        if o_score < threshold:
            reasons.append(f"claim token overlap {o_score:.2f} below {threshold}")
            return verdict("claim_weak")

    if not checked_title and not checked_claim:
        reasons.append("URL reachable, but no meaningful title or claim check was possible")
        return verdict("unchecked")

    reasons.append("reachable; available title/claim heuristics passed (not proof of truth)")
    return verdict("clean")
