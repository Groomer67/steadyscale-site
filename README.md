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

- `assets/screenshots/raw/` — bare device captures, copied from the app repo's `app_store/screenshots/raw-ios/` (1320×2868). **The same captures the App Store listing is composed from**, so the carousel and the store art can never show different builds.
- `assets/screenshots/cropped/` — processed 800×1650 PNGs for the carousel
- `assets/screenshots/frame.py` — draws the phone body (rounded screen, bezel, side buttons) around each capture on white. Geometry is lifted from the app repo's `app_store/screenshots/compose.py` so the site's phones and the store screenshots read as one system; the store art's drop shadow is deliberately omitted, since these sit on the page's white.

To replace the screenshots: re-capture in the app repo (`app_store/screenshots/README.md` has the procedure — canonical dataset, frozen `DevClock`, status-bar recipe), copy `raw-ios/*.png` into `raw/`, then run `python3 assets/screenshots/frame.py`. If the capture device changes, the output height changes with it — the script prints the `width`/`height` to put on the carousel's `<img>` tags.

*(Until November 2026 this was `crop.py`, which masked a phone silhouette out of an iOS **Simulator** window capture that drew its own bezel. The app repo now captures bare screen content at device resolution, so the site draws the body itself.)*

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
