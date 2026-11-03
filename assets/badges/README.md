# Store badges — official assets, do not edit

Both files are the **official** badge art, used unmodified. They replaced
hand-drawn HTML/CSS recreations in November 2026, when the app shipped on both
stores and the pair had to sit side by side.

| File | Source | Intrinsic size |
|---|---|---|
| `app-store.svg` | Apple — `tools.applemediaservices.com/api/badges/download-on-the-app-store/black/en-us` | 119.66 × 40, artwork fills the box |
| `google-play.png` | Google — `play.google.com/intl/en_us/badges/static/images/badges/en_badge_web_generic.png` | 646 × 250, **artwork is 564 × 168** inside 41 px of transparent padding |

⚠️ **The two are not sized the same way.** Google bakes its required clear space
(~1/4 of badge height) into the file; Apple does not. Matching the files' heights
would render Google's button visibly smaller. Every place that shows both sizes
them so the *visible buttons* match:

- `index.html` — Apple `height: 44px`, Google `height: 65px` (65 × 168/250 ≈ 44)
- `assets/site.css` `.news-badge` — Apple `width: 128px`, Google `width: 165px` (165 × 250/646 × 168/250 ≈ 42.9, matching Apple's 128 × 40/119.66 ≈ 42.8), plus `margin: -10px` on the Play badge — all four sides, because the baked padding is symmetric — to cancel it from the **layout** box both horizontally (it would otherwise widen the date column) and vertically (it would otherwise sit ~10px lower under its date than every other badge). The padding stays on screen, so the clear space is intact; only the space the layout *reserves* goes. Without it the 165px box overflows the 140px date column, and because a flex item's automatic minimum size is its content, that column — and so that row's title and body text — grew wider than every other row's. `.news-date` carries `min-width: 0` for the same reason.

⚠️ **Match the visible HEIGHT, not the width.** The two badges are different shapes — Google's is the wider of the two — so equal widths leave the Play button visibly shorter. An earlier pass made exactly that mistake on `/news`.

Both guidelines also require clear space around the badge. Google's is in the
file; Apple's (10% of height) is covered by the surrounding flex gap and margins.

**Don't recolour, crop, stretch, add effects, or re-draw these.** If a badge must
change size, change the display size and keep the aspect ratio. Alt text is fixed
by the guidelines: "Download on the App Store" and "Get it on Google Play".
