# CiteGuard kill clock
**Show HN:** https://news.ycombinator.com/item?id=49594410 (posted 2026-09-07 by lordlarry)  
**Clock start:** 2026-09-07  
**Decision deadline:** **2026-09-14 09:00 Europe/Stockholm** (routine `citeguard-7-day-keep-kill`)

## Thresholds
| Outcome | Condition |
|---------|-----------|
| KEEP / scale | ≥25 GitHub stars **OR** ≥20 HN points (or forks≥3 + external issues/PRs) |
| MODIFY | 10–24 stars OR 10–19 HN points — reposition, keep building |
| KILL / fold | <10 stars **AND** HN peak <10 points after 7 days with Show HN done; OR “chatbot wrapper” pile-on |

## Soft outs
- Fixture accuracy <80% → fix-or-kill immediately (independent)
- Merged registry PRs with measurable inbound can support MODIFY, not alone KEEP

## Anti-spam
- No more awesome-list PRs
- Agent does not post HN/Reddit/LinkedIn

## Snapshot log
See `metrics/hn-github.log` and `STATUS.md`. T0: score=1, stars=0, substantive comments=0.
