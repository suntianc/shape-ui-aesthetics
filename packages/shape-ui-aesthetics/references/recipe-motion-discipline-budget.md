# Recipe: Motion Discipline & Micro-Interaction Budget

This recipe is exemplar-derived vocabulary, not a default; adopt, adapt, or reject it in service of the established aesthetic thesis.

**Supporting evidence:** five production sites — Family (family.co, captured 2026-07-26), Amie (amie.so, captured 2026-07-26), Emil Kowalski's personal site (emilkowal.ski, captured 2026-07-26), Raycast (raycast.com, captured 2026-07-26), Linear (linear.app, captured 2026-07-25). **Boundary counter-examples:** Lando Norris (landonorris.com, captured 2026-07-26) and iA (ia.net, captured 2026-07-26).

## 1. System proposition

Motion earns credibility through scarcity and shared physics: the whole interface converges on one signed easing curve plus one small-increment vocabulary of state feedback, while self-playing animation is rationed by a single-digit budget and issued only to narrative zones. Motion confirms cause and effect; it does not decorate. The lower the density, the more believable each individual movement becomes.

## 2. Applies when

- Tool-type and SaaS product or marketing pages, where users complete tasks, compare information, and scan evidence. Motion's role is "your action took effect," not performance. Linear, Raycast, Amie, and Family all belong to this class.
- High-frequency or long-dwell interfaces. Repeated exposure grinds the novelty of decorative motion into noise; only causal feedback survives the thousandth trigger.
- Pages that already carry a clear type-scale and gray-scale hierarchy. Motion only needs to receive that hierarchy, not substitute for it. Emil Kowalski's site is the limit sample: a motion engineer's personal site with zero keyframes.
- Multi-author teams where motion is implemented independently across components. The tokenized discipline in this recipe exists precisely to prevent a "one curve per author" split in the interface's physics.

## 3. Does not apply — with live counter-examples

- **Portfolio and brand sites where motion is the identity.** See the opposite practice at landonorris.com (captured 2026-07-26): a scroll-driven 3D helmet assembly hero, roughly two hundred cards revealed through clip-path and transform, a loading screen turned into a brand pun ("LOAD NORRIS"), and durations stretched to a theatrical 0.75s. Its motion budget is inverted — movement itself is the content. Note, however, that even at this ceiling the site holds exactly one token pair (`--cubic-default: cubic-bezier(0.65, 0.05, 0, 1)` plus `--duration-default: 0.75s`); curve discipline did not lapse when the budget inverted. Grafting Norris's theatrical durations and clip-path reveals onto a SaaS tool yields only a slower tool.
- **Pure reading and editing sites find even this recipe's budget excessive.** See ia.net (captured 2026-07-26): one keyframe on the entire page (a link background), transitions touching only color and transform, hover feedback expressed as text darkening from gray 34 toward 0 and press scales of 0.95/0.98. In a reading flow, any autonomous movement taxes attention; near-zero is correct.
- One-time-viewing contexts — first-reveal campaign pages, launch countdowns — where the repeated-exposure assumption fails. The budget may loosen there, though keeping the curve-token discipline is still advised.

## 4. Perceptual grounding

This recipe hangs on motion causality: motion is legitimate only when it closes a causal chain — user action first, interface movement second. The ease-out family (fast out, slow settle) is the default physics of micro-interaction because it imitates a real object that decelerates naturally after being pushed, making the response predictable to the body. Sharing one curve across the whole interface declares that this interface obeys a single set of physical laws, so any movement anywhere can be verified by bodily intuition. Autonomous, uncaused movement carries no causal information and only consumes attention, which is why it must be confined by budget to narrative zones.

## 5. Parameter bands

**Data caveat:** the collection pipeline injected a uniform `0.001s` to freeze animations during capture, so every duration recorded in the extracted token data is an artifact. Millisecond-scale duration bands for micro-interactions could not be measured from this corpus and are excluded from the table below, downgraded to a phenomenon note in section 7. The only genuine duration value observed is the landonorris.com CSS token `--duration-default: 0.75s`. Easing curves, transitioned properties, feedback increments, and animation density were all measured directly.

