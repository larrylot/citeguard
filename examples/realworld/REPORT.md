# CiteGuard real-world evidence run

**Date:** 2026-09-07 (Europe/Stockholm)  
**Repo:** https://github.com/larrylot/citeguard  
**Mode:** live network `citeguard check` (no `--fixtures`) on synthetic “agent research dumps”  
**Purpose:** public evidence that CiteGuard flags dead links and title mismatches on external-looking Markdown — not a claim about any third-party company’s wrongdoing.

All dumps under `examples/realworld/*.md` are **synthetic**. URLs are either well-known public pages (`https://example.com`, `https://www.rfc-editor.org/rfc/rfc791`) or deliberately broken (`http://127.0.0.1:9/...`, `https://this-domain-should-not-resolve-citeguard-test.invalid/...`).

Per-file machine output: [`out/`](out/) (`*.json` + human `*.md` summaries).

## Per-dump findings (CiteGuard summary counts)

| Dump | clean (ok) | dead | title_mismatch | claim_weak | total |
|------|----------:|-----:|---------------:|-----------:|------:|
| [01_ip_fragmentation_brief](01_ip_fragmentation_brief.md) | 1 | 1 | 1 | 0 | 3 |
| [02_vanished_mirror_survey](02_vanished_mirror_survey.md) | 0 | 3 | 0 | 1 | 4 |
| [03_title_bait_example_com](03_title_bait_example_com.md) | 0 | 0 | 1 | 0 | 1 |
| [04_rfc_and_example_cleanish](04_rfc_and_example_cleanish.md) | 2 | 1 | 0 | 0 | 3 |
| [05_multi_failure_stew](05_multi_failure_stew.md) | 0 | 2 | 1 | 1 | 4 |
| [06_footnotes_style](06_footnotes_style.md) | 2 | 1 | 0 | 0 | 3 |
| [07_agent_memo_bare_urls](07_agent_memo_bare_urls.md) | 1 | 2 | 1 | 0 | 4 |
| **Totals** | **6** | **10** | **4** | **2** | **22** |

Counts are CiteGuard’s per-unique-URL verdicts (duplicate URLs in one dump collapse to one citation).

## What failed (by design)

| Failure mode | How it was planted | Typical verdict |
|--------------|--------------------|-----------------|
| Dead TCP / refused | `http://127.0.0.1:9/...` | `dead` |
| Dead DNS | `https://this-domain-should-not-resolve-citeguard-test.invalid/...` | `dead` |
| Title mismatch | Misleading anchor text → `https://example.com/` (page title “Example Domain”) | `title_mismatch` |
| Working controls | `https://www.rfc-editor.org/rfc/rfc791`, honestly labeled `https://example.com/` | usually `clean` (sometimes `claim_weak` when claim tokens are thin) |

## Reproduce

```bash
cd citeguard
python3 -m venv .venv && source .venv/bin/activate
pip install -e .
mkdir -p examples/realworld/out
for f in examples/realworld/[0-9]*.md; do
  base=$(basename "$f" .md)
  citeguard check "$f" --json --timeout 20 > "examples/realworld/out/${base}.json" || true
  citeguard check "$f" --timeout 20 > "examples/realworld/out/${base}.md" || true
done
```

Demo site: https://larrylot.github.io/citeguard/
