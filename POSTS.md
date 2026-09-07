# Human post templates (agent does not send)

## Reddit — r/LocalLLaMA

**Title:** CiteGuard – local CLI to verify citations in agent / deep-research Markdown

**Body:**

If you run local agents that spit out research Markdown, you have probably seen dead links and “citations” that resolve to SEO junk.

CiteGuard is MIT, pip-installable, no API key for core checks:

- extract links + footnotes
- resolve URL (HEAD→GET)
- soft-match link text vs HTML title
- optional claim vs page-text token overlap
- `--fixtures` offline mode for CI

Repo: https://github.com/larrylot/citeguard

```bash
pip install -e .
citeguard check fixtures/mixed.md --fixtures
```

Happy to hear what false-positive patterns you hit on real agent reports.

---

## Reddit — r/ClaudeAI

**Title:** Tiny local tool: verify citations in Claude/deep-research Markdown exports

**Body:**

Built a small CLI (CiteGuard) that takes an agent Markdown report and returns per-citation verdicts — dead, title mismatch, weak claim overlap, clean — without sending the doc to another model.

Meant for people who paste research into PRs/docs and want a preflight check.

https://github.com/larrylot/citeguard

Offline fixtures included so CI does not hit the live web.

---

## LinkedIn (organic, one post)

Agent Markdown research is useful until the citations are dead or point at SEO farms.

I open-sourced CiteGuard — a local CLI:

`citeguard check report.md`

Resolve → title soft-match → optional claim/source overlap. No SaaS, no telemetry, MIT.

GitHub: https://github.com/larrylot/citeguard

If you want a later CI badge / batch API, the waitlist form is in the README (free).

#opensource #AI #research

---

## Notes
- Human posts only. No cold DMs. No paid boosts (0 SEK).
- Prefer Show HN first; Reddit same day or +1; LinkedIn last.
