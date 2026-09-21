import math, subprocess, pathlib

ORANGE = "#F2711C"
W, H = 1280, 400
FONT = "Avenir Next, Helvetica Neue, Helvetica, Arial, sans-serif"

def cluster(cx, cy, n=9, unit=15, gap=11, peak=132):
    parts, total = [], n * unit + (n - 1) * gap
    x0, mid, beacon = cx - total / 2, n // 2, None
    for i in range(n):
        t = (i - (n - 1) / 2) / ((n - 1) / 2)
        h = peak * (1 - 0.70 * t * t) + (30 if i == mid else 0)
        x, y = x0 + i * (unit + gap), cy - h / 2
        if i == mid:
            beacon = (x + unit / 2, y)
        parts.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{unit}" height="{h:.1f}" rx="{unit/2:.1f}"/>')
    return "\n".join(parts), beacon, (x0, cy - peak / 2, total, peak)

def field(colour, start, end, base_op):
    """A regular rhythm that recedes, rather than a scatter. The wave is a
    single sine so it reads as one signal continuing off the edge, and the
    opacity falls with distance so the eye is not pulled away from the mark."""
    out, span = [], max(end - start, 1)
    for i, x in enumerate(range(start, end, 24)):
        h = 40 + 30 * math.sin(i * 0.55)
        op = base_op * (1 - 0.55 * ((x - start) / span))
        out.append(f'<rect x="{x}" y="{196 - h/2:.0f}" width="6" height="{h:.0f}" '
                   f'rx="3" fill="{colour}" opacity="{op:.3f}"/>')
    return "\n".join(out)

def banner(name, bg1, bg2, hot, cool, title, sub, foot, fld, fld_op, glow):
    body, bc, (bx, by, bw, bh) = cluster(206, 196)
    x1, y1 = bx - 34, by + bh + 64
    x2, y2 = bx + bw + 44, by - 64
    g = '<ellipse cx="206" cy="200" rx="345" ry="255" fill="url(#glow)"/>' if glow else ""
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="{bg1}"/><stop offset="1" stop-color="{bg2}"/></linearGradient>
  <radialGradient id="glow" cx="0.5" cy="0.5" r="0.5">
    <stop offset="0" stop-color="{ORANGE}" stop-opacity="0.24"/>
    <stop offset="1" stop-color="{ORANGE}" stop-opacity="0"/></radialGradient>
  <clipPath id="up"><polygon points="{x1},{y1} {x2},{y2} {x2},-220 {x1},-220"/></clipPath>
  <clipPath id="lo"><polygon points="{x1},{y1} {x2},{y2} {x2},{H+220} {x1},{H+220}"/></clipPath>
</defs>
<rect width="{W}" height="{H}" fill="url(#bg)"/>
{g}
{field(fld, 1044, 1292, fld_op)}
<g clip-path="url(#up)" fill="{hot}">{body}</g>
<g clip-path="url(#lo)" fill="{cool}">{body}</g>
<circle cx="{bc[0]:.1f}" cy="{bc[1]:.1f}" r="17" fill="{hot}"/>
<text x="484" y="178" font-family="{FONT}" font-size="68" font-weight="600" fill="{title}" letter-spacing="-1.5">mast</text>
<text x="486" y="226" font-family="{FONT}" font-size="25" font-weight="500" fill="{sub}">Multi-tenant MQTT broker built on core NATS</text>
<rect x="486" y="250" width="52" height="3" rx="1.5" fill="{ORANGE}"/>
<text x="486" y="292" font-family="{FONT}" font-size="18" fill="{foot}">One binary, from an edge box to a clustered fleet.</text>
</svg>'''
    pathlib.Path(f"{name}.svg").write_text(svg)
    for scale, suffix in ((1, ""), (2, "@2x")):
        subprocess.run(["rsvg-convert","-w",str(W*scale),"-h",str(H*scale),
                        "-o",f"{name}{suffix}.png",f"{name}.svg"], check=True)

banner("banner-dark", "#232427", "#141517", ORANGE, "#E8E9EC",
       "#FFFFFF", "#C9CBD0", "#8A8D93", "#FFFFFF", 0.075, True)
banner("banner-light", "#F6F6F6", "#EAEAEA", ORANGE, "#4A4A4A",
       "#3A3A3A", "#6A6A6A", "#8E8E8E", "#4A4A4A", 0.10, False)
print("ok")
