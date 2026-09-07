# CiteGuard — STATUS

**Lane:** Exploration bet (The Lord) — **active signal bet** (elevated 2026-09-07)  
**Capital:** 0 SEK  
**Outreach sent:** none (templates only; agent does not post)  
**Merchant / SaaS:** none  
**Date opened:** 2026-09-07 (Europe/Stockholm)  
**Last external-validation pass:** 2026-09-07 ~07:50 Europe/Stockholm

Source thesis: `/workspace/venture/exploration/2026-09-07-no-merchant.md` (Thesis 1).

## Signal metrics (7 days)

| Metric | Pass | Stretch | Actual | As of |
|--------|-----:|--------:|--------|-------|
| GitHub stars | ≥25 | ≥100 | — | — |
| Show HN points (if human posts) | ≥20 | ≥50 | — | — |
| Forks or “reproduced” issues | ≥3 | ≥10 | — | — |
| Tally/Google waitlist | ≥20 | ≥50 | — | — |

Fill Actual after human posts + form live. Do not invent numbers.

## Kill criteria (from exploration doc)

1. **&lt;10 stars AND &lt;10 waitlist** after 7 days with at least one public post attempt by human → kill or fold into blog-only.
2. **Core check accuracy &lt;80%** on fixture set → fix or kill **before** posting.
3. Looks like a **generic chatbot wrapper** in first ~20 comments → reposition or kill.

## Build checklist

- [x] Package `citeguard/` + pyproject + MIT + README
- [x] CLI `citeguard check`
- [x] Fixtures ≥8 reports + expected JSON + offline catalog
- [x] pytest accuracy gate ≥80%
- [x] SHOW_HN.md + POSTS.md (human)
- [x] WAITLIST.md
- [x] GitHub repo public + push: https://github.com/larrylot/citeguard
- [x] GitHub topics: citation, cli, llm, agents, markdown, research, hallucination, python, validation
- [x] GitHub Release v0.1.0 (notes → fixtures demo)
- [x] Citation Failure Corpus `corpus/` (20 snippets) committed
- [x] Docs / GitHub Pages one-pager (`docs/`) explaining output JSON
- [x] Awesome-list PRs opened where fit (see Notes); skips documented
- [x] PyPI: no token → `PYPI.md` prepared for human (no invent)
- [x] HUMAN-ONE-ACTION.md (Show HN)
- [ ] HUMAN: create Tally/Google Form, paste URL in README
- [ ] HUMAN: public post (HN / Reddit / LinkedIn templates) — **primary unlock**
- [ ] HUMAN: PyPI publish per `PYPI.md` when token ready

## External validation actions taken (2026-09-07)

| Action | Result |
|--------|--------|
| Topics | Set (incl. `hallucination`, not typo `hallucation`) |
| Release | v0.1.0 — see GitHub Releases |
| Corpus | `corpus/` 20 MD + README |
| Pages | `docs/` site; Pages enabled via `gh` if API allowed |
| Awesome PRs | Opened only where guidelines allow brand-new CLI; others skipped |
| PyPI | Blocked — no twine/token; `PYPI.md` written |
| Portfolio | CiteGuard elevated active signal; CSL demoted scrap/parked |

## Notes

No outreach emails. No Show HN/Reddit/LinkedIn by agent. Primary EAA remains merchant-blocked separately; this bet does not spend the 2000 SEK pool.
