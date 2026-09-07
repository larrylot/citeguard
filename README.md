# CiteGuard

[![CI](https://github.com/larrylot/citeguard/actions/workflows/ci.yml/badge.svg)](https://github.com/larrylot/citeguard/actions/workflows/ci.yml)


**Local CLI that verifies citations in agent / deep-research Markdown reports.**

`citeguard check report.md` → per-citation verdicts: URL resolve, title/host soft-match, optional claim–source overlap.

- **No API keys** for core checks
- **No telemetry**, no SaaS, no account
- **Offline `--fixtures` mode** for CI
- MIT licensed

> Exploration bet for The Lord (0 SEK). Not a merchant product.

## Why not “just ask ChatGPT”?

| | CiteGuard | Ask ChatGPT / another LLM |
|--|-----------|---------------------------|
| Reproducible | Deterministic resolve + scores | Non-deterministic prose |
| Offline CI | `--fixtures` planted cases | Needs network + model |
| Cost / keys | Free local HTTP | API key / subscription |
| Audit trail | JSON verdicts per URL | Chat transcript |
| Hallucination check on the checker | No LLM in the loop | Can invent “looks fine” |

CiteGuard does **not** claim to prove a source supports a legal/scientific conclusion. It flags **dead links, title bait, weak overlap, and shady redirects** — the failure modes that show up in agent research dumps.

## Agent skill

Portable `SKILL.md` (Cursor / Claude / Codex / agentskills.io format):

- Canonical: [`skill/SKILL.md`](skill/SKILL.md)
- Cursor mirror: [`.cursor/skills/citeguard/SKILL.md`](.cursor/skills/citeguard/SKILL.md)
- skills CLI layout: [`skills/citeguard/SKILL.md`](skills/citeguard/SKILL.md)

```bash
npx skills add larrylot/citeguard -s citeguard -y
```

## Install

```bash
cd citeguard
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Demo (copy-paste)

```bash
# Offline CI-style check on a clean planted report
citeguard check fixtures/clean.md --fixtures

# A bad report (dead links) — exits 1
citeguard check fixtures/dead_link.md --fixtures

# Title-bait SEO farm planted as "asyncio docs"
citeguard check fixtures/title_mismatch.md --fixtures

# Machine-readable
citeguard check fixtures/mixed.md --fixtures --json
```

Example human output:

```
CiteGuard — fixtures/mixed.md
Summary: {'clean': 3, 'dead': 1, 'title_mismatch': 1, 'total': 5}
------------------------------------------------------------
[OK] L3 https://docs.github.com/en/actions
...
[DEAD] L7 https://example.invalid/dead-citation-404
...
[TITLE] L9 https://example.invalid/python-asyncio-guide
```

Live network check (no fixtures):

```bash
citeguard check path/to/agent-report.md
citeguard check path/to/agent-report.md --json --no-overlap
```

## Verdicts

| Verdict | Meaning |
|---------|---------|
| `clean` | Resolved; title/claim checks passed |
| `dead` | 404 or network failure |
| `http_error` | Non-success HTTP (e.g. 500) |
| `title_mismatch` | Link text soft-match vs `<title>` too low |
| `claim_weak` | Claim sentence tokens barely appear in page text |
| `redirect_suspect` | Cross-host redirect without strong title match |
| `unresolved` | URL missing from fixtures catalog (fixtures mode only) |

## Real-world evidence dumps

Synthetic agent-style Markdown under [`examples/realworld/`](examples/realworld/) (dead links, DNS failures, title bait on `example.com`, plus working RFC / Example Domain controls).

- Findings table (FACT counts): [`examples/realworld/REPORT.md`](examples/realworld/REPORT.md)
- Per-dump JSON + text: [`examples/realworld/out/`](examples/realworld/out/)
- Live demo page: https://larrylot.github.io/citeguard/

## Citation Failure Corpus

[`corpus/`](corpus/) — 20 short public-domain-style fake agent-research Markdown snippets with planted failures (`example.invalid`, title bait via `example.com` / `httpbin.org`). Documented for benchmarks. See [`corpus/README.md`](corpus/README.md).

## Docs / demo page

One-page JSON output demo: [`docs/index.html`](docs/index.html) (GitHub Pages: https://larrylot.github.io/citeguard/).

- [CiteGuard vs alternatives](docs/vs-alternatives.md) — honest comparison vs “ask ChatGPT”, LinkChecker, html-proofer, ReportBench (FACT / ASSUMPTION labeled)

## Docker

```bash
docker build -t citeguard .
docker run --rm -v "$PWD":/data -w /data citeguard check fixtures/mixed.md --fixtures
```

## Fixtures

`fixtures/` ships **9** Markdown reports + `*.expected.json` + HTML pages + `catalog.json` for offline resolve:

- clean cites, dead links, title mismatch, claim–source mismatch, redirect suspect, HTTP error, footnotes, mixed, bare URLs

```bash
pytest -q
# accuracy gate: ≥80% resolve+classify on fixtures
```

## Waitlist (hosted / batch API later)

Free form — **HUMAN SETUP** ≤10 min: see [`WAITLIST.md`](WAITLIST.md). Paste the public URL below when ready:

> Waitlist: `<!-- HUMAN: paste Tally or Google Form URL -->`

## Posts (human sends)

- [`SHOW_HN.md`](SHOW_HN.md) — Show HN draft
- [`POSTS.md`](POSTS.md) — Reddit / LinkedIn templates

Agent does **not** post or outreach.

## Status / kill

See [`STATUS.md`](STATUS.md). Kill if &lt;10 stars **and** &lt;10 waitlist after 7 days with ≥1 human public post, or fixture accuracy &lt;80%, or HN reads it as a chatbot wrapper.

## License

MIT — see [`LICENSE`](LICENSE).
