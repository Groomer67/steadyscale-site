# Steady Scale — website

Public marketing site for [Steady Scale](https://steadyscale.app), a personal weight tracking app for iOS.

Hosted on GitHub Pages from this repo. `CNAME` routes the `steadyscale.app` apex.

## Pages

| File | Purpose |
|---|---|
| `index.html` | Landing — tour intro + 10-screen scroll-snap carousel of app screenshots + pricing section + "Your data" privacy posture |
| `how-it-works.html` | How it works — the method (daily averaging, the 14-day trend, plan target vs forecast, projection + uncertainty cone) |
| `science.html` | The science — research + statistical model behind the app, cited, with author bylines |
| `guide.html` | Quick guide — product + domain Q&A / help (`FAQPage` schema on the question-framed entries) |
| `about.html` | About — founder bios (a physicist + a kinesiologist), headshots + LinkedIn / Scholar |
| `news.html` | News — press + launches (OBJ press card + Peerlist / Product Hunt / App Store badges) |
| `support.html` | Contact page — email link + copy-to-clipboard button |
| `privacy.html` | Privacy Policy (generated from `legal/PrivacyPolicy.md` in the app repo) |
| `terms.html` | Terms of Service (generated from `legal/TermsOfService.md` in the app repo) |
| `licenses.html` | Open-source license acknowledgments |
| `favicon.svg`, `og-image.png` | Brand assets |
| `llms.txt`, `sitemap.xml`, `robots.txt`, `CNAME` | Hosting + SEO / AI config |

Top nav across every page: brand · Home · How it works · Science · Quick guide · News · About · Contact us.
Footer across every page: Privacy · Terms · Licenses · `© 2026 Steady Scale Inc., Canada`.

## Source of truth for copy

The shipped source of truth is the live HTML. Structured English copy records: the homepage **"A quick tour" carousel** → [`Strings.md`](Strings.md); the **content pages** (How it works, Science, Quick guide, About) → Markdown drafts in the **app repo** at `~/Code/SteadyScale/marketing/website/` (`how-it-works.md`, `science.md`, `guide.md`, `about.md`), which carry the copy + design rationale. Those pages are live, so edit the md draft and re-port to the HTML here on change (no Markdown→HTML builder for content pages yet). Legal pages (Privacy, Terms) are generated from the app repo's `legal/*.md` via `_scripts/build_legal.py`; other homepage sections + Support are authored directly in the HTML.

**Localization** (site is English-only today): see [`Strings.md`](Strings.md) → "Localization" for the translation plan — per-locale pages + `hreflang` + per-locale sitemap, generated from one template.

Legal copy lives in `legal/PrivacyPolicy.md` and `legal/TermsOfService.md` in the app repo (`~/Code/SteadyScale/`). To update them on the site, edit the markdown there, then re-run `_scripts/build_legal.py` from this repo root.

## Stack

Static HTML, hosted on GitHub Pages. Minimal vanilla JS:

- `index.html` ships a small block for the carousel (IntersectionObserver tracking the most-visible slide, native `scroll-snap-type: x mandatory`, arrow buttons + dot pagination + keyboard arrow keys).
- `support.html` ships a small block for the copy-to-clipboard button (`navigator.clipboard.writeText` with a selection fallback for older browsers).

Each page inlines its own CSS, scoped to a shared set of design tokens that mirror the app's `screens/DesignTokens.md` — colors, typography, radii, spacing. The site reads as the same product as the app.

No external dependencies. No analytics. No cookies.

## Assets

- `assets/screenshots/raw/` — source iOS Simulator captures (status bar reset to `9:41` via `xcrun simctl status_bar booted override --time "9:41"` before capture)
- `assets/screenshots/cropped/` — processed 800px-wide PNGs for the carousel
- `assets/screenshots/crop.py` — rounded-rect mask + button-protrusion processor that produces the cropped versions

To replace a screenshot: drop the new capture into `raw/`, then run `python3 assets/screenshots/crop.py` to regenerate the cropped version.

## Build script

- `_scripts/build_legal.py` — ports the legal markdown from the app repo into `privacy.html` + `terms.html`. Preserves the site template (nav, footer, design tokens) and converts the markdown body with `python-markdown` (extras: `extra`, `tables`, `sane_lists`). Run from this repo's root after editing either legal markdown file in the app repo.

## Local preview

```bash
python3 -m http.server 8000
```

Visit `http://localhost:8000`.

## Editing

Edit any HTML file directly. Push to `main` and GitHub Pages rebuilds within ~1 minute.

When updating shared values:

- Design tokens live in each page's `:root` block — keep them in sync.
- Nav and footer markup is duplicated across all ten HTML pages — update all of them.

## Contact

[support@steadyscale.app](mailto:support@steadyscale.app)

---

&copy; 2026 Steady Scale Inc.
