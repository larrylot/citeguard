"""Safety and regression tests for CiteGuard 0.2."""

from __future__ import annotations

import json
import socket

from citeguard.check import check_report
from citeguard.classify import classify
from citeguard.cli import main
from citeguard.extract import extract_citations
from citeguard.models import Citation, ResolveResult
from citeguard.resolve import FixtureStore, resolve_url


class FakeResponse:
    def __init__(self, status=200, body=b"<html><title>Example</title><body>Example research claim</body></html>", content_type="text/html", location=None):
        self.status_code = status
        self.data = body
        self.headers = {"Content-Type": content_type}
        if location:
            self.headers["Location"] = location
        self.encoding = "utf-8"

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def iter_content(self, chunk_size=65536):
        yield self.data


class FakeSession:
    trust_env = True

    def __init__(self, *responses):
        self.responses = list(responses)
        self.urls = []

    def get(self, url, **kwargs):
        self.urls.append(url)
        assert kwargs["allow_redirects"] is False
        assert kwargs["stream"] is True
        return self.responses.pop(0)


def test_repeated_url_is_checked_for_each_claim(tmp_path, monkeypatch):
    doc = tmp_path / "report.md"
    doc.write_text(
        "Python supports arithmetic. [Python Guide](https://example.org/guide)\n"
        "Python forbids arithmetic. [Python Guide](https://example.org/guide)\n",
        encoding="utf-8",
    )
    calls = []

    def fake_resolve(url, **kwargs):
        calls.append(url)
        return ResolveResult(
            url=url, ok=True, status=200, final_url=url,
            body="<html><title>Python Guide</title><body>Python supports arithmetic.</body></html>",
        )

    monkeypatch.setattr("citeguard.check.resolve_url", fake_resolve)
    result = check_report(doc)
    assert len(result.citations) == 2
    assert len(calls) == 1
    assert [c.line for c in result.citations] == [1, 2]
    assert [c.verdict for c in result.citations] == ["clean", "clean"]
    # Lexical overlap is NOT a semantic contradiction detector.


def test_markdown_parser_ignores_code_and_keeps_same_url():
    doc = (
        "```md\n[not a citation](https://example.org/code)\n```\n"
        "`https://example.org/inline`\n"
        "[First](https://example.org/real) [Second](https://example.org/real)\n"
        "Visible https://example.org/bare.\n"
    )
    found = extract_citations(doc)
    assert [x.url for x in found] == [
        "https://example.org/real", "https://example.org/real",
        "https://example.org/bare",
    ]


def test_reference_style_markdown_link():
    text = "Read [Python Docs][p].\n\n[p]: https://docs.python.org/3/tutorial/\n"
    found = extract_citations(text)
    assert any(c.url == "https://docs.python.org/3/tutorial/" and c.line == 1 for c in found)


def test_footnote_uses_claim_line():
    text = "Some interesting assertion.[^1]\n\n[^1]: https://example.org/footnote\n"
    found = extract_citations(text)
    assert len(found) == 1
    assert found[0].line == 1
    assert found[0].kind == "footnote"


def test_default_fail_closed_for_unresolved(tmp_path, capsys):
    catalog = tmp_path / "fixtures"
    catalog.mkdir()
    (catalog / "catalog.json").write_text("{}")
    doc = tmp_path / "report.md"
    doc.write_text("[Something](https://example.org/unknown)")
    assert main(["check", str(doc), "--fixtures", str(catalog), "--json"]) == 1
    result = json.loads(capsys.readouterr().out)
    assert result["citations"][0]["verdict"] == "unresolved"


def test_no_citations_cannot_pass(tmp_path, capsys):
    doc = tmp_path / "empty.md"
    doc.write_text("An unsourced claim.")
    assert main(["check", str(doc), "--json"]) == 1
    assert json.loads(capsys.readouterr().out)["summary"]["total"] == 0


def test_private_ip_blocked_even_with_mock_http():
    session = FakeSession(FakeResponse())
    result = resolve_url("http://127.0.0.1/private", session=session)
    assert result.error == "blocked_private_address"
    assert session.urls == []


def test_credentials_blocked():
    result = resolve_url("https://user:secret@example.com/private")
    assert result.error == "embedded_credentials"


def test_redirect_to_private_ip_is_blocked(monkeypatch):
    import citeguard.resolve as resolver
    original = resolver._validate_target

    def fake_validation(url, *, allow_private=False):
        if url == "https://example.org/start":
            return None
        return original(url, allow_private=allow_private)

    monkeypatch.setattr(resolver, "_validate_target", fake_validation)
    session = FakeSession(FakeResponse(status=302, location="http://169.254.169.254/latest/meta-data"))
    result = resolve_url("https://example.org/start", session=session)
    assert result.error == "blocked_private_address"
    assert len(session.urls) == 1


def test_html_download_bounded(monkeypatch):
    monkeypatch.setattr("citeguard.resolve._validate_target", lambda *args, **kwargs: None)
    session = FakeSession(FakeResponse(body=b"X" * 128))
    result = resolve_url("https://example.org", session=session, max_html_bytes=64)
    assert result.error == "body_too_large"


def test_pdf_is_unchecked(monkeypatch):
    monkeypatch.setattr("citeguard.resolve._validate_target", lambda *args, **kwargs: None)
    session = FakeSession(FakeResponse(body=b"pdf", content_type="application/pdf"))
    resolved = resolve_url("https://example.org/document.pdf", session=session)
    verdict = classify(Citation(url=resolved.url, link_text="Document", claim="Evidence statement"), resolved)
    assert verdict.verdict == "unchecked"


def test_network_failure_is_unverifiable_not_dead():
    cit = Citation(url="https://example.org/", claim="A claim")
    resolved = ResolveResult(url=cit.url, ok=False, error="network:Timeout")
    assert classify(cit, resolved).verdict == "unverifiable"


def test_html_without_evidence_not_clean():
    cit = Citation(url="https://example.org/", link_text="source", claim="")
    resolved = ResolveResult(
        url=cit.url, ok=True, status=200, final_url=cit.url, body="<html><body>Hello</body></html>"
    )
    assert classify(cit, resolved).verdict == "unchecked"


def test_fixture_catalog_cannot_traverse(tmp_path):
    root = tmp_path / "fixtures"
    root.mkdir()
    (root / "pages").mkdir()
    outside = tmp_path / "secret.txt"
    outside.write_text("should not be included")
    (root / "catalog.json").write_text(json.dumps({
        "https://example.org": {"status": 200, "page": "../../secret.txt"}
    }))
    assert FixtureStore.load(root).get("https://example.org").body is None
