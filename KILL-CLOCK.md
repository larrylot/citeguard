# CiteGuard kill clock (multi-signal)
**Show HN:** https://news.ycombinator.com/item?id=49594410  
**Clock start:** 2026-09-07 · **Decision deadline:** 2026-09-14 09:00 Europe/Stockholm

## Principle
**HN performance alone is not a kill criterion.** A weak Show HN is evidence about *distribution on HN*, not automatic proof the product has no value. Weight these **equally** as external evidence:

| Signal class | Examples |
|--------------|----------|
| GitHub adoption | stars, forks, clones, watchers |
| Network acceptance | merged PRs into lists/registries; external references/links |
| Usage | installs (PyPI downloads when live), issues from others, PRs from others, “I tried it” reports |
| Substantive feedback | bug reports, feature asks, criticism that implies real use |
| HN / social | points, comments — *distribution channel evidence only* |

## Outcomes (review on deadline — holistically)
| Outcome | Guidance |
|---------|----------|
| **KEEP / scale** | Clear external pull on **any** strong channel: e.g. ≥25 stars, **or** ≥3 forks + external issues, **or** merged list/registry PRs driving clones/stars, **or** documented third-party usage — even if HN stayed flat |
| **MODIFY** | Mixed/weak-but-nonzero signals (a few stars, useful feedback, 1 merge) — reposition distribution; do not kill for HN alone |
| **KILL / fold** | After 7 days **and** Show HN attempted: **no meaningful external evidence across the board** (≈0 stars, 0 forks, 0 merges, 0 external issues/usage, no substantive feedback) — product+distribution both unproven. If HN failed but *other* channels show life → **MODIFY**, not kill |

## Anti-patterns
- Do not kill solely because HN score &lt;10
- Do not KEEP solely because of self-activity (our own commits/PRs)
- Fixture accuracy &lt;80% → fix-or-kill immediately (quality gate, independent)

## Anti-spam
No more awesome-list PRs. Agent does not post HN/Reddit/LinkedIn.
