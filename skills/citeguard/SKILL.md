---
name: citeguard
description: >
  Verify citations in agent / deep-research Markdown reports with the local
  CiteGuard CLI (URL resolve, title soft-match, optional claim–source overlap).
  Use when the user asks to check citations, validate sources in a research
  dump, CI-check Markdown footnotes/links, or catch dead links / title bait /
  weak overlap — not when they only want an LLM opinion.
license: MIT
compatibility: Requires Python 3.10+ and the citeguard CLI (pip install -e . from https://github.com/larrylot/citeguard). Network optional; --fixtures works offline.
metadata:
  version: "0.1.0"
  homepage: "https://github.com/larrylot/citeguard"
  category: research-validation
---

# CiteGuard — verify citations in research Markdown

## When to use

Activate this skill when:

- An agent (or human) produced a **Markdown research report** with URLs, footnotes, or bare links
- The user asks to **check / verify / validate citations**, catch **hallucinated sources**, or gate CI on citation quality
- You need **reproducible, non-LLM** verdicts (dead links, title mismatch, weak claim overlap)

**Do not use** this skill to:

- “Ask another LLM if the citations look fine”
- Claim legal/scientific proof that a source supports a conclusion
- Replace a full plagiarism or fact-checking product

CiteGuard flags **dead links, title bait, weak overlap, and shady redirects** — failure modes common in agent research dumps.

## Install

From the CiteGuard repo (or a clone):

```bash
git clone https://github.com/larrylot/citeguard.git
cd citeguard
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
```

Docker (no local venv):

```bash
docker build -t citeguard .
docker run --rm -v "$PWD":/data -w /data citeguard check path/to/report.md --fixtures
```

Optional install into agent skill dirs (Cursor / Claude / Codex):

```bash
# Cursor project skill
mkdir -p .cursor/skills/citeguard
cp skill/SKILL.md .cursor/skills/citeguard/SKILL.md

# Or via skills CLI (discovers SKILL.md in the repo)
npx skills add larrylot/citeguard -s citeguard -y
```

## Procedure

### 1. Locate the Markdown report

Prefer the user’s file path. Typical names: `report.md`, `research.md`, agent dumps under `examples/` or `corpus/`.

### 2. Prefer offline fixtures when validating CiteGuard itself or CI

```bash
citeguard check fixtures/clean.md --fixtures
citeguard check fixtures/dead_link.md --fixtures   # expect exit 1
citeguard check fixtures/mixed.md --fixtures --json
```

### 3. Live-check a real report (needs network)

```bash
citeguard check path/to/agent-report.md
citeguard check path/to/agent-report.md --json
citeguard check path/to/agent-report.md --json --no-overlap
```

Flags:

| Flag | Meaning |
|------|---------|
| `--fixtures` | Offline resolve via `fixtures/catalog.json` (CI) |
| `--json` | Machine-readable verdicts (already supported) |
| `--no-overlap` | Skip claim–source token overlap |
| `--timeout N` | HTTP timeout seconds (default 12) |

### 4. Interpret verdicts

| Verdict | Meaning |
|---------|---------|
| `clean` | Resolved; title/claim checks passed |
| `dead` | 404 or network failure |
| `http_error` | Non-success HTTP (e.g. 500) |
| `title_mismatch` | Link text soft-match vs `<title>` too low |
| `claim_weak` | Claim sentence tokens barely appear in page text |
| `redirect_suspect` | Cross-host redirect without strong title match |
| `unresolved` | URL missing from fixtures catalog (fixtures mode only) |

Exit code **non-zero** when any citation fails (use in CI).

### 5. Report back to the user

Summarize counts (`clean` / `dead` / `title_mismatch` / …). For failures, list URL + line + verdict + short reason. Attach `--json` output when the user wants machine follow-up.

End with: *CiteGuard does not prove a source supports a legal/scientific conclusion — it flags resolve/title/overlap failure modes.*

## Example commands (copy-paste)

```bash
# Offline demo — clean planted report
citeguard check fixtures/clean.md --fixtures

# Offline — mixed failures + JSON
citeguard check fixtures/mixed.md --fixtures --json

# Live network check
citeguard check examples/realworld/01-agent-research-dump.md --json

# Pytest accuracy gate (≥80% on fixtures)
pytest -q
```

## Anti-patterns

- Replacing CiteGuard with “looks fine to me” LLM prose
- Inventing pass/fail without running the CLI
- Posting Show HN / awesome-list spam from the agent (human-only outreach)
- Treating `clean` as “the claim is true”

## Links

- Repo: https://github.com/larrylot/citeguard
- Live demo page: https://larrylot.github.io/citeguard/
- Vs alternatives: `docs/vs-alternatives.md`
