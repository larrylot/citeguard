"""Accuracy ≥80% on planted fixtures (resolve + classify)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from citeguard.check import check_report

FIXTURES = Path(__file__).resolve().parent.parent / "fixtures"

REPORTS = sorted(FIXTURES.glob("*.expected.json"))


@pytest.fixture(scope="module")
def fixtures_root() -> Path:
    assert (FIXTURES / "catalog.json").exists()
    return FIXTURES


def _load_expected(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


@pytest.mark.parametrize("expected_path", REPORTS, ids=lambda p: p.stem)
def test_each_fixture_report(expected_path: Path, fixtures_root: Path):
    exp = _load_expected(expected_path)
    report = fixtures_root / exp["report"]
    assert report.exists(), report
    result = check_report(report, fixtures_root=fixtures_root)
    got = {c.url: c.verdict for c in result.citations}
    for item in exp["citations"]:
        url = item["url"]
        assert url in got, f"missing citation {url} in {report.name}; got {list(got)}"
        assert got[url] == item["verdict"], (
            f"{report.name}: {url} expected {item['verdict']} got {got[url]}"
        )


def test_overall_accuracy(fixtures_root: Path):
    total = 0
    correct = 0
    mismatches = []
    for expected_path in REPORTS:
        exp = _load_expected(expected_path)
        result = check_report(fixtures_root / exp["report"], fixtures_root=fixtures_root)
        got = {c.url: c.verdict for c in result.citations}
        for item in exp["citations"]:
            total += 1
            if got.get(item["url"]) == item["verdict"]:
                correct += 1
            else:
                mismatches.append(
                    (exp["report"], item["url"], item["verdict"], got.get(item["url"]))
                )
    assert total >= 8, "need enough fixture citations"
    acc = correct / total
    assert acc >= 0.80, f"accuracy {acc:.1%} < 80%; mismatches={mismatches}"


def test_cli_clean_and_dead(fixtures_root: Path):
    from citeguard.cli import main

    assert main(["check", str(fixtures_root / "clean.md"), "--fixtures", str(fixtures_root)]) == 0
    assert (
        main(["check", str(fixtures_root / "dead_link.md"), "--fixtures", str(fixtures_root)])
        == 1
    )
