# Recipe — Editorial Reading Baseline

This recipe is exemplar-derived vocabulary, not a default; adopt, adapt, or reject it in service of the established aesthetic thesis.

> Supporting sites: ia.net, frankchimero.com, pudding.cool, joshwcomeau.com, paco.me (all captured 2026-07, archives intact). Counter-examples: vercel.com, linear.app (captured 2026-07).

## 1. System proposition

The aesthetic of a long-form or content-first page is anchored by the body triad — size × line-height × measure — with hierarchy derived outward from the body through a single lever, and all separation delegated to whitespace on a discrete spacing scale. Typography reinforces the information structure; it does not invent structure through large type.

## 2. Applies when

- The dominant content mode is **continuous reading**: article pages, blog indexes, personal homepages, editorial or magazine-style front pages, documentation body text — the reader works through paragraphs line by line rather than glancing and clicking away.
- The page's value lives in the words themselves (argument, narrative, catalogue); product screenshots or illustration serve at most as head-and-tail decoration (joshwcomeau.com: "sugar at the ends, nutrition in the middle").
- A single page carries at least several hundred words, or an item list requires isomorphic scanning across a dozen or more entries (the joshwcomeau.com article stream, pudding.cool story cards).
- The product's temperament accepts "typography as the product" (ia.net) or "plain surface, systematic core" (paco.me) — restraint is willingly traded for readability.

## 3. Does not apply — with live counter-examples

- **Manifesto-style marketing heroes**: copy compressed below ten words, hierarchy carried by enormous type and whitespace — see vercel.com: H1 at 64px, line-height 1.0, letter-spacing -6%, with body text reduced to a footnote. That "display kill" holds only for a two-word headline; transplanted into multi-line long-form text it becomes a return-sweep disaster.
- **Density-first tool narrative pages**: see linear.app: heading line-height pressed to 1.0, H2 demoted by same-form graying, buttons at 13px, the whole page cycling "claim → full-width screenshot as evidence" — the evidence is screenshots, not prose; 13px is control-type discipline, not reading-type discipline.
- Dashboards, tables, and interfaces built for high-frequency operation, comparison, or entry — that is a scanning-composition problem, not an immersive-reading problem; route it through the field-structured path of reading-and-scanning composition.

## 4. Perceptual grounding

- **Information, attention, and typography** (reading-and-scanning composition; visual hierarchy and salience): typeface, contrast, measure, and spacing should **reinforce, never invent**, the information structure. Immersive long-form reading is explicitly a different scene from operational scanning, and a narrative must not be handled with scanning's fragmenting devices. Continuous reading moves by saccade plus return sweep at each line break; measure and line-height jointly determine return-sweep accuracy — this is the mechanism behind "when size rises, line-height and measure rise with it" (ia.net pairs 22px with 1.65; pudding.cool needs only 1.4 at 16px).
- **Human fit, cognition, and inclusion**: 16px is the floor for effortless reading, and reading comfort can itself be a product claim (ia.net renders "focused writing" directly as the felt experience of its own site); near-black on near-white softens contrast to reduce glare fatigue over long sessions.

## 5. Parameter bands

Bands, not single values.

