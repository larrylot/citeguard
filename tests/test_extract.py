from citeguard.extract import extract_citations


def test_markdown_links():
    text = "See [Python Tutorial](https://docs.python.org/3/tutorial/) for basics."
    cites = extract_citations(text)
    assert len(cites) == 1
    assert cites[0].url.endswith("/tutorial/")
    assert cites[0].link_text == "Python Tutorial"
    assert cites[0].kind == "link"


def test_skips_images():
    text = "![chart](https://example.com/x.png)\n[ok](https://example.com/page)"
    cites = extract_citations(text)
    assert len(cites) == 1
    assert cites[0].url == "https://example.com/page"


def test_footnotes():
    text = "Claim.[^1]\n\n[^1]: https://peps.python.org/pep-0008/\n"
    cites = extract_citations(text)
    assert any(c.kind == "footnote" for c in cites)
    assert cites[0].url.startswith("https://peps.python.org")


def test_bare_url():
    text = "Read https://docs.pytest.org/en/stable/ today."
    cites = extract_citations(text)
    assert len(cites) == 1
    assert "pytest" in cites[0].url


def test_dedupes():
    text = (
        "[A](https://example.com/a) and again [A2](https://example.com/a)"
    )
    cites = extract_citations(text)
    assert len(cites) == 1
