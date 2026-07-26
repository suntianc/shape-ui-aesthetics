# Shape UI Aesthetics

An authored aesthetic system for designing distinctive, medium-native user interfaces with AI coding agents.

Shape UI Aesthetics treats an interface as one authored system: establish the protagonist, ritual, desired afterimage, central tension, aesthetic thesis, and Signature Move before selecting components. Its nine-domain capability layer then reconciles composition, typography, color, motion, interaction, computational medium, human fit, and evidence into one coherent result.

## How it works

The Skill runs as a Director that owns one authored result end to end:

1. **Frame** the assignment — artifact, change boundary, real content, and the environment's available media assets and asset-generation tools.
2. **Establish the Aesthetic Engine** — protagonist, ritual, desired afterimage, central tension, aesthetic thesis, Signature Move.
3. **Scan nine domain lenses**, loading exact capability contracts only where a decision is materially uncertain.
4. **Materialize** — declare an explicit asset strategy (*generate / placeholder / deliberately none*), consult the exemplar recipes for measured parameter bands, then build the real artifact.
5. **Critique before delivery** against authorship, coherence, accessibility, and implementation truth.

Two knowledge layers feed those decisions:

- **A principle layer** distilled from 22 cross-disciplinary books on architecture, perception, color, motion, typography, inclusion, and 3D — the *why* behind every judgment.
- **An exemplar layer** measured from living reference sites (Linear, Stripe, Aesop, iA, Teenage Engineering, 端傳媒, ほぼ日刊イトイ新聞, and more) — the *what exactly*: real type scales, color values, spacing systems, motion tokens, and imagery disciplines, recorded as parameter bands with named sources.

## The exemplar recipe layer

Six recipes translate the measured corpus into deployable vocabulary. Each carries applicability conditions, live counter-examples, parameter bands (never single values), disciplines, and known failure modes; every number cites the site it was measured from. Recipes are vocabulary, not defaults — the Director adopts, adapts, or rejects them in service of the thesis, and copying any single exemplar wholesale is defined as a failure mode.

| Recipe | Core discipline |
|---|---|
| Dark monochrome work system | Hierarchy through one lever (grayscale); zero-hue budget — color only lives in content |
| Near-white single accent | Surface color and content color keep separate ledgers; the accent is an enumerated slot budget |
| Paper serif brand | Dual non-extreme ground and ink; a single serif jurisdiction; near-zero weight budget |
| Editorial reading baseline | The body triad (size × line-height × measure) anchors the page, with measured CJK bands |
| Motion discipline and budget | One signed easing site-wide; measured duration tiers; single-digit autonomous animation budget |
| Imagery as material | Mandatory asset strategy; generation prompts derived from the thesis; schematics ship with micro-captions |

Recipes evolve through use: consequential human review verdicts are folded back as recorded **usage rulings** — the CJK two-tier line-height model and the schematic-plus-caption rule both entered the package this way — so the vocabulary sharpens with every real assignment.

## Repository layout

- `packages/shape-ui-aesthetics/` — the Runtime Package source for the authoring Skill.
- `packages/renovate-ui/` — the renovation-workflow Skill: grades an existing UI into one of four intervention grades (Rebuild / Remodel / Calibrate / Elevate), delivers an evidence-backed report plus an HTML preview before touching code, and delegates aesthetic judgment to shape-ui-aesthetics. Works across web, mobile, and desktop surfaces. Accepted in release 1.2.1.
- `evaluation/shape-ui-aesthetics/` — package-external qualification inputs and local exploratory runs; it never ships in the Skill payload.
- `releases/shape-ui-aesthetics/1.2.1/` — the current accepted runtime package and manifest (`1.0.0/`, `1.1.0/`, and `1.2.0/` remain as immutable predecessors).
- `releases/shape-ui-aesthetics/distributions/1.2.1/` — the matching Codex and Claude Code archives.
- `examples/nine-scenarios/` — nine self-contained qualification demonstrations.
- `docs/release-integrity.md` — the one-time `1.0.0` portability rebaseline and the immutable-release rule that follows it.
- `tools/validate_repository.py` — the reproducible public repository gate.
- `evaluation/shape-ui-aesthetics/package_platform_distributions.py` — deterministic dual-platform packaging and validation.

## Install across agents

Each package under `packages/` uses platform-neutral discovery metadata. Install the authoring Skill with the Vercel Labs Skills CLI for any supported agent:

```bash
npx skills@latest add suntianc/shape-ui-aesthetics \
  --skill shape-ui-aesthetics \
  --agent '*' \
  --global \
  --yes
```

