"""Token overlap between claim sentences and page snippets."""

from __future__ import annotations

import re
from typing import Iterable

STOPWORDS = frozenset(
    """
    a an the and or but if in on at to for of from by with as is are was were be
    been being it this that these those i you he she we they them their our your
    not no nor so than then too very can could should would may might will just
    about into over after before between under again further once here there when
    where why how all each few more most other some such only own same
    """.split()
)

TOKEN_RE = re.compile(r"[a-z0-9][a-z0-9\-']{1,}", re.IGNORECASE)


def tokenize(text: str) -> set[str]:
    tokens = {t.lower() for t in TOKEN_RE.findall(text or "")}
    return {t for t in tokens if t not in STOPWORDS and len(t) > 2}


def overlap_score(claim: str, page_text: str) -> float:
    """Jaccard-like overlap of claim tokens vs page tokens (claim-centric).

    Returns fraction of claim tokens that appear in the page snippet.
    Empty claim → 1.0 (no claim to fail). Empty page with claim → 0.0.
    """
    claim_toks = tokenize(claim)
    if not claim_toks:
        return 1.0
    page_toks = tokenize(page_text)
    if not page_toks:
        return 0.0
    hit = claim_toks & page_toks
    return len(hit) / len(claim_toks)


def soft_title_match(link_text: str, page_title: str) -> float:
    """Soft-match link text against HTML title (0..1)."""
    a = tokenize(link_text)
    b = tokenize(page_title)
    if not a or not b:
        # If link text is a URL-ish short host label, compare hosts loosely
        if link_text and page_title:
            lt = link_text.lower().strip()
            pt = page_title.lower().strip()
            if lt in pt or pt in lt:
                return 0.7
            return 0.0
        return 1.0  # nothing to mismatch
    inter = a & b
    # Prefer recall of link-text tokens in the title
    return len(inter) / len(a)


def snippet(text: str, limit: int = 4000) -> str:
    if not text:
        return ""
    return text[:limit]
