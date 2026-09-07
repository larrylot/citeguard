from citeguard.classify import classify
from citeguard.models import Citation, ResolveResult


def _cit(url="https://example.com/x", text="Example", claim="Example topic"):
    return Citation(url=url, link_text=text, kind="link", line=1, claim=claim)


def test_dead_404():
    r = ResolveResult(url="https://x", ok=False, status=404, error="http_404")
    v = classify(_cit(), r)
    assert v.verdict == "dead"


def test_network_dead():
    r = ResolveResult(url="https://x", ok=False, error="network:ConnectionError")
    v = classify(_cit(), r)
    assert v.verdict == "dead"


def test_http_error():
    r = ResolveResult(url="https://x", ok=False, status=500, error="http_500")
    v = classify(_cit(), r)
    assert v.verdict == "http_error"


def test_clean_with_matching_title():
    body = "<html><head><title>Python Tutorial Docs</title></head><body>Python tutorial basics language</body></html>"
    r = ResolveResult(
        url="https://docs.python.org/3/tutorial/",
        ok=True,
        status=200,
        final_url="https://docs.python.org/3/tutorial/",
        body=body,
    )
    v = classify(
        _cit(
            url="https://docs.python.org/3/tutorial/",
            text="Python Tutorial",
            claim="Python tutorial basics language",
        ),
        r,
    )
    assert v.verdict == "clean"


def test_title_mismatch():
    body = "<html><head><title>Buy Cheap Shoes Online</title></head><body>sneakers boots fashion</body></html>"
    r = ResolveResult(
        url="https://example.invalid/python-asyncio-guide",
        ok=True,
        status=200,
        final_url="https://example.invalid/python-asyncio-guide",
        body=body,
    )
    v = classify(
        _cit(
            url="https://example.invalid/python-asyncio-guide",
            text="Python Asyncio Complete Guide",
            claim="asyncio best practices",
        ),
        r,
    )
    assert v.verdict == "title_mismatch"
