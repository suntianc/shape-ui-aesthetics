# Recipe: Dark Monochrome Work System

This recipe is exemplar-derived vocabulary, not a default; adopt, adapt, or reject it in service of the established aesthetic thesis.

**Evidence sites:** linear.app, raycast.com, resend.com (primary dark-mode evidence); vercel.com (a light-mode mirror of the same discipline — it supports the typography and color-budget clauses only, not the dark-ground values). All captured 2026-07.

**Counter-example archive:** amie.so, nothing.tech, daylightcomputer.com. All captured 2026-07.

## System proposition

Zero out the UI's hue budget and hand hierarchy to a single lever — grayscale demotion — so that scarce color and light emanate only from real content (screenshots, code, data, glow effects). In exchange: low fatigue under hours of sustained gaze on a near-black ground, and the credibility of "engineering precision — the demo is the proof."

## Applies when

Consider this system only when all of the following hold:

- **A professional tool used in long immersive sessions**: developer tools, productivity tools, infrastructure products where users stare at the screen for hours daily (linear.app, raycast.com, vercel.com, and resend.com all belong to this class).
- **The content carries its own evidentiary force**: product screenshots, real code, and data panels persuade on their own; the page need only organize evidence rather than render emotion (linear.app's loop of verb-phrase headings plus full-width live screenshots; resend.com's real SDK code windows).
- **The brand persona is restraint and precision**: the persuasion strategy is demonstration rather than dramatization, and the page is allowed to look "undesigned" (vercel.com's two-word H1 above the fold).
- **A sustained supply of high-quality content evidence exists** — in a grayscale system, content is the only source of color; when screenshot or code quality falls short, the whole system reads as empty.

## Does not apply — with live counter-examples

- **The product needs warmth, humanity, and play** → see the opposite move at amie.so: a light-gray paper ground (rgb 250), long-letter copy at 1.75 line height, highlighter marks, handwritten annotation type. Its persuasion runs on content density and a "hand-graded layer"; dark restraint would kill that temperament.
- **Brand commerce where product photography is the protagonist** → see nothing.tech: the UI is likewise zero-hue, but the ground is light gray #f5f5f5, all color is supplied by product photography, and multiple typographic personas (dot-matrix / monospace / serif) provide the play. A dark monochrome ground would swallow the lighting gradations in product photography.
- **A thesis of nature, warmth, and anti-screen-anxiety** → see daylightcomputer.com: a cream ground #faf5f2, fine serifs, and a single amber accent #ff9d00. Cold near-black gray is the exact opposite of an "amber glow" sensory claim — the color discipline is equally strict, but the direction is entirely different.
- **The content itself is polychrome** (calendar events, canvas-based creative tools): the 9-color × 9-step event palette leaked in amie.so's stylesheet shows its product content is inherently colorful; a dark gray base cannot carry it.

## Perceptual grounding

- **Color, light, and material**: in scotopic-leaning viewing, the eye is far more sensitive to lightness differences than hue differences, so a single grayscale ladder can carry all hierarchy information. Once the UI's hue is zeroed, any color appearing in content automatically acquires very high signal value — scarcity itself is the emphasis mechanism. Near-black (rather than pure black) preserves the lowest register of "surface-ness," giving 1px light borders and floating cards something to sit on.
- **Information, attention, and typography**: attention is a single-channel scarce resource; when hierarchy uses one encoding dimension (lightness demotion), the decoding rule a reader builds is the simplest and most stable. Redundant multi-dimensional encoding — size plus color plus weight — raises cognitive cost instead. The 1.0 line height and negative tracking on large display type are not a style but optical compensation: enlarging the type enlarges the apparent gaps between letters and lines, which must be tightened to keep the word-group cohesive.
- **Spatial composition / motion rhythm and causality**: isomorphic section loops ("short claim → full-width live evidence"; linear.app's five identical major sections, raycast.com's couplet cycle) keep the cognitive load of a long page constant. One shared easing curve site-wide (raycast.com writes its spring as a CSS token) keeps the motion language as monophonic as the grayscale language, generating no new attentional noise.

## Parameter bands

These are bands, not single values.

| Decision | Band | Forbidden zone | Evidence |
|---|---|---|---|
| Background lightness | Near-black rgb 7–10, slightly cool (linear.app rgb(8,9,10); raycast.com rgb(7,8,10)) | Pure black #000 (unless compensated like resend.com with an alpha ladder plus glow material); any deep ground with a pronounced hue (deep blue-violet) | linear.app, raycast.com; resend.com as the boundary case (captured 2026-07) |
| Body/heading primary | 240–248, not pure white (linear.app 247; resend.com 240; raycast.com uses 255 but compresses body line height to 1.15 at low density) | Long body passages in pure white with no grayscale demotion | linear.app, resend.com, raycast.com (captured 2026-07) |
| Secondary text | One mid-gray step, 120–155 (raycast.com #78787c; linear.app rgb(138,143,152)); optionally one more step near 194 as a third level (raycast.com fg-200) | A text palette exceeding three gray levels; color used for secondary information | linear.app, raycast.com (captured 2026-07) |
| Hierarchy mechanism | Same size, demoted gray (linear.app's H2 = H1 in form, only switched to 138 gray); or a "white-bold line + gray line" couplet (raycast.com's 20px H2); or a family switch (resend.com: serif H1 / sans H2) | A size-ladder barrage (48/36/28/22) plus gray demotion plus bolding — all three levers at once | linear.app, raycast.com, resend.com (captured 2026-07) |
| H1 scale | 64–96px / line height 1.0–1.1 / tracking -1% to -6% / weight 400–600 (linear.app 64/1.0/510/-2.2%; raycast.com 64/1.1/600/0; resend.com 96/1.0/400/-1%; vercel.com 64/1.0/400/-6%) | Heavy-weight barrages at ≥700; negative tracking applied to body text at ≤16px; "tightness" drawn simultaneously from extreme negative tracking and high weight (each site takes only one source) | linear.app, vercel.com, resend.com, raycast.com (captured 2026-07) |
| UI hue budget | 0–1: zero (linear.app's hero carries no accent) or one functional color (vercel.com's link blue rgb(0,114,245)); brand color permitted only as background glow, never as controls (raycast.com: red = light beam) | Polychrome gradient accents; a colored primary CTA; kickers that change color every section (that is amie.so's system) | linear.app, vercel.com, raycast.com (captured 2026-07) |
| Where color lives | Color resides only in the content layer: inside screenshots (linear.app), code highlighting and data green (resend.com), third-party extension cards (raycast.com); semantic state colors held down on ~15%-alpha grounds (raycast.com's four) | Any decorative color in the UI's base layer | linear.app, resend.com, raycast.com (captured 2026-07) |
| Primary button on dark | Light ground with dark text (raycast.com rgb(230,230,230) ground / rgb(47,48,49) text; resend.com's light "Get started" button) | A solid colored primary button | raycast.com, resend.com (captured 2026-07) |
| Control radius | 4–8px (vercel.com 6; resend.com 6–8; raycast.com 4–8 steps) | Site-wide default pill (linear.app's 9999px pill is a single-site signature; transplanting it is cloning) | vercel.com, resend.com, raycast.com (captured 2026-07) |
| Monospace type | A separate family reserved for machine language only: code, command lines, labels, states (linear.app Berkeley Mono; raycast.com JetBrains Mono; resend.com Commit Mono; vercel.com Geist Mono) | Monospace spread into body and headings as "tech-flavored decoration" | linear.app, raycast.com, resend.com, vercel.com (captured 2026-07) |
| Motion | One primary easing site-wide: a custom ease-out class curve (raycast.com's cubic-bezier(0.23,1,0.32,1) appears 980 times; vercel.com and resend.com lean on cubic-bezier(0.4,0,0.2,1)); raycast.com additionally writes its spring as a hundred-segment linear() shared token | A different easing per component; bounce-class comedic curves | raycast.com, vercel.com, resend.com (captured 2026-07) |
| Body spec | 16px / line height 1.15–1.5 (linear.app 16/24; raycast.com 16/18.4) | Line heights ≥1.7 with a "long-letter" feel (that is amie.so's system) | linear.app, raycast.com (captured 2026-07) |

## Disciplines

1. **One hierarchy lever, carried all the way through**: once grayscale demotion (or a family switch) is chosen, size drama is reserved for the hero alone; from H2 down, size no longer speaks.
2. **Zero hue budget; color must have a residence**: the UI base layer holds only grays. Every color must answer "which layer does it live in" (content screenshot / code highlighting / data / background glow); color with no residence is deleted.
3. **Tightness has exactly one source**: with line height compressed to 1.0–1.1, choose negative tracking or high weight — never both — and apply negative tracking only at display sizes.
4. **Monospace is the dedicated channel for machine language**: permitted for code, commands, labels, states; barred from body and headings.
5. **Near-black, not pure black**; if pure black is chosen, hierarchy must switch to an alpha-transparency ladder (resend.com's --black-a1 through a12 approach) rather than a gray palette, or the dark end collapses into banding.
6. **Primary buttons on dark grounds use lightness, not color** — the button's salience comes from lightness contrast, spending nothing from the hue budget.
7. **Isomorphic narrative loop**: "short claim → real product evidence," repeated section after section without variation; a long page holds attention through constant rhythm, not visual stimulation.

## Known failure modes

- **Dark ground plus polychrome gradient accents** = neither Linear nor anything else — the first discipline (zeroed hue) is broken, and the whole system degrades to a "black skin."
- **Pure black #000 with an 8-step gray palette transplanted directly**: the dark-end grays smear into one muddy band on pure black; resend.com's remedy is the alpha ladder plus glow material — without that compensation, do not use pure black.
- **All three levers at once**: size ladder plus gray demotion plus bolding produces redundant hierarchy and destroys the sense of restraint — the single lever is where this system's identity comes from.
- **Monospace spread across the page for "hacker flavor"**: once the machine-language channel is diluted, real code evidence loses its identity.
- **Packing up Linear's full signature set** (510 weight + pill buttons + -2.2% tracking + the rgb(8,9,10) ground, moved together): that is single-site cloning, not use of a recipe; each parameter should land inside its band anew, against your own typeface and content.
- **A grayscale system with hollow content**: with no real screenshots or code to show, the page is left with a gray ground and slogans — at that point switch persuasion strategies (see amie.so's long-copy system) instead of forcing dark restraint.
- **Negative tracking pushed down into body text**: tracking beyond -2% at or below 16px collapses readability outright — measured body tracking at every evidence site is 0.

## Usage rulings

- 2026-07-26, Zellij trial (human-accepted): a kicker label used one accent color under the near-white recipe's slot-accounting discipline (one color, no rotation, three enumerated slots) inside an otherwise dark monochrome system. Ruling: borrowing the slot ledger is a legitimate combination — this recipe's zero-accent stance is the default starting point, not a hard prohibition.
