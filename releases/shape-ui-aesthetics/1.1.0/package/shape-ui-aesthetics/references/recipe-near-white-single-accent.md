# Recipe: Near-White Calm System with a Single-Accent Budget

This recipe is exemplar-derived vocabulary, not a default; adopt, adapt, or reject it in service of the established aesthetic thesis.

> **Evidence sites:** supabase.com, asana.com, family.co, nothing.tech (all captured 2026-07). **Counter-examples:** linear.app, landonorris.com, amie.so (captured 2026-07). All values were measured from each site's captured profile and extracted design tokens.

## System proposition

Compress layout chroma to zero (near-white ground, near-black text, grayscale hierarchy) and concentrate all color salience into **at most one accent, granted only to enumerated slots** — manufacture attention through scarcity rather than saturation, and carry hierarchy with grayscale rather than color.

## Applies when

- The product needs a trustworthy, calm, evidence-first temperament: developer tools (supabase.com), work-management platforms (asana.com), finance/wallet products that want consumer warmth without frivolity (family.co), hardware commerce where the product itself is the protagonist (nothing.tech).
- **Content brings its own color.** Real product screenshots, photography, illustration, and status chips keep entering the page — the layout must yield, or layout color and content color fight each other. Across all four sites, every chromatic element belongs to the content layer: supabase.com's customer-story cards, asana.com's status chips and agent avatars, family.co's sticker illustrations, nothing.tech's product photography.
- Long multi-section pages (full-page heights of 7691–11315px across the four sites) that need constant cognitive load, building rhythm by switching evidence type rather than switching color theme.
- Light-mode reading environments — primarily daytime office and browsing contexts.

## Does not apply — with live counter-examples

