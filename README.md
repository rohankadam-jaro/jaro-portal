# Jaro Education Analytics Portal

Static portal (Vercel, `public/` is the output dir) linking every university dashboard.

- `public/index.html` – university dashboard hub
- `public/feedback.html` – combined student feedback for all universities (university/company/rating/domain filters, Symbiosis videos, reviews)
- `public/feedback.json`, `public/videos.json` – generated data
- `scripts/build_feedback.py` – regenerates the JSON from each university's `public/td.json` (re-run after any university's feedback changes)
- `scripts/make_page.py` – one-off generator for `feedback.html` (edit the HTML directly from now on)
- `middleware.js` – optional IP allow-list via `ALLOWED_IPS`

Feedback data contains student names: keep this repository **private**.