| Decision | Band | Forbidden zone | Evidence |
|---|---|---|---|
| Body size | 16–22px (16 is the mode; 22 the large-type upper end) | <16px as body; 13px tool sizing for long-form text | frankchimero.com, pudding.cool, joshwcomeau.com, paco.me (16) / ia.net (22) |
| Body line-height | Latin 1.4–1.75, coupled to size (16px → 1.4–1.5; 22px → 1.65); **CJK long-form 1.7–2.0** (square glyphs lack ascenders and descenders, so return sweeps need extra leading); **CJK short-copy/list 1.5–1.65** (short paragraphs have no long return sweep and tolerate Latin leading) | <1.3; large size with tight leading (22/1.2); CJK long-form below 1.7 | pudding.cool 1.4, frankchimero.com and joshwcomeau.com 1.5, ia.net 1.65, paco.me token 1.75. CJK long-form band confirmed by five site measurements (2026-07-26): theinitium.com article 18px × 2.0, blog.justfont.com article 18px × 1.81, sspai.com article 17px × 1.8, thetype.com article 19px × 1.7, 1101.com long-form column 16px × 1.9 while the same site's UI short copy uses 1.5 — one site running both tiers is the strongest evidence for the two-tier model; the KOReader trial's 17px × 1.9 sits mid-band. CJK short-copy tier measured: sspai.com home 1.5, theinitium.com home 1.5, morisawa.co.jp 1.5, toraya-group.co.jp 1.6, ia.net/ja 1.65 |
| CJK body letter-spacing | 0 to +5% (positive tracking): Traditional-Chinese and Japanese text in **left-aligned** settings often adds +2% to +5% of ease; Simplified Chinese commonly stays at 0; **drops to zero under justified alignment** (the justification algorithm takes over inter-glyph distribution) | Negative tracking on CJK body text; stacking positive tracking on justified text | Measured: 1101.com +0.8px at 16px (+5%), morisawa.co.jp +0.7px at 14px (+5%), theinitium.com +0.45px at 18px (+2.5%), sspai.com and thetype.com at 0. Conditional evidence: blog.justfont.com uses 0 tracking on its justified long-form body but +0.48px (+3%) on left-aligned excerpts — one site proving both branches |
| Measure (content column width) | Latin 576–720px (≈60–80 characters at 16px); **CJK long-form 36–42 characters per line** (≈640–760px) | Text running the full container; Latin >90 characters; CJK >45 characters | frankchimero.com `--spacing-col: 36rem` (576), paco.me `--content-width: 640px`, pudding.cool `--width-column-regular: 720px`; CJK measured (2026-07-26): theinitium.com 680px/38 chars, sspai.com 680px/40 chars, thetype.com 711px/37 chars, blog.justfont.com 750px/42 chars, 1101.com 580px/36 chars |
| Heading-to-body size ratio | 0.9–2.6 (a heading may be no larger than body) | ≥4× (64/16 is a marketing ratio) | paco.me 1.0 (H1 = 16), frankchimero.com 0.875 (h1 at 14 < 16), joshwcomeau.com and pudding.cool 2.0 (32/16), ia.net 2.6 (57.8/22); counter-examples vercel.com and linear.app at 4.0 |
| Heading line-height | 1.1–1.5 (take the upper end for multi-line headings) | 1.0 on multi-line headings | ia.net 1.1, joshwcomeau.com 1.5; counter-examples vercel.com and linear.app at 1.0 |
| Letter-spacing | Body 0 to +1%; headings 0 to -2.5% | -6% on headings (the vercel.com reading) | frankchimero.com body +0.16px (≈+1%), ia.net headings -1.5%, pudding.cool headings -0.8px/32px (≈-2.5%) |
| Foreground/background | Near-black foreground, L 10–58, on background 247–255 (or the same logic inverted) | Pure #000 colliding with pure #fff | ia.net 34/247, pudding.cool 38/255, joshwcomeau.com rgb(10,12,16), paco.me #3a3a3a; inverted face frankchimero.com #eee/#3d4340 |
| Weight lever | One step per level: +100 (paco.me 400→500), or an extreme jump (pudding.cool 900/400 with no intermediate), or a single site-wide weight (frankchimero.com 400) | 500/600/700 deployed as consecutive multi-step ladder | paco.me, pudding.cool, frankchimero.com |
| Spacing scale | Discrete, 6–9 steps (e.g. 4/8/16/24/32/48/64/72/128) | Off-scale arbitrary values; continuous micro-adjustment | paco.me nine steps, frankchimero.com six steps (0.25/0.5/1/1.5/4/6rem) |

## 6. Disciplines

1. **Body first**: lock the size × line-height × measure triad before anything else; headings, annotations, and spacing all derive from it. The triad is internally coupled — when size rises, line-height and measure rise with it.
2. **One lever per level**: each hierarchy step moves exactly one variable and carries it through — paco.me moves only weight (+100), frankchimero.com only gray value (two light/dark steps), joshwcomeau.com only color plus letter-spacing (the magenta eyebrow), pudding.cool only the extreme weight gap (900/400). A size jump is the last resort, not the first.
3. **Headings need not exceed body size**: position, weight, and color are sufficient to declare hierarchy (paco.me H1 = body 16px; frankchimero.com's h1 is smaller than body).
4. **Links spend no color budget**: on all five supporting sites, links share body color or its gray family, distinguished by underline (pudding.cool, joshwcomeau.com, paco.me) or by position plus a two-gray split (ia.net, frankchimero.com); external links take a structural mark such as ↗ (paco.me, frankchimero.com).
5. **Monospace only for exhibited content and machine language**: code, dates, serial numbers, forms (joshwcomeau.com inline code, pudding.cool metadata, paco.me 13px code, ia.net editor screenshots) — never inside the body container.
6. **Separation by whitespace, not bordered cards**: between items and paragraphs, only steps drawn from the spacing scale (the joshwcomeau.com article stream carries no card borders; whitespace occupies two-thirds of frankchimero.com; paco.me opens with 128px of top whitespace).
7. **All-caps only as small-size, positive-tracking eyebrows or labels** (joshwcomeau.com 16px with +2px tracking; ia.net CTA capsules); uppercase long-sentence body text is forbidden.

## 7. Known failure modes

- **Marketing headline discipline transplanted into article pages**: 64px with line-height 1.0 and -6% tracking applied to multi-line headings — the vercel.com treatment holds only on a two-word H1; long headlines get glyph collision and warring lines.
- **Large size without its couplings**: copying ia.net's 22px while keeping 1.4 leading and a full-width container yields crowding, not generosity.
- **All three levers at once**: every heading level jumping size, weight, and color together — the hierarchy noise drowns the structure; none of the five supporting sites does this.
- **Colored links**: brand blue plus hover shift plus icon on body links breaks the grayscale skeleton; the color budget belongs to points of emphasis (ia.net spends it only on the CTA, joshwcomeau.com only on the eyebrow).
- **Tool sizing for body text**: 13–14px long-form text (linear.app's 13px is button/control discipline), or mobile body dropping below 16px and triggering zoom.
- **Single-site cloning**: lifting ia.net's 22/1.65 plus light-gray paper plus blue capsule wholesale — that is iA's brand, not the recipe. Take the triad-coupling discipline; choose parameters within the bands according to your own temperament.
