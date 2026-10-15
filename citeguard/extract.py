"""Extract every citation occurrence without mistaking code examples for citations."""

from __future__ import annotations

import re

from markdown_it import MarkdownIt

from citeguard.models import Citation

MD = MarkdownIt("commonmark")
FOOTNOTE_DEF = re.compile(
    r"^\s*\[\^?([^\]]+)\]:\s*(https?://\S+)", re.IGNORECASE
)
BARE_URL = re.compile(r"https?://[^\s<>\]\)\"']+", re.IGNORECASE)
MARKDOWN_LINK = re.compile(r"!?\[[^\]]*\]\(https?://[^\s)]+\)")
SENTENCE_SPLIT = re.compile(r"(?<=[.!?])\s+")


def _claim_near(lines: list[str], line_idx: int, link_text: str = "") -> str:
    """Find nearby assertion text, without inflating overlap with URL/anchor text."""
    for idx in [line_idx, *range(line_idx - 1, max(-1, line_idx - 4), -1)]:
        if not 0 <= idx < len(lines):
            continue
        line = lines[idx]
        if idx != line_idx and (line.lstrip().startswith("#") or FOOTNOTE_DEF.match(line)):
            continue
        cleaned = MARKDOWN_LINK.sub(" ", line)
        cleaned = BARE_URL.sub(" ", cleaned)
        cleaned = re.sub(r"\[\^?[^\]]+\]", " ", cleaned)
        cleaned = re.sub(r"\s+", " ", cleaned).strip(" -\t")
        if not cleaned:
            continue
        parts = SENTENCE_SPLIT.split(cleaned)
        claim = (parts[-1] if parts else cleaned).strip()
        claim = re.sub(
            r"(?i)\b(according to|per|see|via|from|at|in)(\s+the)?\s*[.,;:]*\s*$",
            "", claim,
        ).strip(" -,")
        if claim:
            return claim
    return ""


def _location(
    lines: list[str], start: int, end: int, url: str, label: str,
    cursor_line: int, cursor_col: int,
) -> tuple[int, int]:
    """Find the next occurrence in document order, even for repeated URLs."""
    end = min(len(lines), max(start + 1, end))
    for idx in range(cursor_line, end):
        offset = cursor_col if idx == cursor_line else 0
        options = [url]
        if label:
            options.append(f"[{label}]")
        positions = [lines[idx].find(x, offset) for x in options]
        positions = [p for p in positions if p >= 0]
        if positions:
            pos = min(positions)
            return idx, pos + len(url)
    return start, 0


def extract_citations(text: str) -> list[Citation]:
    lines = text.splitlines()
    tokens = MD.parse(text)
    found: list[Citation] = []
    code_lines: set[int] = set()
    for token in tokens:
        if token.type in {"fence", "code_block", "html_block"} and token.map:
            code_lines.update(range(token.map[0], token.map[1]))

    for block in tokens:
        if block.type != "inline":
            continue
        start, end = block.map if block.map else (0, 1)
        if FOOTNOTE_DEF.match(lines[start]) if start < len(lines) else False:
            continue
        children = block.children or []
        active_url: str | None = None
        label_parts: list[str] = []
        cursor_line, cursor_col = start, 0

        for child in children:
            if child.type == "link_open":
                active_url = child.attrGet("href")
                label_parts = []
            elif child.type == "link_close":
                if active_url and active_url.lower().startswith(("http://", "https://")):
                    label = "".join(label_parts)
                    idx, cursor_col = _location(
                        lines, start, end, active_url, label, cursor_line, cursor_col,
                    )
                    cursor_line = idx
                    footnote_label = bool(re.fullmatch(r"\^?[0-9]+", label))
                    found.append(Citation(
                        url=active_url, link_text="" if footnote_label else label,
                        kind="footnote" if footnote_label else "link",
                        line=idx + 1, claim=_claim_near(lines, idx, label),
                    ))
                active_url = None
                label_parts = []
            elif child.type == "text":
                if active_url is not None:
                    label_parts.append(child.content)
                else:
                    for match in BARE_URL.finditer(child.content):
                        url = match.group(0).rstrip(".,;!?:")
                        idx, cursor_col = _location(
                            lines, start, end, url, "", cursor_line, cursor_col,
                        )
                        cursor_line = idx
                        found.append(Citation(
                            url=url, kind="bare", line=idx + 1,
                            claim=_claim_near(lines, idx),
                        ))
            elif child.type == "code_inline" and active_url is not None:
                label_parts.append(child.content)

    # CommonMark doesn't resolve footnote-style [^1] definitions. Find uses of
    # numbered/footnote references and associate each assertion with its source.
    for definition_idx, line in enumerate(lines):
        if definition_idx in code_lines:
            continue
        match = FOOTNOTE_DEF.match(line)
        if not match:
            continue
        marker, url = match.groups()
        url = url.rstrip(").,;")
        pointer = re.compile(r"\[\^?" + re.escape(marker) + r"\]")
        uses = [
            idx for idx, content in enumerate(lines)
            if idx != definition_idx and idx not in code_lines and pointer.search(content)
        ]
        for idx in uses or [definition_idx]:
            if any(c.url == url and c.line == idx + 1 for c in found):
                continue
            found.append(Citation(
                url=url, kind="footnote", line=idx + 1,
                claim=_claim_near(lines, idx),
            ))

    # Stable order by actual place in the report; do not collapse URL reuse.
    return sorted(found, key=lambda c: c.line)


def extract_from_path(path: str) -> tuple[str, list[Citation]]:
    with open(path, encoding="utf-8") as handle:
        text = handle.read()
    return text, extract_citations(text)
