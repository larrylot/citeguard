# CiteGuard summary — 01_ip_fragmentation_brief.md

```
CiteGuard — examples/realworld/01_ip_fragmentation_brief.md
Summary: {'clean': 1, 'title_mismatch': 1, 'dead': 1, 'total': 3}
------------------------------------------------------------
[OK] L8 https://www.rfc-editor.org/rfc/rfc791
       link_text: RFC 791 — Internet Protocol
       claim: Primary reference material is .
       status=200 final=https://www.rfc-editor.org/info/rfc791/ title="RFC 791: Internet Protocol | RFC Editor" title_score=1.0 overlap=0.333
       reasons: resolved; title/claim checks passed

[TITLE] L12 https://example.com/
       link_text: IPv4 Fragmentation Deep Dive — Official IETF Handbook
       claim: An agent dump incorrectly labeled it as .
       status=200 final=https://example.com/ title="Example Domain" title_score=0.0
       reasons: title soft-match 0.00 < 0.34

[DEAD] L13 http://127.0.0.1:9/mtu-probe
       link_text: Internal MTU probe dashboard
       claim: A secondary cite pointed at a local tooling endpoint that is not reachable from CI: .
       status=None final=None
       reasons: network:ConnectionError

```
