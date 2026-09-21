#!/usr/bin/env python3
"""Render the mast banner in a dark and a light variant.

    python3 banner.py

Run it from this directory; it reads mascot.png and writes banner*.png here.
Requires Pillow and rsvg-convert (librsvg).

The layout is drawn as SVG and rasterised, then the mascot photograph is
composited on top. The mascot cannot be drawn: it is a bitmap with a white
backdrop, and its white t-shirt sits six levels away from that backdrop with
no edge between them, so there is nothing to cut it out along. Instead both
variants put a panel behind it in exactly the backdrop's own colour, which
turns what would be a seam into a deliberate card.
"""

import pathlib
import subprocess

from PIL import Image, ImageDraw, ImageFilter

ORANGE = (242, 113, 28)
W, H = 1280, 400
FONT = "Avenir Next, Helvetica Neue, Helvetica, Arial, sans-serif"
MASCOT = "mascot.png"

# Measured from mascot.png rather than guessed.
PANEL = (251, 251, 251)

PANDA_H = 404  # the mascot fills its square frame top to bottom
PANEL_X, PANEL_Y = W - 470, 34
PANDA_X, PANDA_Y = PANEL_X + 36, PANEL_Y + 24


def cluster(cx, cy, hot, cool, n=9, unit=13, gap=10, peak=112):
    """The logo mark: nine rounded bars under a diagonal two-tone split."""
    parts, total = [], n * unit + (n - 1) * gap
    x0, mid, beacon = cx - total / 2, n // 2, None

    for i in range(n):
        t = (i - (n - 1) / 2) / ((n - 1) / 2)
        h = peak * (1 - 0.70 * t * t) + (26 if i == mid else 0)
        x, y = x0 + i * (unit + gap), cy - h / 2
        if i == mid:
            beacon = (x + unit / 2, y)
        parts.append(
            f'<rect x="{x:.1f}" y="{y:.1f}" width="{unit}" '
            f'height="{h:.1f}" rx="{unit / 2:.1f}"/>'
        )

    body = "\n".join(parts)
    x1, y1 = x0 - 28, cy + peak / 2 + 54
    x2, y2 = x0 + total + 36, cy - peak / 2 - 54

    clips = (
        f'<clipPath id="up"><polygon points="{x1},{y1} {x2},{y2} '
        f'{x2},-220 {x1},-220"/></clipPath>'
        f'<clipPath id="lo"><polygon points="{x1},{y1} {x2},{y2} '
        f'{x2},{H + 220} {x1},{H + 220}"/></clipPath>'
    )
    marks = (
        f'<g clip-path="url(#up)" fill="{hot}">{body}</g>'
        f'<g clip-path="url(#lo)" fill="{cool}">{body}</g>'
        f'<circle cx="{beacon[0]:.1f}" cy="{beacon[1]:.1f}" r="14.5" fill="{hot}"/>'
    )
    return clips, marks


def build(name, bg, cool, title, sub, foot, dark):
    clips, marks = cluster(122, 168, f"rgb{ORANGE}", cool)
    glow = (
        '<ellipse cx="146" cy="182" rx="290" ry="224" fill="url(#glow)"/>'
        if dark
        else ""
    )

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{bg[0]}"/><stop offset="1" stop-color="{bg[1]}"/></linearGradient>
  <radialGradient id="glow" cx="0.5" cy="0.5" r="0.5">
    <stop offset="0" stop-color="rgb{ORANGE}" stop-opacity="0.20"/>
    <stop offset="1" stop-color="rgb{ORANGE}" stop-opacity="0"/></radialGradient>
  {clips}
</defs>
<rect width="{W}" height="{H}" fill="url(#bg)"/>
{glow}{marks}
<text x="122" y="282" font-family="{FONT}" font-size="58" font-weight="600" fill="{title}" letter-spacing="-1.5" text-anchor="middle">mast</text>
<text x="322" y="158" font-family="{FONT}" font-size="34" font-weight="600" fill="{title}" letter-spacing="-0.6">Multi-tenant MQTT broker</text>
<text x="322" y="202" font-family="{FONT}" font-size="34" font-weight="400" fill="{sub}" letter-spacing="-0.6">built on core NATS</text>
<rect x="322" y="230" width="52" height="3" rx="1.5" fill="rgb{ORANGE}"/>
<text x="322" y="272" font-family="{FONT}" font-size="17" fill="{foot}">One binary, from an edge box to a clustered fleet.</text>
</svg>"""

    tmp = pathlib.Path(f".{name}.svg")
    tmp.write_text(svg)
    subprocess.run(
        ["rsvg-convert", "-w", str(W), "-h", str(H), "-o", f".{name}.png", str(tmp)],
        check=True,
    )
    base = Image.open(f".{name}.png").convert("RGBA")
    tmp.unlink()
    pathlib.Path(f".{name}.png").unlink()

    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(shadow).rounded_rectangle(
        [PANEL_X - 2, PANEL_Y - 2, W + 40, H + 40],
        radius=32,
        fill=(0, 0, 0, 70 if dark else 26),
    )
    base.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(14)))

    # Rounded on the two visible corners; the other two sit off-canvas.
    panel = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(panel).rounded_rectangle(
        [PANEL_X, PANEL_Y, W + 40, H + 40], radius=30, fill=PANEL + (255,)
    )
    base.alpha_composite(panel)

    mascot = Image.open(MASCOT).convert("RGB")
    mascot = mascot.resize(
        (int(mascot.width * PANDA_H / mascot.height), PANDA_H), Image.LANCZOS
    )
    base.alpha_composite(mascot.convert("RGBA"), (PANDA_X, PANDA_Y))

    out = base.convert("RGB")
    out.save(f"{name}.png", optimize=True)
    out.resize((W * 2, H * 2), Image.LANCZOS).save(f"{name}@2x.png", optimize=True)


build("banner", ("#26272B", "#141517"), "#E8E9EC", "#FFFFFF", "#C9CBD0", "#8A8D93", True)
build("banner-light", ("#EAEAEC", "#F1F1F3"), "#4A4A4A", "#3A3A3A", "#6A6A6A", "#8E8E8E", False)
