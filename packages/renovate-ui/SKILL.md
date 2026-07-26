---
name: renovate-ui
description: Diagnose, grade, and renovate the UI of an existing product — web, mobile, or desktop. Use when the user asks to optimize, beautify, modernize, upgrade, or redesign an interface that already exists and the depth of change is not yet agreed. Grades the current UI into one of four intervention grades (Rebuild, Remodel, Calibrate, Elevate), then delivers an evidence-backed analysis report plus a high-fidelity HTML preview of the proposed result before any code is touched.
---

# Renovate UI

Renovation is a consulting workflow, not a styling pass. Its central failure mode — inherited from timid defaults — is anchoring: treating whatever design exists as a constraint to respect, then polishing a system that should have been replaced. This skill replaces anchoring with grading: judge first whether the current design deserves to survive, obtain an explicit mandate, show the destination, and only then change anything.

Aesthetic judgment itself is delegated: run diagnosis, direction, and execution through the shape-ui-aesthetics skill (its nine domain lenses, exemplar recipes with measured parameter bands, and critique guardrails). This skill owns the contract around that judgment: evidence, grade, mandate, preview, and staged execution.

## 1. Collect the evidence set

Renovation judges a real interface, never a description of one. Assemble an evidence set before judging:

- **Live captures** of every consequential surface — key screens, states (empty, loaded, error), and both light/dark themes where they exist — at desktop and mobile breakpoints for web, at device resolution for apps.
- **Style truth** from the source: stylesheets, design tokens, theme files, component styles (whatever the stack — CSS, utility classes, SwiftUI/Compose/Flutter/React Native style code).
- **Product truth**: what the product is, who uses it, and any brand constraints the owner declares immovable.

Capture with whatever the platform offers — browser automation for web, simulator or device screenshots for mobile apps, window captures or accessibility tooling for desktop. When the environment cannot capture, request screenshots from the user; do not diagnose from imagination or from code alone.

## 2. Diagnose against the reference bar

Run the evidence set through the shape-ui-aesthetics review protocol: scan the nine domain lenses, measure the interface against the exemplar recipes' parameter bands, and record findings as evidence — measured values, contradictions, and screenshots — never as taste adjectives. Two questions structure everything:

1. **Is there a system?** One authored logic governing type, color, spacing, and motion — or accumulated fragments that contradict each other.
2. **Is the system right?** Does its direction fit the product's meaning, audience, era, and platform conventions? A mobile app wearing web-marketing aesthetics is a direction error even when internally consistent.

## 3. Grade the intervention

Assign exactly one grade from [intervention grades](references/intervention-grades.md). The grade is the mandate: it defines what the renovation is allowed to destroy.

| Grade | Signal | Mandate |
|---|---|---|
| **Rebuild** | No coherent system exists, or the system fundamentally misfits the product | Suspend deference to the current visual layer entirely; establish a new aesthetic thesis from zero |
| **Remodel** | A real system points in the wrong direction — dated, borrowed, or misaligned | Replace the governing direction; preserve information architecture and load-bearing structure |
| **Calibrate** | Direction is right, execution is sloppy — parameters fall outside measured recipe bands | Bring parameters into band; do not change direction |
| **Elevate** | Nothing is wrong and nothing is memorable | Preserve the system; introduce a Signature Move and finishing depth |

State the grade with its supporting evidence. Never grade above the evidence, and never soften a grade to avoid a large mandate — an under-graded renovation is the anchoring failure this skill exists to prevent.

Regardless of grade, the **protected band** never enters the mandate: real content, working functionality, state truth, accessibility, and data integrity survive every grade including Rebuild.

## 4. Deliver the report and the preview

Before touching product code, deliver two artifacts:

1. **Analysis report** — the grade with per-domain evidence, what will change and what is protected, and the measured gaps (current value → target band, with the reference sites behind each band).
2. **Preview** — one self-contained HTML page showing a consequential surface *after* renovation, built with the product's real content, at the fidelity of a shippable page. For mobile or desktop apps, render the preview as a high-fidelity mockup inside a device frame; the preview is a visual promise, not an implementation claim. Follow [report and preview](references/report-and-preview.md).

The owner may accept the grade or bound it downward ("I accept it needs Rebuild, but this cycle only allows Calibrate"). Record the accepted mandate; it governs execution.

## 5. Execute within the mandate

Hand execution to the shape-ui-aesthetics workflow in the mode the grade implies — Rebuild and Remodel run as redesigns, Calibrate and Elevate as bounded refinements — carrying the accepted mandate as the Change Boundary and implementing in the product's actual stack, with units translated to the platform's system (px, pt, dp). Verify the result against the preview promise on the real product, at the same surfaces and states the evidence set captured.

Renovation ends with a delivery statement: grade, what changed, measured before/after values, what was deliberately preserved, and what remains for future cycles.
