"""Extract page title and visible text snippet from HTML."""

from __future__ import annotations

import re
from typing import Optional, Tuple

from bs4 import BeautifulSoup

from citeguard.overlap import snippet


def parse_html(body: Optional[str]) -> Tuple[Optional[str], str]:
    """Return (title, text_snippet)."""
    if not body:
        return None, ""
    # Fast path for tiny planted fixtures without full parse failure
    try:
        soup = BeautifulSoup(body, "html.parser")
    except Exception:
        m = re.search(r"<title[^>]*>(.*?)</title>", body, re.I | re.S)
        title = re.sub(r"\s+", " ", m.group(1)).strip() if m else None
        return title, snippet(re.sub(r"<[^>]+>", " ", body))

    title = None
    if soup.title and soup.title.string:
        title = re.sub(r"\s+", " ", soup.title.string).strip()
    elif soup.title:
        title = re.sub(r"\s+", " ", soup.title.get_text(" ", strip=True)).strip() or None

    # Drop scripts/styles
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()
    text = soup.get_text(" ", strip=True)
    text = re.sub(r"\s+", " ", text)
    return title, snippet(text)
