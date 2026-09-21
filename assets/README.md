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
| `banner.png` | Wide lockup for the top of a README, 1280x360. |
| `banner-640.png` | The same at half size, for a narrower column. |

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
