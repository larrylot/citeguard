# CiteGuard vs alternatives

Honest comparison so you can pick the right tool. Labels: **FACT** = observable from public docs/repos/behavior; **ASSUMPTION** = reasoned conjecture, not measured here.

CiteGuard scope (reminder): local CLI that checks **citations already written** into agent / deep-research Markdown — URL resolve, title soft-match, optional claim–source token overlap, offline fixtures. It does **not** generate research, score RAG retrieval, or prove scholarly correctness.

---

## 1. “Just ask ChatGPT” (or another chat LLM)

| Dimension | CiteGuard | Ask ChatGPT / chat LLM |
|-----------|-----------|-------------------------|
| Reproducibility | **FACT:** Deterministic HTTP resolve + scored heuristics for a given page snapshot | **FACT:** Model sampling + tool browsing vary run-to-run |
| Offline / CI | **FACT:** `--fixtures` mode with planted catalog | **FACT:** Needs network + model access |
| Cost / keys | **FACT:** No API key for core checks | **FACT:** Subscription or API spend |
| Audit trail | **FACT:** Per-URL JSON verdicts | **ASSUMPTION:** Chat transcripts are harder to gate in CI |
| Checker hallucination | **FACT:** No LLM in CiteGuard’s loop | **FACT:** An LLM can invent “looks fine” for a dead/bait cite |

**When to use ChatGPT instead:** exploratory reading, rewriting claims, or judging *semantic* support of a nuanced scientific/legal argument.

**When to use CiteGuard:** CI gate or batch pass over agent Markdown dumps where dead links and title bait are the failure modes you care about first.

---

## 2. LinkChecker ([linkchecker/linkchecker](https://github.com/linkchecker/linkchecker))

| Dimension | CiteGuard | LinkChecker |
|-----------|-----------|-------------|
| Primary job | **FACT:** Citation-aware checks on Markdown reports | **FACT:** Recursive website / document link checking |
| Stars (approx.) | See repo | **FACT:** ~1k+ GitHub stars (public count as of 2026-09) |
| Dead URLs | **FACT:** Yes (`dead` / `http_error`) | **FACT:** Yes (mature HTTP checking) |
| Title vs link-text | **FACT:** Soft-match → `title_mismatch` | **ASSUMPTION:** Not citation-title aware out of the box |
| Claim–source overlap | **FACT:** Optional token overlap → `claim_weak` | **FACT:** Out of scope |
| Markdown agent reports | **FACT:** First-class (`link` / `footnote` / `bare`) | **ASSUMPTION:** Possible via HTML export; not tailored to agent cites |
| Offline fixtures | **FACT:** Planted catalog for CI | **ASSUMPTION:** Typically live network unless you mock |

**Overlap:** both catch dead links. **CiteGuard adds** title-bait and weak-overlap heuristics aimed at *agent research dumps*, not full-site crawls.

**Use LinkChecker** for site QA / docs sites. **Use CiteGuard** for per-report citation hygiene after a deep-research agent run.

---

## 3. html-proofer ([gjtorikian/html-proofer](https://github.com/gjtorikian/html-proofer))

| Dimension | CiteGuard | html-proofer |
|-----------|-----------|--------------|
| Primary job | **FACT:** Markdown citation verifier | **FACT:** Validate *rendered HTML* (links, images, scripts, favicon, etc.) |
| Typical home | Agent research Markdown | Static site / Jekyll / docs pipelines |
| Stars (approx.) | See repo | **FACT:** ~1.6k+ GitHub stars (public count as of 2026-09) |
| Dead links | **FACT:** Yes | **FACT:** Yes |
| Title / claim heuristics | **FACT:** Yes | **FACT:** No (link existence / HTML integrity focus) |
| Language | **FACT:** Python CLI | **FACT:** Ruby gem |

**Overlap:** link existence. **Not substitutes:** html-proofer assumes you already have HTML output; CiteGuard assumes Markdown citation lists from agents.

---

## 4. Academic / agent benches (e.g. ReportBench)

**ReportBench** ([ByteDance-BandAI/ReportBench](https://github.com/ByteDance-BandAI/ReportBench), [arXiv:2508.15804](https://arxiv.org/abs/2508.15804)):

| Dimension | CiteGuard | ReportBench |
|-----------|-----------|-------------|
| Role | **FACT:** Lightweight *tool* you run on a report file | **FACT:** *Benchmark* + agent eval framework for deep-research reports |
| Ground truth | **FACT:** None required (heuristic checks) | **FACT:** Expert arXiv survey papers as gold references (per paper/README) |
| Citation quality | **FACT:** Resolve + soft title + token overlap | **FACT:** Reference precision/recall vs gold; citation match rate via semantic checks (per paper) |
| Non-cited claims | **FACT:** Not evaluated | **FACT:** Dual-path eval with web-connected LLM voting (per paper) |
| Cost | **FACT:** Free local HTTP | **ASSUMPTION:** Non-trivial LLM / scraping cost to run full bench |
| CI smoke test | **FACT:** Designed for fixture gates | **ASSUMPTION:** Heavier; research eval, not a 1-file smoke check |

**FACT (from ReportBench paper abstract / README):** commercial Deep Research agents can outperform base LLMs on coverage/grounding but still show room for improvement on citation breadth and factual consistency; citation match rates in their published table are far from 100% (e.g. OpenAI Deep Research ~78.9% cit. match rate in their reported table).

**ASSUMPTION:** CiteGuard would catch a subset of failures ReportBench cares about (dead/bait URLs, weak surface overlap) but would **miss** semantic mis-citation and gold-reference coverage gaps that ReportBench measures.

Related family (not deep compared here): RAGAS, DeepEval, TruLens — **FACT:** LLM-as-judge / RAG faithfulness frameworks; **ASSUMPTION:** complementary to CiteGuard’s deterministic cite layer, not competitors for the same CLI niche.

---

## Quick chooser

| Need | Prefer |
|------|--------|
| CI gate on agent Markdown cites, no keys | **CiteGuard** |
| Crawl / QA a docs website | **LinkChecker** or **html-proofer** |
| Judge “does this paragraph support the claim?” semantically | Chat LLM / NLI / ReportBench-style pipeline |
| Score a deep-research *product* vs academic surveys | **ReportBench** (or similar benches) |
| RAG faithfulness on retrieved chunks | RAGAS / DeepEval / etc. |

---

## What CiteGuard explicitly does *not* claim

- Prove a source supports a legal or scientific conclusion (**ASSUMPTION:** humans / domain judges still required).
- Replace retrieval evaluation or hallucination benchmarks.
- Match LinkChecker’s site-crawl depth or html-proofer’s HTML asset checks.

Last updated: 2026-09-07 (Europe/Stockholm). Star counts drift — check GitHub for live numbers.
