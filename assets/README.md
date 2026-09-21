# assets

Brand assets for mast.

| File | Use |
| --- | --- |
| `logo.png` | Source lockup, 1254x1254. Start here for anything new. |
| `logo-512.png` | Organization avatar. GitHub asks for at least 500px. |
| `logo-256.png` | READMEs and docs. |
| `logo-128.png` | Small inline use. |
| `mark.png` | The mark alone, no wordmark, for places the word would be redundant or too small to read. |
| `mark-256.png` | The same at a sensible size. |
| `mascot.png` | The mascot, 1254x1254. It wears the lockup, so it stands in for the logo where there is room for personality. |
| `mascot-512.png` | The same, sized for a README. |
| `banner.png` | Dark banner, 1280x400, with the mascot. The default. |
| `banner@2x.png` | The same at 2560x800, for retina. |
| `banner-light.png` | Light banner. Pair it with the dark one in a `<picture>` so each GitHub theme gets its own. |
| `banner-light@2x.png` | The same at 2x. |
| `banner.py` | The source. Edit this, not the PNGs — it renders all four. |

## Regenerating the banners

`banner.py` is the whole source: it draws the layout as SVG, rasterises it, then composites `mascot.png` on top. Run it from inside `assets/`, with Pillow and `rsvg-convert` available.

```console
$ cd assets && python3 banner.py
```

### Why the mascot sits on a panel

The mascot is a photograph on a white backdrop and cannot be cut out. Its backdrop measures `(251, 251, 251)` and its white t-shirt measures `(245, 243, 248)` — six levels apart, with no edge between them. Every threshold tight enough to keep the shirt leaves a halo, and every threshold loose enough to remove the backdrop eats holes in the shirt and the white fur. A flood fill from the frame edges fails for a second reason: the mascot's own dark body touches the bottom edge, so some seed points are inside the subject.

So it is not cut out. Both banners draw a rounded panel in exactly the backdrop's own colour and place the mascot inside it. What would have been a seam becomes a deliberate card, and a soft shadow under the panel does the work the cutout was supposed to do.

### Decisions made by looking, not by reasoning

The beacon extends its own bar upward so it sits on the mast rather than floating above it. The mascot bleeds off the bottom edge instead of standing clear of it, because a figure with air underneath reads as pasted in. And the mark is placed left of the text rather than above it: stacked, the banner needed more height than 400px and GitHub renders it smaller for the trouble.

## There is deliberately no favicon here

The lockup was rendered at the sizes it will actually be seen at before being adopted. It survives 40px, which is what GitHub shows in a list, and it does not survive 16px: nine bars with two-pixel gaps become an orange-grey blur and the wordmark becomes a smear. The mark alone is better at that size and still soft.

A favicon needs its own drawing — three or five bars rather than nine, wider gaps, no wordmark, and probably no diagonal split, since at 16px the split adds noise rather than meaning. Shipping a downscaled lockup as a favicon would just be shipping a blur.

## Colours

Sampled from the artwork rather than specified in advance, so treat them as the source of truth for anything new:

| | |
| --- | --- |
| Orange | `#F2711C` |
| Charcoal | `#4A4A4A` |
| Ground | `#F3F3F3` — off-white, not pure white |

The ground is sampled from the artwork rather than chosen. Compositing onto `#F4F4F4` instead left the lockup sitting in a faintly visible box one shade off its surroundings, which is the kind of thing nobody sees until they do.
