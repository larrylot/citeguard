from pathlib import Path

from citeguard.resolve import FixtureStore

FIXTURES = Path(__file__).resolve().parent.parent / "fixtures"


def test_fixture_store_ok():
    store = FixtureStore.load(FIXTURES)
    r = store.get("https://docs.python.org/3/tutorial/")
    assert r.ok
    assert r.status == 200
    assert r.body and "Python" in r.body
    assert r.from_fixtures


def test_fixture_store_404():
    store = FixtureStore.load(FIXTURES)
    r = store.get("https://example.invalid/dead-citation-404")
    assert not r.ok
    assert r.status == 404