| Decision | Band (not a single value) | Forbidden zone | Evidence |
|---|---|---|---|
| Number of signed easing curves | One primary curve site-wide (1–2 low-frequency auxiliary variants allowed) | One curve per component; bare browser `ease` treated as a design decision | Raycast `cubic-bezier(0.23,1,0.32,1)` x980; Linear `(0.25,0.46,0.45,0.94)` x97; Family `(0.19,1,0.22,1)` x98; landonorris.com holds `--cubic-default` as its sole curve token |
| Micro-interaction curve family | ease-out family (fast out, slow settle), or the standard curve `(0.4,0,0.2,1)` | Hover starting from `ease-in`; bounce/elastic on control feedback | The signed curves of Family, Raycast, and Linear are all ease-out variants; Amie x17 and Emil Kowalski x1 use `(0.4,0,0.2,1)` |
| Writing springs | Springs are tokenized too: a many-segment `linear()` approximation stored in a CSS variable, shared site-wide | JS spring parameters scattered per component | Raycast `--spring-1` (a 101-segment `linear()`); landonorris.com is isomorphic with its single token |
| Hover background increment | Overlay opacity 3–8%: light ground `rgba(0,0,0,0.05)`, dark ground `rgba(255,255,255,0.08)`; or a lightness shift of at most 3 steps | Hue changes; large-area inversion; new shapes appearing on hover | Amie `0→0.05`; Linear `0→0.08` (text stepping 138→247 in sync); Emil Kowalski ground 253→245; Family white → display-p3 0.984 (about 2%) |
| Press / hover scale | Scale 0.95–0.98, button-class elements only | Text links translating; scale beyond 5% | ia.net measured at two stops, `matrix(0.95…)` and `matrix(0.98…)`; Linear button transition props include transform |
| Transitioned-property allowlist | color / background(-color) / opacity / transform / border-color / box-shadow / filter | Layout properties — width/height/top/left (sole corpus exception: Raycast nav height) | Aggregated transition-property data across all seven sites — Linear, Raycast, Amie, Family, Emil Kowalski, iA — falls entirely inside the allowlist |
| Autonomous animation (keyframes) budget | 0–8 per page, appearing only in hero / product-demo cards / decorative grids; marketing pages take the upper bound, personal and reading sites take 0–1 | Autonomous animation on nav, links, buttons, inputs | Emil Kowalski 0; Amie 1 (marquee); Family 1; iA 1 (link); Raycast 7 (hero and card demos); Linear 8 (card staggerIn plus decorative grid-dot) |
| Duration token structure | Duration converges to a single token; expressive/narrative motion caps at about 0.75s | A magic-number duration per animation site | landonorris.com `--duration-default: 0.75s` (the only measured true duration); Raycast's tokenized easing corroborates "motion parameters live in the variable system" |

## 6. Disciplines

1. **Every motion has a cause; two classes never mix.** Interactive elements get transitions only (user triggers, interface responds); autonomous animation goes only to narrative zones — hero, product demo, decorative grid — and never appears on navigation, links, buttons, or inputs. All seven corpus sites hold this without exception.
2. **One curve equals one physics.** The signed easing lives as a token shared site-wide; springs are tokenized through `linear()` as well. Before adding a motion, ask whether the existing curve serves; if not, question the motion itself.
3. **Feedback through increments, not drama.** Express state change through small increments on cheap properties (compositor and paint layers): 3–8% background opacity, one gray-scale step on text, scale within 5%. Translation, deformation, and newly appearing elements do not belong to the hover-feedback vocabulary.
4. **The density budget decays with proximity to text.** At most one autonomous animation per viewport; the closer to body-reading flow and list-scanning zones, the closer the budget goes to zero. iA and Emil Kowalski are living proof of the zero budget.
5. **One duration token; hierarchy sets the tier.** Control feedback shortest, container transitions middle, page-level narrative longest — but all derived by multiplier from the same token. Do not invent a distinct duration per button.
6. **Respect `prefers-reduced-motion`** (a principle-level requirement, not measured in this corpus): autonomous animation must degrade to zero movement; causal feedback may remain as an instant state switch.

## 7. Known failure modes

- **"Premium means everything moves."** Parallax per card, translation per button, a hand-written curve per site — the interface's physics fractures, bodily intuition can no longer model any single movement, and the result reads busy and cheap. The motion-richest corpus site, Raycast, uses its custom easing 980 times — as 980 reuses of one curve.
- **Treating Norris as the default.** Moving the 0.75s theatrical duration and clip-path reveals into SaaS controls makes every click a performance. What transfers from the ceiling sample is the token discipline, never the parameters.
- **Bare `ease` everywhere.** Unsigned curves — browser-default `ease` mixed with ad-hoc beziers — is what ungoverned territory looks like in the token data across all seven sites; a signed curve with a high reuse count is what governed territory looks like.
- **Learning "no feedback" from Emil Kowalski.** Misreading zero keyframes as zero feedback and cutting even the hover background increment destroys affordance. That site has no animation, yet every link confirms with a 253→245 shift.
- **Transitioning layout properties.** Animating width/height/top/left forces reflow and stutters; the texture of the movement immediately betrays the engineering level. When a property outside the allowlist wants to move, first ask whether transform is equivalent.
- **Phenomenon note (recorded, not admitted to the parameter bands):** the conventional millisecond band for micro-interactions (roughly 100–300ms) could not be verified in this corpus because capture froze animations; it awaits re-measurement once the pipeline is fixed. At present only "duration converges to a token; narrative tier caps at about 0.75s" holds evidential standing.
