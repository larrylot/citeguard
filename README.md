# CiteGuard

[![CI](https://github.com/larrylot/citeguard/actions/workflows/ci.yml/badge.svg)](https://github.com/larrylot/citeguard/actions/workflows/ci.yml)

**CiteGuard is a local, explainable citation hygiene checker for Markdown research reports.**

It detects dead URLs, HTTP failures, misleading link titles, cross-host redirects, and weak word overlap between an assertion and the linked HTML page. It checks each **citation occurrence** separately, even if the same URL is reused for different claims. Repeated URLs are downloaded once per report.

CiteGuard **does not prove that a claim is true or entailed by its source**. Its overlap heuristic cannot identify contradictions, fabricated arguments, or missing references. A `clean` verdict means only that the checks **performed by CiteGuard** passed.

- No account or API key, no AI model, no tracking or telemetry
- Python 3.10+; supports offline fixture tests
- JSON output and predictable process exit codes for CI
- HTML inspection only: PDFs and non-HTML responses are explicitly `unchecked`
- Restrictive default treatment of private/internal URLs, redirects, and oversized HTML

## Install

CiteGuard 0.2 can be installed from this repository without waiting for PyPI:

```bash
# Requires Python 3.10+
python -m pip install "git+https://github.com/larrylot/citeguard.git"
citeguard --version
```

For an isolated CLI installation, use `pipx install git+https://github.com/larrylot/citeguard.git` instead. If testing an unmerged branch, append `@fix/citeguard-robustness-20261015` to the Git URL.

From a checkout:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
pytest -q
```

## Use

```bash
citeguard check report.md
citeguard check report.md --json > citation-results.json
citeguard check report.md --no-overlap
```

For a deterministic, network-free demo from a **repository checkout**:

```bash
citeguard check fixtures/clean.md --fixtures
citeguard check fixtures/dead_link.md --fixtures  # exit 1, expected
citeguard check fixtures/mixed.md --fixtures --json
```

`--fixtures` uses a local `fixtures/catalog.json`. A URL missing from the catalog returns `unresolved` and fails by default, instead of silently passing.

### Verdicts

| Verdict | Meaning | Default exit failure |
|---|---|---|
| `clean` | Available title/claim heuristics passed. **Not proof of factual support.** | No |
| `dead` | Source returned 404 or 410 | Yes |
| `http_error` | Other HTTP failure (403/429/500 etc.) | Yes |
| `title_mismatch` | Descriptive citation label does not resemble page title | Yes |
| `claim_weak` | Claim words poorly overlap readable HTML | Yes |
| `redirect_suspect` | Cross-host redirect without strong title match | Yes |
| `unresolved` | Citation absent from offline fixture catalog | Yes |
| `unverifiable` | Network/DNS failure, oversized response, redirect exhaustion | Yes |
| `unchecked` | Cannot inspect a readable HTML source or meaningful title/claim | Yes |
| `blocked` | URL scheme, credentials, or private destination disallowed | Yes |

A report with zero detectable citations also exits with code 1 (nothing was checked).

**Exit codes:** `0` = all citations passed, `1` = at least one configured failure (or no citations), `2` = input/CLI error. Override the gate using `--fail-on dead,http_error,blocked` if some unverified statuses are acceptable for your workflow.

### Safe network defaults

```bash
citeguard check report.md --timeout 10 --max-html-bytes 1048576
# For trusted internal reports ONLY:
citeguard check internal-report.md --allow-private
```

The network checker validates each redirect destination, rejects loopback/private and non-global IPs by default, ignores environment proxy settings, and limits HTML reads to 2 MiB per URL. These are **defense-in-depth protections, not a complete SSRF sandbox**: DNS rebinding and other egress risks remain. Do not run a publicly exposed multi-tenant service without enforced network-level egress restrictions. Read [SECURITY.md](SECURITY.md).

## Use in GitHub Actions

```yaml
- uses: actions/checkout@v4
- uses: actions/setup-python@v6
  with:
    python-version: "3.12"
- run: python -m pip install "git+https://github.com/larrylot/citeguard.git"
- run: citeguard check reports/research.md --json
```

For repeatable CI runs pin installation to a release tag or commit SHA once published.

## Agent skill

The optional [portable agent skill](skill/SKILL.md) documents a verify-after-research workflow:

```bash
npx skills add larrylot/citeguard -s citeguard -y
```

The skill is an instruction file, not an automated citation assertion engine. Mirrored versions are in [`.cursor/skills/`](.cursor/skills/citeguard/SKILL.md) and [`skills/`](skills/citeguard/SKILL.md).

## Examples and limitations

- [Failure corpus](corpus/README.md) provides 20 planted examples for testing.
- [Synthetic live-network samples](examples/realworld/REPORT.md) demonstrate the types of failures found, **not ground-truth accuracy on real user reports**.
- [Alternatives](docs/vs-alternatives.md) outlines when conventional link checkers, semantic evaluators, or manual review are better fits.
- [Demo page](https://larrylot.github.io/citeguard/) shows example output.
- `fixtures/` contains offline golden tests; run `pytest -q`.

Known limits: HTML only, heuristics for English-oriented titles and token overlap, approximate sentence extraction, no semantic entailment, and no search for missing sources. In particular, `clean` does **not** imply factual correctness.

## Development

Issues and patches are welcome: [GitHub Issues](https://github.com/larrylot/citeguard/issues). Local tests and GitHub CI use Python 3.10, 3.12, and 3.13. Read [CHANGELOG.md](CHANGELOG.md) for compatibility notes.

**License:** [MIT](LICENSE). No hosted product or public API is offered.
