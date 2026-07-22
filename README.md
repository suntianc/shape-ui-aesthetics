# Shape UI Aesthetics

An authored aesthetic system for designing distinctive, medium-native user interfaces with AI coding agents.

Shape UI Aesthetics treats an interface as one authored system: establish the protagonist, ritual, desired afterimage, central tension, aesthetic thesis, and Signature Move before selecting components. Its nine-domain capability layer then reconciles composition, typography, color, motion, interaction, computational medium, human fit, and evidence into one coherent result.

## Repository layout

- `packages/shape-ui-aesthetics/` — the single editable Runtime Package source.
- `evaluation/shape-ui-aesthetics/` — package-external qualification inputs and local exploratory runs; it never ships in the Skill payload.
- `releases/shape-ui-aesthetics/1.0.0/` — the accepted Codex runtime package and manifest.
- `releases/shape-ui-aesthetics/distributions/1.0.0/` — the matching Codex and Claude Code archives.
- `examples/nine-scenarios/` — nine self-contained qualification demonstrations.
- `tools/validate_repository.py` — the reproducible public repository gate.
- `evaluation/shape-ui-aesthetics/package_platform_distributions.py` — deterministic dual-platform packaging and validation.

## Nine scenario gallery

Open [`examples/nine-scenarios/gallery.html`](examples/nine-scenarios/gallery.html) locally to compare all nine pages.

https://github.com/user-attachments/assets/b7ac16cc-34f6-4e12-ae62-29ea714a1386

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

## Install across agents

The editable Runtime Source uses platform-neutral discovery metadata and is the repository's only discoverable Skill. Install it with the Vercel Labs Skills CLI for any supported agent:

```bash
npx skills@latest add suntianc/shape-ui-aesthetics \
  --skill shape-ui-aesthetics \
  --agent '*' \
  --global \
  --yes
```

Omit `--global` for a project-local installation. The CLI installs from the Git repository; accepted release archives remain the auditable, checksum-backed distribution record.

Pin installation to the accepted `v1.0.0` Runtime Package path for reproducibility:

```bash
npx skills@latest add \
  https://github.com/suntianc/shape-ui-aesthetics/tree/v1.0.0/packages/shape-ui-aesthetics \
  --skill shape-ui-aesthetics \
  --agent '*' \
  --global \
  --yes
```

## Install the 1.0.0 archives

Both `1.0.0` archives contain the same platform-neutral `SKILL.md`, references, and capability contracts. The Codex archive additionally includes `agents/openai.yaml`; the Claude Code archive omits only that Codex-specific UI metadata.

```bash
# Claude Code
unzip releases/shape-ui-aesthetics/distributions/1.0.0/shape-ui-aesthetics-1.0.0-claude-code.zip -d ~/.claude/skills

# Codex
unzip releases/shape-ui-aesthetics/distributions/1.0.0/shape-ui-aesthetics-1.0.0-codex.zip -d ~/.codex/skills
```

Inspect an existing installation before replacing it. Do not use the rejected legacy package as a rollback target.

## Build and validate release archives

Build only from an accepted immutable release. The builder refuses to overwrite an existing version:

```bash
python3 evaluation/shape-ui-aesthetics/package_platform_distributions.py build 1.0.0
python3 evaluation/shape-ui-aesthetics/package_platform_distributions.py validate 1.0.0
```

`SKILL.md` remains byte-identical across Codex and Claude Code archives; only Codex-specific `agents/openai.yaml` is omitted from the Claude Code archive.

## Validate source work and releases

Candidate mode validates the editable Skill, the current Stable Baseline, and its platform distributions without requiring the evolving Source Package to equal that baseline. Release mode additionally requires byte-level parity between Source and the selected accepted release. Neither mode treats visual judgment as a mechanical pass/fail score.

```bash
python3 -m pip install -r requirements-dev.txt
python3 tools/validate_repository.py --mode candidate
python3 tools/validate_repository.py --mode release --version 1.0.0
```

## Status

The platform-neutral `1.0.0` Runtime Package is accepted for cross-agent distribution. The nine example pages are independently browser-checked at mobile and desktop widths; they are demonstration artifacts, not a replacement for human aesthetic acceptance of future changes.

## Contributing

Keep `packages/shape-ui-aesthetics/` as the only editable runtime source. Every accepted package version must produce both a Codex and a Claude Code distribution from the same release artifact. Changes to capability behavior, routing, or the Stable Spine require the project's evolution and qualification process.

Read [CONTRIBUTING.md](CONTRIBUTING.md) before opening a change. Report security concerns privately as described in [SECURITY.md](SECURITY.md).
