# Website strings

**English copy record for [steadyscale.app](https://steadyscale.app).** The shipped source of truth is the live HTML in this repo. This file is the structured English-string record for the homepage **"A quick tour" carousel** — the natural unit to translate from. Keep it in sync when the carousel copy changes, and re-verify against the live HTML before any translation pass.

**Copy records for the rest of the site:**
- **Content pages** (How it works · Science · Quick guide · About) — Markdown drafts in the app repo at `~/Code/SteadyScale/marketing/website/` (`how-it-works.md`, `science.md`, `guide.md`, `about.md`); those carry the copy *and* the design rationale.
- **Legal pages** (Privacy · Terms) — generated from `legal/PrivacyPolicy.md` / `legal/TermsOfService.md` (app repo) via `_scripts/build_legal.py`.
- **Other homepage sections + Support** — authored directly in the HTML.

## Localization (future — English-only today)

When we translate the site (see `marketing/Visibility.md` "languages phase"):
- **English source** = the live HTML per page, with this file + the `marketing/website/` drafts as the structured records to extract from.
- **Approach** = per-locale copy → per-locale pages (e.g. `/es/…`, `/fr/…`), each with a correct `<html lang>` (already `en` today), `hreflang` alternates in `<head>`, `og:locale` + JSON-LD `inLanguage`, and per-locale `sitemap.xml` entries. The Markdown→HTML "article builder" queued in `marketing/Visibility.md` is the natural vehicle — generate every locale from one template so nav / footer / structured data stay consistent.
- The **app's own strings localize separately** (ARB generated from the app repo `Strings/`); keep website and app translations consistent in terminology (trend, check-in, monitor, plan).

---

## Tour heading

**Eyebrow** — A quick tour
**Title** — See every screen
**Subtitle** — Swipe, click, or use the arrow keys to explore the app.

---

## Carousel slides

Ten slides, in order. Each has: eyebrow · headline · body · image alt text · dot label. (Headlines carry no terminal period — the site-wide heading rule.)

### 1 · Welcome

- **Eyebrow** — Welcome
- **Headline** — A short setup
- **Body** — Onboarding takes about a minute. Pick how you want to track, choose a goal or reference weight, and set your weekly check-in day.
- **Image alt** — Welcome screen with a small trend chart and the subtitle: Simple tracking that turns daily ups and downs into something you can trust.
- **Dot label** — Welcome
- **Screenshot** — `assets/screenshots/cropped/01-welcome.png`

### 2 · Tracking mode

- **Eyebrow** — Tracking mode
- **Headline** — Loss, Gain, or Monitor
- **Body** — Pick the one that fits. The weekly trend works the same for all three — and you can switch any time without losing your history.
- **Image alt** — Tracking mode selection: Lose weight, Gain weight, or Monitor weight.
- **Dot label** — Tracking mode
- **Screenshot** — `assets/screenshots/cropped/02-tracking-mode.png`

### 3 · Goal weight

- **Eyebrow** — Goal weight
- **Headline** — A goal you could maintain
- **Body** — Pick a weight you could see yourself maintaining, not just reaching. BMI is shown as a reference, not a prescription.
- **Image alt** — Goal weight picker with a BMI bar and an expandable card titled What makes a good goal weight.
- **Dot label** — Goal weight
- **Screenshot** — `assets/screenshots/cropped/03-goal-weight.png`

### 4 · Weekly rate

- **Eyebrow** — Weekly rate
- **Headline** — Pick a pace
- **Body** — Choose any rate from 0.5 to 2.0 lb per week. Your rate sets a weekly target that stays constant throughout the week and updates after each check-in day.
- **Image alt** — Weekly rate picker with four presets (0.5, 1.0, 1.5, 2.0 lb per week) and a day-of-week check-in selector.
- **Dot label** — Weekly rate
- **Screenshot** — `assets/screenshots/cropped/04-weekly-rate.png`

### 5 · Free trial

- **Eyebrow** — Free trial
- **Headline** — Free for 7 days
- **Body** — No accounts, no servers, no ads. Your data stays on your device and backs up to your iCloud. Cancel any time in iOS Settings.
- **Image alt** — Completion screen with a checkmark, You're all set heading, and a Start 7-Day Free Trial button.
- **Dot label** — Free trial
- **Screenshot** — `assets/screenshots/cropped/05-completion.png`

### 6 · Dashboard

- **Eyebrow** — Dashboard
- **Headline** — Long term, this week, today
- **Body** — Three cards show three time horizons: where you're heading, how this week's pace compares to plan, and today's daily average.
- **Image alt** — Dashboard with three cards: Goal arrival date, This Week pace, and Today's daily average.
- **Dot label** — Dashboard
- **Screenshot** — `assets/screenshots/cropped/06-dashboard.png`

### 7 · Chart

- **Eyebrow** — Chart
- **Headline** — Noise into signal
- **Body** — The chart layers raw weigh-ins, daily averages, and a 14-day rolling trend that filters out day-to-day noise. From your trend and chosen rate, it projects forward to your goal — so you can see when you'll get there.
- **Image alt** — Chart screen showing daily measurements, a smoothed trend line, a goal projection, and check-in markers.
- **Dot label** — Chart
- **Screenshot** — `assets/screenshots/cropped/07-chart.png`

### 8 · Log

- **Eyebrow** — Log
- **Headline** — Log as often as you like
- **Body** — Weigh in once a day or multiple times a day — whatever works for you. You can edit or backfill measurements any time, and unlikely entries get flagged so a typo doesn't throw off your trend.
- **Image alt** — Log screen with a weight input field, date and time rows, and a list of recent measurements.
- **Dot label** — Log
- **Screenshot** — `assets/screenshots/cropped/08-log.png`

### 9 · Settings

- **Eyebrow** — Settings
- **Headline** — Plan, preferences, and backup
- **Body** — Your active plan lives in one card: edit, pause, or delete from there. Switching between Loss, Gain, and Monitor preserves your history, and deleted plans can be restored from Past plans.
- **Image alt** — Settings screen with Profile, Plan card showing goal, rate, and check-in day, plus Edit, Pause, and Delete actions.
- **Dot label** — Settings
- **Screenshot** — `assets/screenshots/cropped/09-settings.png`

### 10 · Help

- **Eyebrow** — Help
- **Headline** — Every element explained
- **Body** — The Help tab covers how the math works, how to read the chart, how your data is handled, and how to get in touch. Every part of the system is open.
- **Image alt** — Help screen with How it works, Reading the chart, Choosing a goal weight, and other expandable sections.
- **Dot label** — Help
- **Screenshot** — `assets/screenshots/cropped/10-help.png`
