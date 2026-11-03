"""Frame bare device captures into the website's phone silhouette on white.

Replaces the old crop.py, whose input was an iOS *Simulator* window capture that
already drew its own bezel (plus a soft drop shadow that had to be masked away).
The app repo now captures bare screen content at device resolution
(app_store/screenshots/raw-ios/, 1320x2868) and draws the phone body itself in
compose.py, so the website does the same thing from the same source. One set of
captures now feeds both the store listings and this carousel.

Geometry is taken from app_store/screenshots/compose.py so the site's phones and
the store screenshots are visibly one system:
  - bezel / body width = 18/1081 (its iOS numbers), rounded here to BEZEL_FRAC
  - screen corner radius = 0.085 x screen width; body radius = screen r + bezel
  - side buttons at the same body-height fractions, protruding BUTTON_DEPTH_FRAC
Deliberately NOT taken from it: the drop shadow. Store art sits on a tinted
canvas; these sit on the page's white, where a baked shadow would fight the
background. Output is RGB on white, as crop.py's was.

Usage:  python3 assets/screenshots/frame.py
"""
from pathlib import Path

from PIL import Image, ImageDraw

RAW = Path(__file__).parent / "raw"
OUT = Path(__file__).parent / "cropped"
OUT.mkdir(exist_ok=True)

CANVAS_W = 800          # the width the carousel's <img> is authored against
BODY_W = 768            # phone body; leaves room for the buttons to protrude
MARGIN_Y = 6            # breathing room above/below the body

FRAME_COLOR = (24, 24, 27)
BEZEL_FRAC = 0.01665          # bezel thickness / body width  (compose.py: 18/1081)
SCREEN_RADIUS_FRAC = 0.085    # screen corner radius / screen width
BUTTON_DEPTH_FRAC = 0.0104    # protrusion / body width
BUTTON_RADIUS_FRAC = 0.0026
BUTTONS = [                   # (side, y_start, y_end) as fractions of body height
    ("left", 0.180, 0.213),   # Action
    ("left", 0.249, 0.327),   # Volume Up
    ("left", 0.339, 0.417),   # Volume Down
    ("right", 0.296, 0.425),  # Side
]
SUPERSAMPLE = 3               # PIL's rounded_rectangle has no antialiasing


def rounded(img, radius):
    mask = Image.new("L", img.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle(
        [0, 0, img.size[0] - 1, img.size[1] - 1], radius=radius, fill=255
    )
    img.putalpha(mask)
    return img


def body_layer(fw, fh, radius, depth, btn_r):
    """Phone body + protruding side buttons, drawn supersampled then downsampled."""
    s = SUPERSAMPLE
    w, h = fw + 2 * depth, fh
    img = Image.new("RGBA", (w * s, h * s), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    for side, y0f, y1f in BUTTONS:
        y0, y1 = fh * y0f, fh * y1f
        x0, x1 = (0, depth * 2) if side == "left" else (fw, fw + 2 * depth)
        d.rounded_rectangle([x0 * s, y0 * s, x1 * s, y1 * s],
                            radius=btn_r * s, fill=FRAME_COLOR + (255,))
    d.rounded_rectangle([depth * s, 0, (depth + fw) * s, h * s],
                        radius=radius * s, fill=FRAME_COLOR + (255,))
    return img.resize((w, h), Image.LANCZOS)


def main():
    srcs = sorted(RAW.glob("*.png"))
    if not srcs:
        raise SystemExit(f"no captures in {RAW}")

    bezel = round(BODY_W * BEZEL_FRAC)
    depth = max(2, round(BODY_W * BUTTON_DEPTH_FRAC))
    btn_r = max(1, round(BODY_W * BUTTON_RADIUS_FRAC))
    screen_w = BODY_W - 2 * bezel

    for src in srcs:
        shot = Image.open(src).convert("RGBA")
        screen_h = round(shot.height * screen_w / shot.width)
        shot = shot.resize((screen_w, screen_h), Image.LANCZOS)
        screen_r = round(screen_w * SCREEN_RADIUS_FRAC)
        shot = rounded(shot, screen_r)

        fh = screen_h + 2 * bezel
        canvas = Image.new("RGBA", (CANVAS_W, fh + 2 * MARGIN_Y), (255, 255, 255, 255))
        body = body_layer(BODY_W, fh, screen_r + bezel, depth, btn_r)
        bx = (CANVAS_W - (BODY_W + 2 * depth)) // 2
        canvas.alpha_composite(body, (bx, MARGIN_Y))
        canvas.alpha_composite(shot, (bx + depth + bezel, MARGIN_Y + bezel))

        dst = OUT / src.name
        canvas.convert("RGB").save(dst, "PNG", optimize=True)
        print(f"  {src.name}: {Image.open(src).size} -> {canvas.size} "
              f"({dst.stat().st_size // 1024} KB)")

    print(f"\n<img> attributes: width=\"{CANVAS_W}\" height=\"{canvas.size[1]}\"")


if __name__ == "__main__":
    main()
