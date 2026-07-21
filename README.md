# Shape UI Aesthetics

An authored aesthetic system for designing distinctive, medium-native user interfaces with Codex and Claude Code.

Shape UI Aesthetics treats an interface as one authored system: establish the protagonist, ritual, desired afterimage, central tension, aesthetic thesis, and Signature Move before selecting components. Its nine-domain capability layer then reconciles composition, typography, color, motion, interaction, computational medium, human fit, and evidence into one coherent result.

## Repository layout

- `packages/shape-ui-aesthetics/` — the single editable Runtime Package source.
- `releases/shape-ui-aesthetics/1.0.0/` — the accepted Codex runtime package and manifest.
- `releases/shape-ui-aesthetics/distributions/1.0.0/` — the matching Codex and Claude Code archives.
- `examples/nine-scenarios/` — nine self-contained HTML pages generated with OpenCode.
- `evaluation/shape-ui-aesthetics/package_platform_distributions.py` — deterministic dual-platform packaging and validation.

## Nine scenario gallery

Open [`examples/nine-scenarios/gallery.html`](examples/nine-scenarios/gallery.html) locally to compare all nine pages.

| # | Scenario | Page | Generation model |
|---:|---|---|---|
| 01 | Creator Portfolio | [open](examples/nine-scenarios/creator-portfolio/index.html) | `opencode-go/minimax-m2.7` |
| 02 | Ship Customizer | [open](examples/nine-scenarios/ship-customizer/index.html) | `opencode-go/minimax-m2.7` |
| 03 | Wildfire Atlas | [open](examples/nine-scenarios/wildfire-atlas/index.html) | `opencode-go/minimax-m2.7` |
| 04 | Finance Operations | [open](examples/nine-scenarios/finance-operations/index.html) | `opencode-go/minimax-m2.7` |
| 05 | Craft Archive | [open](examples/nine-scenarios/craft-archive/index.html) | `opencode-go/mimo-v2.5` |
| 06 | Clinical Alert | [open](examples/nine-scenarios/clinical-alert/index.html) | `opencode-go/minimax-m2.7` |
| 07 | SVG Favorite | [open](examples/nine-scenarios/svg-favorite/index.html) | `opencode-go/mimo-v2.5` |
| 08 | AI Landing Review | [open](examples/nine-scenarios/ai-landing-review/index.html) | `opencode-go/mimo-v2.5` |
| 09 | 3D Logistics Review | [open](examples/nine-scenarios/logistics-3d-review/index.html) | `opencode-go/mimo-v2.5` |

The first five completed pages used `minimax-m2.7`; after socket/SQLite instability, the remaining four used the same medium-cost tier's `mimo-v2.5`. The AI Landing Review and 3D Logistics Review pages also received their technical corrections from `mimo-v2.5`.

## Install a release

Each accepted version publishes both platform archives. The archives contain the same references and capability contracts. The Codex archive includes `agents/openai.yaml`; the Claude Code archive omits that Codex-only UI metadata and adapts only the platform identity in `SKILL.md`.

```bash
# Claude Code
unzip releases/shape-ui-aesthetics/distributions/1.0.0/shape-ui-aesthetics-1.0.0-claude-code.zip -d ~/.claude/skills

# Codex
unzip releases/shape-ui-aesthetics/distributions/1.0.0/shape-ui-aesthetics-1.0.0-codex.zip -d ~/.codex/skills
```

Inspect an existing installation before replacing it. Do not use the rejected legacy package as a rollback target.

## Build and validate platform distributions

Build only from an accepted immutable release. The builder refuses to overwrite an existing version:

```bash
python3 evaluation/shape-ui-aesthetics/package_platform_distributions.py build 1.0.0
python3 evaluation/shape-ui-aesthetics/package_platform_distributions.py validate 1.0.0
```

## Status

The `1.0.0` Runtime Package is accepted. The nine example pages are independently browser-checked at mobile and desktop widths; they are demonstration artifacts, not a replacement for human aesthetic acceptance of future changes.

## Contributing

Keep `packages/shape-ui-aesthetics/` as the only editable runtime source. Every accepted package version must produce both a Codex and a Claude Code distribution from the same release artifact. Changes to capability behavior, routing, or the Stable Spine require the project's evolution and qualification process.
