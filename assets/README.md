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
| `banner.png` | Dark banner, 1280x400. The default, and the one that works on both GitHub themes. |
| `banner@2x.png` | The same at 2560x800, for retina. |
| `banner-light.png` | Light banner, for a light-only surface. |
| `banner-light@2x.png` | The same at 2x. |
| `banner.svg` / `banner-light.svg` | The sources. Edit these, not the PNGs. |
| `banner.py` | Regenerates every banner from the SVG sources. |

## Regenerating the banners

The banners are drawn, not composited from a screenshot, so they can be
changed without redrawing anything:

```console
$ python3 assets/banner.py && rsvg-convert -w 1280 -h 400 -o banner.png banner.svg
```

Three things in there were decided by looking at the render rather than by
reasoning about it. The beacon extends its own bar upward so it sits on the
mast rather than floating above it. The bar field on the right starts clear
of the longest line of text, because running it underneath softened the
subtitle. And its opacity falls with distance, so it reads as one signal
continuing off the edge instead of a scatter.

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
