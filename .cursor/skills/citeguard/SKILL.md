---
name: citeguard
description: >
  Validate URL health and basic citation hygiene in research Markdown using a
  local, deterministic CLI. Appropriate for Markdown report quality gates,
  broken-source checks, misleading titles, and weak lexical overlap.
license: MIT
compatibility: Python 3.10+ and the citeguard CLI. Offline fixtures are optional.
metadata:
  version: "0.2.0"
  homepage: "https://github.com/larrylot/citeguard"
  category: research-validation
---

# CiteGuard

Check the quality of citations already present in a Markdown research report. **Do not claim CiteGuard proves factual support or semantic entailment.** It does not identify uncited claims.

## Install

Install from GitHub (no PyPI release required):

```bash
python -m pip install "git+https://github.com/larrylot/citeguard.git"
citeguard --version
```

When working inside the repository:

```bash
python -m pip install -e ".[dev]"
pytest -q
```

## Procedure

1. Obtain the user-selected Markdown report path. Never invent a file path or pretend a check ran.
2. Run the real CLI using `citeguard check report.md --json`. This performs HTTP requests to cited sites, unless `--fixtures` is used.
3. Inspect the JSON `summary` and per-citation `url`, `line`, `claim`, `verdict`, and `reasons`.
4. Report both verified-looking and **unverifiable** sources. Treat all statuses except `clean` as requiring review by default.
5. Explain limitations: heuristic token overlap is **not** proof that the source supports the claim, and HTML/PDF support differs.

## Useful flags

| Flag | Purpose |
|---|---|
| `--json` | Machine-readable per-citation results |
| `--fixtures` | Offline catalog; for repository tests only |
| `--no-overlap` | Disable lexical claim matching |
| `--timeout N` | HTTP timeout in seconds |
| `--max-html-bytes N` | Limit HTML download size (default 2 MiB) |
| `--fail-on ...` | Customize verdicts that fail CI |
| `--allow-private` | **Dangerous:** allow private/internal URL targets, for trusted local documents only |

## Verdicts

| Verdict | Interpretation |
|---|---|
| `clean` | Available heuristics passed; **not semantic proof** |
| `dead` | 404/410 |
| `http_error` | Other HTTP error |
| `title_mismatch` | Label and HTML title disagree |
| `claim_weak` | Weak lexical overlap |
| `redirect_suspect` | Redirect to other host without good title match |
| `unverifiable` | Network, DNS, oversized body or redirect failure |
| `unchecked` | Source fetched but insufficient readable/checkable evidence |
| `unresolved` | Missing offline fixture |
| `blocked` | Dangerous or unsupported URL rejected |

Exit 0: clean citations; 1: flagged or no citations; 2: invalid input/arguments.

## Offline examples (from a checkout)

```bash
citeguard check fixtures/clean.md --fixtures
citeguard check fixtures/dead_link.md --fixtures --json
```

## Network safety

Do not expose the CLI as a network-facing multi-tenant fetch service without separate egress isolation. Per-target DNS validation is not a complete defense against DNS rebinding; see `SECURITY.md`.

## Links

- https://github.com/larrylot/citeguard
- https://larrylot.github.io/citeguard/
