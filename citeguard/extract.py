"""Extract citations from Markdown agent reports."""

from __future__ import annotations

import re
from typing import Iterable

from citeguard.models import Citation

# [text](url) — skip images ![alt](url)
LINK_RE = re.compile(
    r"(?<!!)\[([^\]]*)\]\((https?://[^)\s]+)\)",
    re.IGNORECASE,
)
# Footnote defs: [^1]: https://...  or  [1]: https://...
FOOTNOTE_RE = re.compile(
    r"^[ \t]*(?:\[\^?[^\]]+\]:)\s*(https?://\S+)",
    re.IGNORECASE | re.MULTILINE,
)
# Bare URLs on their own (conservative)
BARE_URL_RE = re.compile(r"(?<![(\[])(https?://[^\s<>\]\)\"']+)", re.IGNORECASE)

SENTENCE_SPLIT = re.compile(r"(?<=[.!?])\s+")


def _claim_near(lines: list[str], line_idx: int, link_text: str = "") -> str:
    """Pick the sentence / clause near a link as the claim."""
    line = lines[line_idx] if 0 <= line_idx < len(lines) else ""
    # Prefer same-line text with link markup removed (do not keep link text —
    # it often matches <title> and inflates claim–source overlap).
    cleaned = LINK_RE.sub(" ", line)
    cleaned = re.sub(r"\[\^[^\]]+\]", " ", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned).strip(" -	")
    if cleaned:
        parts = SENTENCE_SPLIT.split(cleaned)
        claim = (parts[-1] if parts else cleaned).strip()
        claim = re.sub(
            r"(?i)\b(according to|per|see|via|from|at|in)\s*[.,;:]*\s*$",
            "",
            claim,
        ).strip(" -")
        return claim
    # Fall back to previous non-empty line
    for i in range(line_idx - 1, max(-1, line_idx - 4), -1):
        prev = lines[i].strip()
        if prev and not prev.startswith("#") and not FOOTNOTE_RE.match(prev):
            parts = SENTENCE_SPLIT.split(prev)
            return (parts[-1] if parts else prev).strip()
    return link_text or ""


def extract_citations(text: str) -> list[Citation]:
    """Extract unique-ordered citations from Markdown text."""
    lines = text.splitlines()
    found: list[Citation] = []
    seen: set[str] = set()

    def add(url: str, link_text: str, kind: str, line: int, claim: str) -> None:
        key = url.rstrip(").,;")
        if key in seen:
            return
        seen.add(key)
        found.append(
            Citation(
                url=key,
                link_text=link_text.strip(),
                kind=kind,
                line=line + 1,
                claim=claim,
            )
        )

    for i, line in enumerate(lines):
        for m in LINK_RE.finditer(line):
            text_label, url = m.group(1), m.group(2)
            add(url, text_label, "link", i, _claim_near(lines, i, text_label))

        fm = FOOTNOTE_RE.match(line)
        if fm:
            url = fm.group(1).rstrip(").,;")
            add(url, "", "footnote", i, _claim_near(lines, i))

    # Bare URLs not already captured
    for i, line in enumerate(lines):
        # Skip lines that are mostly link/footnote defs already handled
        if LINK_RE.search(line) or FOOTNOTE_RE.match(line):
            continue
        for m in BARE_URL_RE.finditer(line):
            add(m.group(1).rstrip(").,;"), "", "bare", i, _claim_near(lines, i))

    return found


def extract_from_path(path: str) -> tuple[str, list[Citation]]:
    with open(path, encoding="utf-8") as f:
        text = f.read()
    return text, extract_citations(text)
