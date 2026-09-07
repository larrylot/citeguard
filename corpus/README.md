# Citation Failure Corpus

Short **public-domain-style** fake “agent / deep-research” Markdown snippets with **planted citation failures** for CiteGuard benchmarks and demos.

These are **not** real research. Links intentionally use:

- `example.invalid` — dead / network-fail / SEO-farm plants (never resolves in the real DNS reserved zone)
- `example.com` / `www.example.com` — live placeholder pages used as **title-mismatch** bait (IANA Example Domain ≠ claimed product docs)
- `httpbin.org` — careful live endpoints (`/html`, `/json`, `/robots.txt`, `/status/500`) whose real titles/bodies **do not** match the agent’s claimed link text

## Layout

| File | Planted failure modes |
|------|------------------------|
| `01_dead_arxiv_clone.md` | dead |
| `02_title_bait_httpbin.md` | title_mismatch (httpbin `/html`) |
| `03_dead_policy_page.md` | dead |
| `04_example_com_as_docs.md` | title_mismatch (example.com) |
| `05_mixed_dead_and_clean.md` | clean + dead |
| `06_httpbin_500.md` | http_error |
| `07_seo_farm_asyncio.md` | title_mismatch (fixtures SEO plant) |
| `08_footnote_dead.md` | dead (footnote) |
| `09_bare_url_dead.md` | dead (bare URL) |
| `10_redirect_suspect.md` | redirect_suspect |
| `11_claim_weak_climate.md` | claim_weak |
| `12_httpbin_json_as_paper.md` | title_mismatch / claim_weak |
| `13_two_dead_links.md` | dead ×2 |
| `14_example_com_user_guide.md` | title_mismatch |
| `15_clean_python_docs.md` | clean control |
| `16_github_actions_plus_dead.md` | clean + dead |
| `17_httpbin_robots_as_policy.md` | title_mismatch |
| `18_pep8_plus_title_bait.md` | clean + title_mismatch |
| `19_fastapi_plus_network_fail.md` | clean + dead/network |
| `20_multi_failure_stew.md` | clean + dead + title_mismatch + http_error |

## How to use

```bash
# Offline (uses fixtures/catalog.json for known URLs):
citeguard check corpus/05_mixed_dead_and_clean.md --fixtures --json

# Live network (will hit example.com / httpbin; example.invalid fails):
citeguard check corpus/20_multi_failure_stew.md --json
```

Pair with the richer planted set under `../fixtures/` (expected JSON + HTML pages) for CI accuracy gates.

## License

Corpus text is CC0-style / public-domain dedication for benchmark reuse. Linked third-party sites remain their owners’.
