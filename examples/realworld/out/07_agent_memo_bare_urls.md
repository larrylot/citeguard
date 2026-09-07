# CiteGuard summary — 07_agent_memo_bare_urls.md

```
CiteGuard — examples/realworld/07_agent_memo_bare_urls.md
Summary: {'title_mismatch': 1, 'clean': 1, 'dead': 2, 'total': 4}
------------------------------------------------------------
[TITLE] L15 https://example.com/
       link_text: Official RFC Editor Operator Handbook
       claim: See the for deployment steps (planted title mismatch).
       status=200 final=https://example.com/ title="Example Domain" title_score=0.0
       reasons: title soft-match 0.00 < 0.34

[OK] L5 https://www.rfc-editor.org/rfc/rfc791
       claim: Spec page: https://www.rfc-editor.org/rfc/rfc791
       status=200 final=https://www.rfc-editor.org/info/rfc791/ title="RFC 791: Internet Protocol | RFC Editor" overlap=0.25
       reasons: resolved; title/claim checks passed

[DEAD] L10 https://this-domain-should-not-resolve-citeguard-test.invalid/x
       claim: https://this-domain-should-not-resolve-citeguard-test.invalid/x
       status=None final=None
       reasons: network:ConnectionError

[DEAD] L11 http://127.0.0.1:9/healthz
       claim: http://127.0.0.1:9/healthz
       status=None final=None
       reasons: network:ConnectionError

```
