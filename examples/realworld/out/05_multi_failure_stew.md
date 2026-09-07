# CiteGuard summary — 05_multi_failure_stew.md

```
CiteGuard — examples/realworld/05_multi_failure_stew.md
Summary: {'claim_weak': 1, 'title_mismatch': 1, 'dead': 2, 'total': 4}
------------------------------------------------------------
[WEAK] L5 https://www.rfc-editor.org/rfc/rfc791
       link_text: Internet Protocol (RFC 791)
       claim: Spec: — expected clean.
       status=200 final=https://www.rfc-editor.org/info/rfc791/ title="RFC 791: Internet Protocol | RFC Editor" title_score=1.0 overlap=0.0
       reasons: claim–source overlap 0.00 < 0.12

[TITLE] L6 https://example.com/
       link_text: Path MTU Discovery Operator Runbook
       claim: Mis-titled placeholder: .
       status=200 final=https://example.com/ title="Example Domain" title_score=0.0
       reasons: title soft-match 0.00 < 0.34

[DEAD] L7 https://this-domain-should-not-resolve-citeguard-test.invalid/status
       link_text: Commercial PMTUD SaaS status page
       claim: Dead DNS: .
       status=None final=None
       reasons: network:ConnectionError

[DEAD] L8 http://127.0.0.1:9/blackhole
       link_text: Lab blackhole collector
       claim: Dead local: .
       status=None final=None
       reasons: network:ConnectionError

```
