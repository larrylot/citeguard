from citeguard.overlap import overlap_score, soft_title_match, tokenize


def test_tokenize_drops_stopwords():
    toks = tokenize("The Python tutorial is easy to learn")
    assert "python" in toks
    assert "the" not in toks


def test_title_soft_match():
    score = soft_title_match(
        "Python Tutorial",
        "The Python Tutorial — Python 3.13 documentation",
    )
    assert score >= 0.5


def test_title_mismatch_low():
    score = soft_title_match(
        "Python Asyncio Complete Guide",
        "Buy Cheap Shoes Online — MegaDealz SEO Farm",
    )
    assert score < 0.34


def test_overlap_high():
    claim = "Requests is an elegant HTTP library for Python"
    page = "Requests is an elegant and simple HTTP library for Python, built for human beings."
    assert overlap_score(claim, page) >= 0.5


def test_overlap_low():
    claim = "Kubernetes horizontal pod autoscaling requires metrics server"
    page = "Global mean temperature continues to rise. Greenhouse gas emissions from fossil fuels."
    assert overlap_score(claim, page) < 0.25