Omit `--global` for a project-local installation. The CLI installs from the Git repository; accepted release archives remain the auditable, checksum-backed distribution record.

A global installation is owned at `~/.agents/skills/shape-ui-aesthetics`; supported agents discover that canonical copy directly or through symlinks. During migration, remove any older manually installed per-agent directory that would shadow it, then verify ownership and agent coverage with `npx skills@latest list -g --json`.

Pin installation to the accepted `v1.2.1` Runtime Package path for reproducibility:

```bash
npx skills@latest add \
  https://github.com/suntianc/shape-ui-aesthetics/tree/v1.2.1/packages/shape-ui-aesthetics \
  --skill shape-ui-aesthetics \
  --agent '*' \
  --global \
  --yes
```

## Install the 1.2.1 archives

Both `1.2.1` archives contain the same platform-neutral `SKILL.md`, references, capability contracts, and exemplar recipes. The Codex archive additionally includes `agents/openai.yaml`; the Claude Code archive omits only that Codex-specific UI metadata.

```bash
# Claude Code
unzip releases/shape-ui-aesthetics/distributions/1.2.1/shape-ui-aesthetics-1.2.1-claude-code.zip -d ~/.claude/skills

# Codex
unzip releases/shape-ui-aesthetics/distributions/1.2.1/shape-ui-aesthetics-1.2.1-codex.zip -d ~/.codex/skills
```

Inspect an existing installation before replacing it. Do not use the rejected legacy package as a rollback target.

## Nine scenario gallery (1.0.0 qualification artifacts)

The nine pages below qualified the original `1.0.0` release. They were generated with deliberately mid-tier models to test the Skill's floor, and are kept as historical demonstration artifacts. Open [`examples/nine-scenarios/gallery.html`](examples/nine-scenarios/gallery.html) locally to compare all nine pages.

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

## Build and validate release archives

Build only from an accepted immutable release. The builder refuses to overwrite an existing version:

```bash
python3 evaluation/shape-ui-aesthetics/package_platform_distributions.py build 1.2.1
python3 evaluation/shape-ui-aesthetics/package_platform_distributions.py validate 1.2.1
```

`SKILL.md` remains byte-identical across Codex and Claude Code archives; only Codex-specific `agents/openai.yaml` is omitted from the Claude Code archive.

## Validate source work and releases

Candidate mode validates the editable Skill, the current Stable Baseline, and its platform distributions without requiring the evolving Source Package to equal that baseline. Release mode additionally requires byte-level parity between Source and the selected accepted release. Neither mode treats visual judgment as a mechanical pass/fail score.

CI also compares the change with its base Git ref, rejects edits to any stable release version that already exists there, rejects movement of an existing `v*` tag, and validates every newly published version tag against its matching accepted release. A correction must be published under a new semantic version.

```bash
python3 -m pip install -r requirements-dev.txt
python3 tools/validate_repository.py --mode candidate
python3 tools/validate_repository.py --mode release --version 1.2.1
```

## Status

`1.1.0` introduced the exemplar recipe layer — distilled from a measured design corpus where every parameter band is backed by at least two reference sites — on top of the unchanged `1.0.0` Stable Spine and 32-capability roster. Its recipe trials (two open-source product pages plus a cross-model comparison on gpt-5.6-sol, gemini-3.6-flash, and MiniMax-M3) received human aesthetic acceptance on 2026-07-26.

`1.2.1` is the current accepted release. It folds the usage-driven evolution of the recipe layer into the package: measured CJK typography bands (five-site article measurements establishing the two-tier line-height model), measured motion-duration tiers (per-element computed-style surveys across seven sites), the imagery-as-material recipe, and the mandatory asset-strategy declaration — validated across five behavioral trials on gpt-5.6-sol, covering both the *generate* branch (thesis-derived prompt generation) and the defended *deliberately none* branch.

The measured corpus itself (screenshots, extracted tokens, per-site profiles) is a local research asset and is not distributed with this repository; recipes cite reference sites by name and capture date, keeping the Runtime Package self-contained. Human aesthetic acceptance remains the final gate for every change.

## Contributing

Keep `packages/shape-ui-aesthetics/` as the only editable runtime source. Every accepted package version must produce both a Codex and a Claude Code distribution from the same release artifact. Changes to capability behavior, routing, or the Stable Spine require the project's evolution and qualification process.

Read [CONTRIBUTING.md](CONTRIBUTING.md) before opening a change. Report security concerns privately as described in [SECURITY.md](SECURITY.md).
