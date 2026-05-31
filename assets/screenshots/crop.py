"""Crop iOS Simulator screenshots and composite onto white via a clean rounded-rect mask.

The mask is a mathematical rounded rectangle (phone body) plus protruding rectangles
for the physical buttons. This eliminates the simulator's soft-shadow stippling that
the prior floodfill approach left as dotted noise outside the bezel curve.

Phone geometry (in cropped coordinates, after applying CROP to the 1032×1936 source):
  - Body bbox: (17, 6, 785, 1585), corner radius 124 — measured empirically
  - Left side buttons (Action, Volume Up, Volume Down): 3 rectangles
  - Right side button (Side): 1 rectangle

The mask is drawn at 3× supersampling and LANCZOS-downsampled for smooth antialiasing.
"""
from PIL import Image, ImageDraw
from pathlib import Path

RAW = Path(__file__).parent / "raw"
OUT = Path(__file__).parent / "cropped"
OUT.mkdir(exist_ok=True)

CROP = (115, 198, 917, 1790)
TARGET_W = 800

PHONE_BBOX = (17, 6, 785, 1585)
CORNER_RADIUS = 124

LEFT_BUTTONS = [
    (9, 291, 17, 343),    # Action
    (9, 399, 17, 523),    # Volume Up
    (9, 541, 17, 664),    # Volume Down
]
RIGHT_BUTTONS = [
    (785, 473, 793, 677),  # Side
]
BUTTON_RADIUS = 2

SUPERSAMPLE = 3


def build_mask(size: tuple[int, int]) -> Image.Image:
    """Build a supersampled mask of the phone silhouette."""
    s = SUPERSAMPLE
    big = (size[0] * s, size[1] * s)
    mask = Image.new("L", big, 0)
    draw = ImageDraw.Draw(mask)

    draw.rounded_rectangle(
        tuple(c * s for c in PHONE_BBOX),
        radius=CORNER_RADIUS * s,
        fill=255,
    )
    for bbox in LEFT_BUTTONS + RIGHT_BUTTONS:
        draw.rounded_rectangle(
            tuple(c * s for c in bbox),
            radius=BUTTON_RADIUS * s,
            fill=255,
        )
    return mask.resize(size, Image.LANCZOS)


# Build mask + white background once — same geometry for every screenshot.
_w, _h = CROP[2] - CROP[0], CROP[3] - CROP[1]
mask = build_mask((_w, _h))
white = Image.new("RGB", (_w, _h), "white")

for src in sorted(RAW.glob("*.png")):
    img = Image.open(src).convert("RGB")
    cropped = img.crop(CROP)
    composited = Image.composite(cropped, white, mask)
    resized = composited.resize(
        (TARGET_W, round(_h * TARGET_W / _w)), Image.LANCZOS
    )
    dst = OUT / src.name
    resized.save(dst, "PNG", optimize=True)
    print(f"  {src.name}: {img.size} → {resized.size} ({dst.stat().st_size // 1024} KB)")
