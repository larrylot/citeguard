"""Shared data models for CiteGuard."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Optional


VERDICTS = (
    "clean",
    "dead",
    "http_error",
    "title_mismatch",
    "claim_weak",
    "redirect_suspect",
    "unresolved",
)


@dataclass
class Citation:
    """One extracted citation from Markdown."""

    url: str
    link_text: str = ""
    kind: str = "link"  # link | footnote | bare
    line: int = 0
    claim: str = ""
    source_span: str = ""


@dataclass
class ResolveResult:
    url: str
    ok: bool
    status: Optional[int] = None
    final_url: Optional[str] = None
    error: Optional[str] = None
    body: Optional[str] = None
    content_type: Optional[str] = None
    from_fixtures: bool = False


@dataclass
class CitationVerdict:
    url: str
    link_text: str
    kind: str
    line: int
    verdict: str
    status: Optional[int] = None
    final_url: Optional[str] = None
    page_title: Optional[str] = None
    title_score: Optional[float] = None
    overlap_score: Optional[float] = None
    claim: str = ""
    error: Optional[str] = None
    reasons: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class ReportResult:
    path: str
    citations: list[CitationVerdict]
    summary: dict[str, int] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "path": self.path,
            "summary": self.summary,
            "citations": [c.to_dict() for c in self.citations],
        }
