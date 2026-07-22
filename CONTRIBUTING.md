# Contributing

## Repository boundaries

- Edit Runtime content only in `packages/shape-ui-aesthetics/`.
- Keep evaluations, fixtures, generated artifacts, and review records outside the Runtime Package.
- Treat `releases/shape-ui-aesthetics/<version>/` and its distributions as immutable accepted artifacts. Do not amend them in place.
- Keep `SKILL.md` frontmatter limited to `name` and `description`. Put conditional depth in `references/`, deterministic repeat work in `scripts/`, and output material in `assets/` only when each is genuinely required.

## Propose a change

1. State the observable change hypothesis and whether it is local, cross-layer, or package-wide.
2. Change the smallest necessary source files. Do not update an accepted release or installed copy as a shortcut.
3. Add or update package-external evidence appropriate to the scope, including a positive case, a near miss, and a boundary case for affected capabilities.
4. Run the public repository gate:

   ```bash
   python3 -m pip install -r requirements-dev.txt
   python3 tools/validate_repository.py --mode candidate
   ```

5. For a proposed release, run the relevant qualification and human aesthetic review before creating an immutable release artifact and its platform distributions. Then verify release parity with `python3 tools/validate_repository.py --mode release --version <version>`.

## Pull request expectations

Describe the user-visible or routing consequence, affected capabilities and revisions, evidence run, and any remaining human judgment. Do not add source books, internal research-library material, local agent installations, generated caches, or credentials to the Runtime Package or pull request.