- **Long-immersion professional dark environments** (tools that live beside an engineer's terminal): linear.app runs a near-black `rgb(8,9,10)` ground with a zero-accent dark monochrome system — the same budget discipline executed at the opposite end of the value scale (linear.app, captured 2026-07). Transplanting a near-white system onto such a product is a temperament mismatch.
- **High-energy, identity-forward brand expression** (athletes, streetwear, campaigns): landonorris.com is a high-saturation two-color identity system — fluorescent lemon `#d2ff00` against deep olive `#282c20` — that generates impact through chromatic collision, not single-accent scarcity (landonorris.com, captured 2026-07).
- **Long letter-style pages that persuade through content density and human warmth**: amie.so rotates one colored kicker per section (green/blue/purple/orange), exposes a 9-hue × 9-step product palette, and compensates for the looseness of many colors with long copy plus a handwritten-annotation layer (amie.so, captured 2026-07). Imitating its multi-color rotation without that compensating layer is this recipe's number-one failure mode (see Known failure modes, mode 1).

## Perceptual grounding

- **Color, light, and material (relational color):** color salience is a relative quantity, not an absolute one — an accent's prominence depends on the chroma level surrounding it, not on its own saturation. Once layout chroma is zeroed, a mid-saturation green (supabase.com's `#3fcf8e`) earns the prominence that would elsewhere require a fluorescent. This is the perceptual basis on which the "budget" holds.
- **Information, attention, and typography (hierarchy and salience):** attention is a zero-sum resource, and the fewer the hierarchy levers, the more predictable the result. All four sites hand hierarchy to a single lever — grayscale (asana.com headings `#0d0e10` vs body `#646f79`; supabase.com's gray-line/black-line two-tone headlines) — so color can be given wholly to the one job of emphasis without competing in hierarchy.
- **Human fit, cognition, and inclusion (reading comfort):** pure white ground with pure black text is maximum contrast — glaring over long pages, and it leaves the intermediate grays no room to live. supabase.com, family.co, and asana.com all keep text near-black (L 10–30%); supabase.com, family.co, and nothing.tech keep the ground at 96–99.5% lightness. Each end steps back one notch, buying hierarchy headroom and low glare.
- **Coherence, critique, and evidence (an auditable system):** an enumerated-slot accent budget makes every chromatic occurrence answerable — in-slot or out-of-bounds. That keeps the system criticizable and conserved through long multi-person iteration, where "decorate by feel" is not.

## Parameter bands

These are bands, not single values.

| Decision | Band | Off-limits | Evidence |
|---|---|---|---|
| Background lightness | L 96–99.5%, chroma ≈ 0: `#f5f5f5` (nothing.tech) → `oklch(0.995 0 34)` (supabase.com); warm drift permitted to `#FBFAF9` (family.co) | Bare pure white `#fff` with no buffer (asana.com does use `#fff`, but cushions it with `--gray-1 #f6f8f9` panels and a dot-grid texture); any large chromatic ground | supabase.com, family.co, nothing.tech, asana.com |
| Primary text | Near-black L 10–30%, chroma ≈ 0: `#0d0e10` (asana.com) / `oklch(0.1 0 34)` (supabase.com) / `#343433` (family.co, warm drift) | Pure black `#000` for 16px-class body text (nothing.tech uses pure black, but at the band's outer edge: ultra-thin display type over photographic grounds — not comparable to ordinary body copy) | supabase.com, asana.com, family.co |
| Secondary text gray | At least two steps apart from primary: `#646f79` (asana.com body), `#848281` (family.co muted), supabase.com's inline half-gray/half-black two-tone caption lines | A single text color site-wide | asana.com, family.co, supabase.com |
| Accent count | **0–1 layout-level accent:** supabase.com, one green `#3fcf8e`; asana.com, one gradient keyword (coral → pink); family.co, zero (CTAs are solid near-black `#343433`); nothing.tech, zero (UI in black/white/gray, all color in photography) | Two or more rotating accents (amie.so's per-section kicker rotation) | supabase.com, asana.com, family.co, nothing.tech |
| Accent slots | 3–5 enumerated slots: supabase.com grants four — H1 key line, primary CTA, code highlight, verification checkmark; asana.com grants one — the gradient keyword | Layout ground color, decorative shapes, illustration fills (supabase.com's illustrations are all gray line art) | supabase.com, asana.com |
| Chromatic/black accent sections | ≤2 per page: supabase.com's single chromatic section (customer-story cards); asana.com's two black sections (product demo + closing) | One color theme per section | supabase.com, asana.com |
| H1 | 46–102px, but **weight must stay light**: 300–500; line-height 0.9–1.1; letter-spacing 0 to -2.5% (supabase.com 46px/500/1.0/0; family.co 68px/500/1.1/-2%; asana.com 102px/300/0.9/-2.5%) | Large size and ≥700 weight applied together (asana.com maps all bold down to 500 site-wide) | supabase.com, family.co, asana.com |
| Body | 16px class, weight 400–450, line-height 1.4–1.75 (supabase.com 16/24 @450; asana.com 16/28; family.co 19px/1.42) | — | supabase.com, asana.com, family.co |
| Buttons | 14–16px / 500; solid near-black or the single accent; one radius regime, chosen once: 6px small radius (supabase.com, tool temperament) or pill (asana.com/family.co, consumer temperament) | More than two button colors in one interface | supabase.com, asana.com, family.co, nothing.tech |
| Spacing | 8px grid (three sites' tokens measured `scaleType: "8px"` identically) | — | supabase.com, asana.com, family.co |
| Shadow/border | Shadows step quietly in a non-black shadow color (asana.com's four levels all use blue-gray `rgb(36,50,66)`), or replace shadow entirely with a 1px light-gray border (supabase.com's bento cards) | Heavy pure-black shadows | asana.com, supabase.com |

## Disciplines

1. **Zero chroma in the layout, full chroma in the content — two ledgers, strictly separate.** Color may enter only as content (screenshots, photography, illustration, status chips); the layout ledger holds only near-white, gray, near-black, and at most one accent. family.co engineers this to its limit: `--graphic-*` tokens serve illustration only, `--app-*` serves product-UI contexts only, semantic colors serve state only, and text always draws from the neutral ledger.
2. **The accent is a budget, not seasoning: enumerate slots first, then apply color.** Everything outside the slots stays grayscale; when the budget runs short, drop an emphasis rather than add a second color. supabase.com's "one green × four slots" is the canonical form.
3. **Hierarchy runs on grayscale as its only lever, carried all the way through.** Headings near-black, body mid-gray, de-emphasis light gray; no size jumps, no multiple colors, no 600+ bolding as a second hierarchy system.
4. **Large headlines conserve weight: the larger the size, the lighter the weight.** 46px pairs with 500; 102px pairs only with 300, with line-height compressed toward 1.0. "Enormous but light" is the only way to scale up without shouting in a near-white system.
5. **Accents are rationed by section, ≤2 per page** (one chromatic or black section as the turn, one as the close); every other section builds rhythm by changing evidence type (screenshot → code → testimonial → number), not by changing color.
6. **Controls share the layout's temperament.** Buttons at small sizes, near-black or the single accent, one radius regime; marketing pages and product UI share the same control language (supabase.com carries 6px/14px from site to product without exception).

## Known failure modes

1. **A different accent per section** — formally resembling amie.so without amie.so's long-copy density and handwritten-annotation compensating layer. The result reads as a table of contents, not a system: the single accent's anchoring effect is diluted into decoration.
2. **Spreading the accent across large areas** (hero grounds, gradient washes, chromatic illustration fills) — scarcity goes bankrupt. supabase.com's green is prominent precisely because it never serves as a ground; spread it and the page degrades into an ordinary template marketing site.
3. **Both ends at maximum:** bare pure white `#fff` ground with pure black `#000` body — maximum contrast glares, the secondary grays have no room to live, and the grayscale lever of Disciplines item 3 collapses with them.
4. **All three hierarchy levers at once** (grayscale + size jumps + 700-level bolding) — everything shouts, so nothing ranks; contrast with asana.com's deliberate flattening of bold to 500.
5. **Single-site cloning:** lifting supabase.com's Manrope + Inter 450 + 6px radius + brand green wholesale is cloning, not distillation. What transfers from this recipe is the logic — zero-chroma layout, enumerated-slot budget, grayscale hierarchy; that the four sites' parameters all differ is the proof.
6. **Admitting illustration or chromatic content without a ledger** — content color and layout color bleed into each other until text and controls start picking up tint. For the correct treatment, see family.co's four-ledger governance in Disciplines item 1.

---

## Usage rulings

- 2026-07-26, Zellij trial run: kicker eyebrow labels used one accent green, declared under this recipe's slot ledger (a single color, no rotation, three slots total), which conflicted with the R1 reading of "zero accents above the fold"; passed human review. **Ruling: a dark system borrowing this recipe's slot ledger is a legitimate combination; R1's zero-accent stance is a default starting point, not a hard prohibition.**
