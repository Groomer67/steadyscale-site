"""Port legal markdown documents to styled HTML pages on the site.

Sources:  /Users/ryangroome/Code/SteadyScale/legal/{PrivacyPolicy,TermsOfService}.md
Targets:  /Users/ryangroome/Desktop/Code/steadyscale-site/{privacy,terms}.html

Re-run any time the markdown is updated. The script preserves the existing site
template (head meta, nav, footer, design tokens) and converts the markdown body
to HTML using python-markdown with the tables + extra extensions.
"""
import re
from pathlib import Path
import markdown

LEGAL = Path("/Users/ryangroome/Code/SteadyScale/legal")
SITE = Path("/Users/ryangroome/Desktop/Code/steadyscale-site")


TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<meta property="og:title" content="{title}">
<meta property="og:description" content="{og_desc}">
<meta property="og:type" content="website">
<meta property="og:url" content="https://steadyscale.app/{slug}">
<meta property="og:site_name" content="Steady Scale">
<meta property="og:image" content="https://steadyscale.app/og-image.png">
<meta property="og:image:alt" content="Steady Scale — chart showing noisy daily measurements smoothed into a clear trend line.">

<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{og_desc}">
<meta name="twitter:image" content="https://steadyscale.app/og-image.png">

<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<meta name="description" content="{meta_desc}">
<title>{title}</title>
<meta name="theme-color" content="#2781DB">
<link rel="canonical" href="https://steadyscale.app/{slug}">

<style>
:root {{
  --bg: #FFFFFF;
  --surface: #F5F5F5;
  --surface-tint: #EBF4FF;
  --celebration-border: rgba(39, 129, 219, 0.18);
  --border: #E0E0E0;
  --border-soft: #ECECEC;
  --text: #2C2C2C;
  --secondary: #555555;
  --muted: #999999;
  --blue: #2781DB;
  --nav-h: 56px;
}}
*, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
html {{ scroll-behavior: smooth; }}
body {{
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', 'SF Pro Display', 'Helvetica Neue', Arial, sans-serif;
  color: var(--text);
  background: var(--bg);
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  line-height: 1.65;
  padding-top: var(--nav-h);
}}
a {{ color: var(--blue); text-decoration: none; }}
a:hover {{ text-decoration: underline; }}

