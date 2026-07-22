# Release Integrity

Accepted Runtime Package versions, their manifests, platform archives, and published Git tags are immutable. A correction after publication receives a new semantic version rather than rewriting an existing release.

## One-time `1.0.0` portability rebaseline

The initial accepted `1.0.0` artifact was introduced by commit `4a7f0f9` with a Codex-specific discovery description. Before adopting Git-based cross-agent installation through `npx skills`, commit `f455dd3` made the discovery metadata platform-neutral and rebuilt the derived Codex and Claude Code archives.

This changed the `SKILL.md` checksum from `028a812495a5c7789973f5ac8a7484e92c59cb09fe18f22d5172e5955a8966f1` to `57e1a8dd9e936c965aa589f8904335a1071b16fdaf81868c5bc10e5636885d68`. It did not change a capability contract, capability revision, routing behavior, qualification result, or Aesthetic Acceptance. The `v1.0.0` tag identifies the portable rebaseline at `f455dd3`.

This is the only accepted exception to release immutability.

## Rule after the rebaseline

- Do not edit a version directory already present under `releases/shape-ui-aesthetics/` or `releases/shape-ui-aesthetics/distributions/`.
- Do not move, replace, or recreate a published version tag.
- Publish representation-only corrections as a `PATCH` release, compatible capability or routing evolution as `MINOR`, and Stable Spine or routing-protocol changes as `MAJOR`.
- Pin reproducible `npx skills` installation to the accepted tag and Runtime Package path.
- Keep release archives as checksum-backed audit and rollback artifacts even when `npx skills` is the primary installation channel.

The repository CI compares each change with its base Git ref. It rejects modifications or additions inside a stable release version that already existed at that ref, while allowing a new semantic-version directory to be introduced. Tag pushes are checked separately: moving an existing `v*` tag fails, while a new tag must pass release parity for the matching version.
