# Changelog

## 0.2.0 — 2026-10-15

### Improved
- Parse CommonMark links, including reference-style citations, and avoid URLs from fenced and inline code.
- Check **every** occurrence of a citation, rather than silently collapsing repeated source URLs.
- Reuse HTTP fetch results per URL while evaluating each nearby claim independently.
- Treat unknown fixtures, network failures, non-HTML pages, and content without enough evidence as non-clean verdicts.
- Reject private and non-global IPs and unsafe redirects by default; cap HTML response sizes.
- Add regression tests for duplicate citations, offline failure handling, SSRF-related cases, and unsupported formats.
- Document safety boundaries and the limited meaning of `clean`.

### Breaking changes
- The default CI gate fails on all verdicts other than `clean`, including `unchecked`, `unverifiable`, `unresolved`, and `blocked`.
- Timeout / DNS failures are no longer described as proven dead links.
- A report containing zero citations no longer passes.
- A `--allow-private` opt-in is required for checking private/internal URLs.
- The package adds `markdown-it-py` as a dependency.

No claim of semantic or factual source verification is made.

## 0.1.0 — 2026-09-07

Initial research Markdown CLI, synthetic offline fixture corpus, and GitHub Pages demo.
