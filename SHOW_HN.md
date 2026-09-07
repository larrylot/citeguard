# Show HN draft (HUMAN posts — agent does not submit)

**Title (≤80 chars):**
Show HN: CiteGuard – local CLI that verifies citations in agent Markdown reports

**Text:**

I got tired of deep-research / agent Markdown dumps with dead links and SEO-farm “citations.”

CiteGuard is a tiny local Python CLI:

    citeguard check report.md

It extracts Markdown links + footnotes, resolves HTTP(S) (HEAD then GET), soft-matches link text against `<title>`, and optionally scores claim–source token overlap. No API keys for core checks. No telemetry. Offline `--fixtures` mode for CI.

Why not ask ChatGPT? I wanted something deterministic I can run in pytest — planted dead links / title bait / clean cites — without paying a model to shrug.

Repo: https://github.com/larrylot/citeguard

Demo:

    pip install -e .
    citeguard check fixtures/clean.md --fixtures
    citeguard check fixtures/dead_link.md --fixtures

Not a SaaS. If useful, there is a free waitlist for a later batch/CI badge — link in README after I paste the form URL.

Feedback welcome on false positives (title soft-match thresholds especially).

---

**Checklist before posting**
- [ ] `pytest` green locally
- [ ] README demo commands work
- [ ] Repo public on GitHub
- [ ] Waitlist URL pasted in README (or explicitly “coming today”)
- [ ] Do **not** mention merchant / pricing in first HN comment
