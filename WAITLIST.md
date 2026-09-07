# Waitlist setup for Lars (≤10 min, 0 SEK)

Goal: capture emails for a **later** hosted batch API / CI badge. Core CLI stays free/local. No merchant required.

## Option A — Tally (recommended)

1. Go to https://tally.so and sign in (free).
2. New form → title: **CiteGuard waitlist**
3. Fields:
   - Email (required)
   - “How do you generate research Markdown?” (short text, optional)
   - “What would you pay for a CI badge / batch API?” (multiple choice optional: “nothing / $5–10/mo / $20+/mo / not sure”)
4. Thank-you message: “Thanks — CiteGuard CLI stays free. We will email only about the batch/CI waitlist.”
5. Publish → copy public form URL.
6. Paste URL into `README.md` replacing `<!-- HUMAN: paste Tally or Google Form URL -->`.
7. Optional: embed snippet is unnecessary for v0; link is enough.

Tally free = unlimited forms/submissions within fair use (verify on tally.so if their plan page changed).

## Option B — Google Form

1. forms.google.com → blank form → **CiteGuard waitlist**
2. Same three fields as above.
3. Responses → link to Sheets.
4. Send → copy link → paste into README.

## Do / Don’t

- DO: one form, one URL in README + Show HN.
- DON’T: promise ship dates, charge cards, or add newsletter spam.
- DON’T: agent-create the form if your Google/Tally session is not available in-browser — human paste is fine.

## Tracking

Log waitlist count weekly in `STATUS.md` signal table.
