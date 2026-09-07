# CiteGuard — STATUS

**Lane:** Exploration bet (The Lord) — **active signal bet** (elevated 2026-09-07)  
**Capital:** 0 SEK  
**Outreach sent:** none (templates only; agent does not post)  
**Merchant / SaaS:** none  
**Date opened:** 2026-09-07 (Europe/Stockholm)  
**Last external-validation pass:** 2026-09-07 ~08:00 Europe/Stockholm

Source thesis: `/workspace/venture/exploration/2026-09-07-no-merchant.md` (Thesis 1).

## Signal metrics (7 days)

| Metric | Pass | Stretch | Actual | As of |
|--------|-----:|--------:|--------|-------|
| GitHub stars | ≥25 | ≥100 | 0 | 2026-09-07 ~08:00 Europe/Stockholm |
| Show HN points (if human posts) | ≥20 | ≥50 | — | — |
| Forks or “reproduced” issues | ≥3 | ≥10 | 0 | 2026-09-07 ~08:00 Europe/Stockholm |
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
- [x] Real-world evidence dumps `examples/realworld/` + REPORT.md
- [x] PyPI: no token → `PYPI.md` prepared for human (no invent)
- [x] HUMAN-ONE-ACTION.md (Show HN)
- [ ] HUMAN: create Tally/Google Form, paste URL in README
- [ ] HUMAN: public post (HN / Reddit / LinkedIn templates) — **primary unlock**
- [ ] HUMAN: PyPI publish per `PYPI.md` when token ready

## External validation actions taken (2026-09-07)

| Action | Result |
|--------|--------|
| Topics | Set: citation, cli, llm, agents, markdown, research, hallucination, python, validation |
| Release | https://github.com/larrylot/citeguard/releases/tag/v0.1.0 |
| Corpus | `corpus/` 20 MD + README (pushed) |
| Pages | **live** https://larrylot.github.io/citeguard/ (`docs/` + `.nojekyll`) |
| Awesome PRs | Opened 2 (see below); skipped lists that require stars/age or “must use AI” |
| PyPI | Blocked — no `~/.pypirc` / `TWINE_*` / twine; `PYPI.md` written for human |
| Portfolio | CiteGuard elevated active signal; CSL demoted scrap/parked |

### Awesome PRs opened
1. https://github.com/DavidZWZ/Awesome-Deep-Research/pull/35 — Open-Source Implementations (deep-research citation verifier fit)
2. https://github.com/toolleeo/awesome-cli-apps-in-a-csv/pull/410 — `data/apps.csv` text-processing

### Awesome lists skipped (why)
- `agarrharr/awesome-cli-apps` — requires ≥20 stars and ≥3 months age
- `kyrolabs/awesome-agents` — rejects brand-new repos without traction
- `jamesmurdza/awesome-ai-devtools` — checklist requires tool that **uses AI**; CiteGuard is deterministic HTTP, not AI-powered

## Notes

No outreach emails. No Show HN/Reddit/LinkedIn by agent. Primary EAA remains merchant-blocked separately; this bet does not spend the 2000 SEK pool.

## Awesome PR status check (2026-09-07 ~07:55 Europe/Stockholm)

| PR | State | Merged | Comments | Notes |
|----|-------|--------|----------|-------|
| [DavidZWZ/Awesome-Deep-Research#35](https://github.com/DavidZWZ/Awesome-Deep-Research/pull/35) | **open** | no | 0 issue comments | mergeable_state=clean; no maintainer reply yet |
| [toolleeo/awesome-cli-apps-in-a-csv#410](https://github.com/toolleeo/awesome-cli-apps-in-a-csv/pull/410) | **open** | no | 0 issue comments | mergeable_state=clean; no maintainer reply yet |

## Real-world public evidence (2026-09-07)

Committed `examples/realworld/` — 7 synthetic dumps + `out/*.json` + [`REPORT.md`](examples/realworld/REPORT.md). Live check totals: **clean 6 / dead 10 / title_mismatch 4 / claim_weak 2 / total 22**. No outreach.

## External validation pass (2026-09-07 ~08:00 Europe/Stockholm)

| Item | Result |
|------|--------|
| Stars citeguard | 0 |
| Stars en549-skill | 0 |
| vs-alternatives |  (+ README + Pages link) |
| Dockerfile | root  (docker not installed on agent box; untested build) |
| Prior awesome PR comments | none on #35 / #410 — no replies sent |
| New awesome PRs | #1 wauldo, #7 jakemeany, #8 priyathamkat, #16 Poll-The-People (URLs above) |

### Awesome PR status (all open as of this pass)

| PR | State | Comments |
|----|-------|----------|
| [DavidZWZ/Awesome-Deep-Research#35](https://github.com/DavidZWZ/Awesome-Deep-Research/pull/35) | open | 0 |
| [toolleeo/awesome-cli-apps-in-a-csv#410](https://github.com/toolleeo/awesome-cli-apps-in-a-csv/pull/410) | open | 0 |
| [wauldo/awesome-rag-hallucination#1](https://github.com/wauldo/awesome-rag-hallucination/pull/1) | open | 0 |
| [jakemeany523/awesome-llm-evaluation#7](https://github.com/jakemeany523/awesome-llm-evaluation/pull/7) | open | 0 |
| [priyathamkat/Awesome-LLM-Evaluation#8](https://github.com/priyathamkat/Awesome-LLM-Evaluation/pull/8) | open | 0 |
| [Poll-The-People/awesome-rag#16](https://github.com/Poll-The-People/awesome-rag/pull/16) | open | 0 |