.skip {{ position: absolute; top: -40px; left: 8px; background: var(--text); color: #FFF; padding: 8px 14px; border-radius: 6px; font-size: 13px; z-index: 100; transition: top 0.15s; }}
.skip:focus {{ top: 8px; }}

.nav {{ position: fixed; top: 0; left: 0; right: 0; height: var(--nav-h); background: rgba(255,255,255,0.85); backdrop-filter: saturate(180%) blur(14px); -webkit-backdrop-filter: saturate(180%) blur(14px); border-bottom: 1px solid rgba(0,0,0,0.06); z-index: 50; }}
.nav-inner {{ max-width: 1080px; margin: 0 auto; height: 100%; padding: 0 24px; display: flex; align-items: center; justify-content: space-between; }}
.nav-brand {{ display: inline-flex; align-items: center; gap: 8px; text-decoration: none; }}
.nav-brand:hover {{ text-decoration: none; }}
.nav-brand svg {{ width: 22px; height: 22px; }}
.nav-wm {{ font-size: 17px; letter-spacing: -0.4px; text-transform: lowercase; }}
.nav-wm .w-steady {{ font-weight: 700; color: var(--blue); }}
.nav-wm .w-scale  {{ font-weight: 400; color: var(--text); margin-left: 0.15em; }}
.nav-links {{ display: flex; align-items: center; gap: 28px; }}
.nav-links a {{ font-size: 13px; font-weight: 500; color: var(--secondary); text-decoration: none; }}
.nav-links a:hover {{ color: var(--blue); text-decoration: none; }}

.container {{ max-width: 720px; margin: 0 auto; padding: 56px 24px 64px; }}

/* Legal document typography */
.legal-doc h1 {{ font-size: 36px; font-weight: 700; letter-spacing: -0.5px; margin-bottom: 8px; color: var(--text); }}
.legal-doc .doc-meta {{ font-size: 13px; color: var(--muted); margin-bottom: 28px; }}
.legal-doc .doc-meta strong {{ color: var(--secondary); font-weight: 600; }}
.legal-doc h2 {{ font-size: 22px; font-weight: 700; letter-spacing: -0.25px; margin-top: 44px; margin-bottom: 14px; color: var(--text); line-height: 1.25; }}
.legal-doc h3 {{ font-size: 17px; font-weight: 600; margin-top: 28px; margin-bottom: 10px; color: var(--text); line-height: 1.3; }}
.legal-doc h4 {{ font-size: 15px; font-weight: 700; margin-top: 20px; margin-bottom: 8px; color: var(--text); }}
.legal-doc p {{ font-size: 15px; color: var(--secondary); margin-bottom: 14px; line-height: 1.65; }}
.legal-doc ul, .legal-doc ol {{ margin-left: 22px; margin-bottom: 14px; }}
.legal-doc li {{ font-size: 15px; color: var(--secondary); margin-bottom: 6px; line-height: 1.6; }}
.legal-doc li > ul, .legal-doc li > ol {{ margin-top: 6px; margin-bottom: 6px; }}
.legal-doc strong {{ color: var(--text); font-weight: 600; }}
.legal-doc em {{ color: var(--text); font-style: italic; }}
.legal-doc hr {{ border: 0; border-top: 1px solid var(--border-soft); margin: 40px 0; }}
.legal-doc blockquote {{
  border-left: 3px solid var(--border);
  padding: 6px 0 6px 20px;
  margin: 16px 0;
  color: var(--secondary);
  font-size: 14.5px;
  line-height: 1.7;
}}
.legal-doc blockquote p {{ margin-bottom: 4px; font-size: 14.5px; }}
.legal-doc table {{
  width: 100%;
  border-collapse: collapse;
  margin: 20px 0;
  font-size: 14px;
  border: 1px solid var(--border);
  border-radius: 8px;
  overflow: hidden;
}}
.legal-doc th {{
  text-align: left;
  font-weight: 700;
  color: var(--text);
  padding: 10px 12px;
  border-bottom: 2px solid var(--border);
  background: var(--surface);
  font-size: 13px;
  letter-spacing: 0.01em;
}}
.legal-doc td {{
  padding: 10px 12px;
  border-bottom: 1px solid var(--border-soft);
  color: var(--secondary);
  vertical-align: top;
  line-height: 1.55;
}}
.legal-doc tbody tr:last-child td {{ border-bottom: none; }}
.legal-doc a {{ color: var(--blue); }}
.legal-doc .doc-footer {{
  margin-top: 48px;
  padding-top: 24px;
  border-top: 1px solid var(--border-soft);
  font-size: 12px;
  color: var(--muted);
  text-align: center;
  font-style: italic;
}}

.footer {{ padding: 56px 24px 40px; text-align: center; border-top: 1px solid var(--border-soft); }}
.footer-nav {{ display: flex; justify-content: center; gap: 6px 22px; flex-wrap: wrap; margin-bottom: 20px; }}
.footer-nav a {{ font-size: 13px; color: var(--secondary); text-decoration: none; transition: color 0.15s; }}
.footer-nav a:hover {{ color: var(--blue); }}
.footer-meta {{ font-size: 12px; color: var(--muted); line-height: 1.6; }}

@media (max-width: 640px) {{
  .container {{ padding: 40px 20px 48px; }}
  .legal-doc h1 {{ font-size: 28px; }}
  .legal-doc h2 {{ font-size: 19px; margin-top: 36px; }}
  .legal-doc h3 {{ font-size: 16px; }}
  .legal-doc table {{ font-size: 13px; }}
  .legal-doc th, .legal-doc td {{ padding: 8px 10px; }}
  .nav-links {{ gap: 18px; }}
  .nav-links a {{ font-size: 12px; }}
}}
</style>
</head>
<body>

<a href="#main" class="skip">Skip to content</a>

<header class="nav" role="banner">
  <div class="nav-inner">
    <a href="/" class="nav-brand" aria-label="Steady Scale home">
      <svg viewBox="0 0 64 64" fill="none" role="img" aria-hidden="true">
        <path d="M 9 18 C 22 17, 30 46, 53 46" stroke="#2781DB" stroke-width="4" stroke-linecap="round"/>
        <circle cx="53" cy="46" r="6" fill="#2781DB"/>
      </svg>
      <span class="nav-wm"><span class="w-steady">steady</span><span class="w-scale">scale</span></span>
    </a>
    <nav class="nav-links" aria-label="Primary">
      <a href="/">Home</a>
      <a href="/support.html">Support</a>
    </nav>
  </div>
</header>

<main id="main" class="container legal-doc">
{body}
</main>

<footer class="footer" role="contentinfo">
  <nav class="footer-nav" aria-label="Secondary">
    <a href="/privacy.html">Privacy Policy</a>
    <a href="/terms.html">Terms of Service</a>
    <a href="/licenses.html">Open-source licenses</a>
  </nav>
  <div class="footer-meta">
    &copy; 2026 Steady Scale Inc., Canada
  </div>
</footer>

</body>
</html>
"""


def convert(md_path: Path, html_path: Path, slug: str, title: str,
            meta_desc: str, og_desc: str) -> None:
    md_text = md_path.read_text()

    # Pull out the H1 + meta block (Effective date / Last updated) so we can
    # render them as styled .doc-meta rather than inline paragraphs.
    h1_match = re.search(r'^# (.+)$', md_text, re.MULTILINE)
    h1_text = h1_match.group(1).strip() if h1_match else 'Document'

    # The "**Effective date:** ... **Last updated:** ..." lines come right
    # after the H1. Strip them from the body and render as styled meta.
    meta_block = ''
    eff_match = re.search(r'\*\*Effective date:\*\* ([^\n]+)', md_text)
    upd_match = re.search(r'\*\*Last updated:\*\* ([^\n]+)', md_text)
    if eff_match and upd_match:
        meta_block = (
            f'<div class="doc-meta">'
            f'<strong>Effective date:</strong> {eff_match.group(1)} &middot; '
            f'<strong>Last updated:</strong> {upd_match.group(1)}'
            f'</div>'
        )

    # Drop the H1 + the two meta lines from the markdown body — we render those manually.
    body_md = re.sub(r'^# .+\n', '', md_text, count=1, flags=re.MULTILINE)
    body_md = re.sub(r'^\*\*Effective date:\*\*[^\n]+\n', '', body_md,
                     count=1, flags=re.MULTILINE)
    body_md = re.sub(r'^\*\*Last updated:\*\*[^\n]+\n', '', body_md,
                     count=1, flags=re.MULTILINE)

    # Convert markdown body to HTML with tables + extra (handles blockquotes, fenced code, etc).
    html_body = markdown.markdown(
        body_md,
        extensions=['extra', 'tables', 'sane_lists'],
    )

    # Cross-link the two legal docs to each other.
    html_body = html_body.replace('./PrivacyPolicy.md', '/privacy.html')
    html_body = html_body.replace('./TermsOfService.md', '/terms.html')

    # Preserve line breaks inside blockquotes (addresses) — markdown collapses
    # single newlines to spaces, which mashes multi-line addresses into one line.
    def fix_blockquote(match):
        inner = match.group(1)
        # Inside the blockquote, replace newlines within <p> tags with <br>.
        inner = re.sub(
            r'<p>(.*?)</p>',
            lambda m: '<p>' + m.group(1).replace('\n', '<br>\n') + '</p>',
            inner,
            flags=re.DOTALL,
        )
        return f'<blockquote>{inner}</blockquote>'
    html_body = re.sub(
        r'<blockquote>(.*?)</blockquote>',
        fix_blockquote,
        html_body,
        flags=re.DOTALL,
    )

    # Wrap the trailing copyright (italic line at the bottom of the markdown)
    # in a .doc-footer div for nicer styling. The markdown renders it as:
    #   <p><em>© 2026 Steady Scale Inc. All rights reserved.</em></p>
    html_body = re.sub(
        r'<p><em>(© 2026 Steady Scale Inc\. All rights reserved\.)</em></p>',
        r'<div class="doc-footer">\1</div>',
        html_body,
    )

    # Assemble: H1 + meta block + body
    full_body = f'<h1>{h1_text}</h1>\n{meta_block}\n{html_body}'

    page = TEMPLATE.format(
        title=title,
        slug=slug,
        meta_desc=meta_desc,
        og_desc=og_desc,
        body=full_body,
    )
    html_path.write_text(page)
    print(f"  ✓ {html_path.name}  ({len(page):,} bytes)")


def main() -> None:
    convert(
        md_path=LEGAL / "PrivacyPolicy.md",
        html_path=SITE / "privacy.html",
        slug="privacy",
        title="Privacy Policy — Steady Scale",
        meta_desc="How Steady Scale collects, uses, and protects information. Local-first storage, no accounts, no servers we operate, no advertising.",
        og_desc="How Steady Scale collects, uses, and protects information. Local-first storage, no accounts, no servers, no advertising.",
    )
    convert(
        md_path=LEGAL / "TermsOfService.md",
        html_path=SITE / "terms.html",
        slug="terms",
        title="Terms of Service — Steady Scale",
        meta_desc="Terms of Service for the Steady Scale iOS app and steadyscale.app website. Subscription, trial, refunds, disclaimers, and governing law.",
        og_desc="Terms of Service for Steady Scale. Subscription, trial, disclaimers, and governing law.",
    )


if __name__ == "__main__":
    main()
