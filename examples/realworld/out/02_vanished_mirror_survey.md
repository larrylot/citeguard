# CiteGuard summary — 02_vanished_mirror_survey.md

```
CiteGuard — examples/realworld/02_vanished_mirror_survey.md
Summary: {'dead': 3, 'claim_weak': 1, 'total': 4}
------------------------------------------------------------
[DEAD] L5 https://this-domain-should-not-resolve-citeguard-test.invalid/x
       link_text: FragSurvey 2024 PDF (mirror A)
       claim: Agent claimed to locate three mirrors of a “2024 fragmentation survey”:
       status=None final=None
       reasons: network:ConnectionError

[DEAD] L6 https://this-domain-should-not-resolve-citeguard-test.invalid/frag-survey-2024
       link_text: FragSurvey 2024 HTML (mirror B)
       claim: - [FragSurvey 2024 PDF (mirror A)](https://this-domain-should-not-resolve-citeguard-test.invalid/x)
       status=None final=None
       reasons: network:ConnectionError

[DEAD] L7 http://127.0.0.1:9/cache/frag-survey
       link_text: Local cache of FragSurvey
       claim: - [FragSurvey 2024 HTML (mirror B)](https://this-domain-should-not-resolve-citeguard-test.invalid/frag-survey-2024)
       status=None final=None
       reasons: network:ConnectionError

[WEAK] L9 https://example.com/
       link_text: Example Domain
       claim: One honest public placeholder was also included: .
       status=200 final=https://example.com/ title="Example Domain" title_score=1.0 overlap=0.0
       reasons: claim–source overlap 0.00 < 0.12

```
