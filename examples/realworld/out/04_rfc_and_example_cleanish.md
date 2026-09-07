# CiteGuard summary — 04_rfc_and_example_cleanish.md

```
CiteGuard — examples/realworld/04_rfc_and_example_cleanish.md
Summary: {'clean': 2, 'dead': 1, 'total': 3}
------------------------------------------------------------
[OK] L5 https://www.rfc-editor.org/rfc/rfc791
       link_text: RFC 791
       claim: Canonical text:
       status=200 final=https://www.rfc-editor.org/info/rfc791/ title="RFC 791: Internet Protocol | RFC Editor" title_score=1.0 overlap=0.5
       reasons: resolved; title/claim checks passed

[OK] L6 https://example.com/
       link_text: Example Domain
       claim: Placeholder host used in documentation examples:
       status=200 final=https://example.com/ title="Example Domain" title_score=1.0 overlap=0.4
       reasons: resolved; title/claim checks passed

[DEAD] L10 http://127.0.0.1:9/rfc791-errata.json
       link_text: RFC 791 annotated errata dump
       claim: The agent also invented a footnote pointing
       status=None final=None
       reasons: network:ConnectionError

```
