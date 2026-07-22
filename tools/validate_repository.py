#!/usr/bin/env python3
"""Validate repository source work or an accepted Shape UI Aesthetics release."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import re
import subprocess
import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_NAME = "shape-ui-aesthetics"
SOURCE = ROOT / "packages" / PACKAGE_NAME
RELEASES = ROOT / "releases" / PACKAGE_NAME
DISTRIBUTIONS = RELEASES / "distributions"
PLATFORM_TOOL = ROOT / "evaluation" / PACKAGE_NAME / "package_platform_distributions.py"
RELEASE_INTEGRITY = ROOT / "docs" / "release-integrity.md"
FRONTMATTER = re.compile(r"\A---\n(?P<yaml>.*?)\n---\n", re.DOTALL)
MARKDOWN_LINK = re.compile(r"(?<!!)\[[^]]*\]\((?P<target>[^)]+)\)")
STABLE_VERSION = re.compile(r"^(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|[1-9]\d*)$")
FORBIDDEN_RUNTIME_NAMES = {"README.md", "CHANGELOG.md", "CONTRIBUTING.md", "SECURITY.md"}
NON_PUBLIC_ROOTS = {".agents", ".claude", ".git", ".scratch", "books", "pdfs", "research", "releases"}


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def file_map(root: Path) -> dict[str, str]:
    return {
        path.relative_to(root).as_posix(): digest(path)
        for path in sorted(item for item in root.rglob("*") if item.is_file())
    }


def within(root: Path, path: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
    except ValueError:
        return False
    return True


def validate_frontmatter(path: Path, failures: list[str]) -> None:
    text = path.read_text(encoding="utf-8")
    match = FRONTMATTER.match(text)
    if not match:
        failures.append("Runtime SKILL.md has malformed frontmatter")
        return
    metadata = yaml.safe_load(match.group("yaml"))
    if set(metadata or {}) != {"name", "description"}:
        failures.append("Runtime SKILL.md frontmatter must contain only name and description")
        return
    if metadata["name"] != PACKAGE_NAME:
        failures.append("Runtime SKILL.md name does not match its directory")
    if not isinstance(metadata["description"], str) or not metadata["description"].strip():
        failures.append("Runtime SKILL.md description is empty")
    if "Codex" in text or "Claude" in text:
        failures.append("Runtime SKILL.md must be platform-neutral for cross-agent distribution")


def validate_links(root: Path, failures: list[str]) -> None:
    for path in root.rglob("*.md"):
        text = path.read_text(encoding="utf-8")
        for match in MARKDOWN_LINK.finditer(text):
            target = match.group("target").split(maxsplit=1)[0].strip("<>")
            if not target or target.startswith(("#", "http://", "https://", "mailto:")):
                continue
            destination = (path.parent / target.split("#", 1)[0]).resolve()
            if not within(root, destination):
                failures.append(f"{path.relative_to(root)} links outside Runtime Package: {target}")
            elif not destination.exists():
                failures.append(f"{path.relative_to(root)} links to a missing path: {target}")


def semantic_key(version: str) -> tuple[int, int, int]:
    match = STABLE_VERSION.fullmatch(version)
    if not match:
        raise ValueError(f"not a stable semantic version: {version}")
    return tuple(int(match.group(part)) for part in ("major", "minor", "patch"))


def load_manifest(path: Path) -> dict:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    return value if isinstance(value, dict) else {}


def accepted_versions() -> list[str]:
    versions: list[str] = []
    if not RELEASES.is_dir():
        return versions
    for path in RELEASES.iterdir():
        if not path.is_dir() or not STABLE_VERSION.fullmatch(path.name):
            continue
        manifest_path = path / "manifest.yaml"
        if not manifest_path.is_file():
            continue
        try:
            metadata = load_manifest(manifest_path).get("package", {})
        except (OSError, UnicodeError, yaml.YAMLError):
            continue
        if (
            isinstance(metadata, dict)
            and metadata.get("name") == PACKAGE_NAME
            and metadata.get("version") == path.name
            and metadata.get("state") == "accepted"
        ):
            versions.append(path.name)
    return sorted(versions, key=semantic_key)


def platform_validation(root: Path, version: str) -> list[str]:
    spec = importlib.util.spec_from_file_location("platform_distributions", PLATFORM_TOOL)
    if spec is None or spec.loader is None:
        return ["could not load platform distribution validator"]
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module.validate_directory(root, version, require_read_only=False)


def validate_runtime_source(failures: list[str]) -> None:
    if not SOURCE.is_dir() or SOURCE.is_symlink():
        failures.append("editable Runtime Package is missing or invalid")
        return

    skill_path = SOURCE / "SKILL.md"
    if not skill_path.is_file() or skill_path.is_symlink():
        failures.append("Runtime SKILL.md is missing or invalid")
    else:
        validate_frontmatter(skill_path, failures)
    forbidden = sorted(
        path.relative_to(SOURCE).as_posix()
        for path in SOURCE.rglob("*")
        if path.is_file() and (path.name in FORBIDDEN_RUNTIME_NAMES or path.name == ".DS_Store")
    )
    if forbidden:
        failures.append(f"non-runtime files found in Runtime Package: {forbidden}")
    validate_links(SOURCE, failures)


def validate_public_skill_inventory(failures: list[str]) -> None:
    unexpected: list[str] = []
    for path in ROOT.rglob("SKILL.md"):
        relative = path.relative_to(ROOT)
        if relative.parts[0] in NON_PUBLIC_ROOTS:
            continue
        if path == SOURCE / "SKILL.md":
            continue
        unexpected.append(relative.as_posix())
    if unexpected:
        failures.append(
            "additional discoverable SKILL.md files would be exposed by repository installers: "
            f"{sorted(unexpected)}"
        )


def git_lines(*args: str) -> list[str]:
    result = subprocess.run(
        ("git", *args),
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return [line for line in result.stdout.splitlines() if line]


def stable_directories_at(ref: str, path: str) -> set[str]:
    try:
        names = git_lines("ls-tree", "-d", "--name-only", f"{ref}:{path}")
    except subprocess.CalledProcessError:
        return set()
    return {name for name in names if STABLE_VERSION.fullmatch(name)}


def validate_release_immutability(base_ref: str, failures: list[str]) -> bool:
    if base_ref.startswith("-") or "\x00" in base_ref:
        failures.append(f"immutable release base ref is invalid: {base_ref!r}")
        return False
    if re.fullmatch(r"0{40}", base_ref):
        return False
    try:
        git_lines(
            "rev-parse",
            "--verify",
            "--end-of-options",
            f"{base_ref}^{{commit}}",
        )
    except subprocess.CalledProcessError:
        failures.append(f"immutable release base ref is unavailable: {base_ref}")
        return False

    release_versions = stable_directories_at(
        base_ref,
        f"releases/{PACKAGE_NAME}",
    )
    distribution_versions = stable_directories_at(
        base_ref,
        f"releases/{PACKAGE_NAME}/distributions",
    )
    try:
        changed_rows = git_lines(
            "diff",
            "--name-status",
            "--find-renames",
            base_ref,
            "--",
            f"releases/{PACKAGE_NAME}",
        )
    except subprocess.CalledProcessError as error:
        failures.append(f"could not compare immutable releases with {base_ref}: {error}")
        return False

    protected: set[str] = set()
    release_prefix = f"releases/{PACKAGE_NAME}/"
    distribution_prefix = f"{release_prefix}distributions/"
    for row in changed_rows:
        fields = row.split("\t")
        for changed_path in fields[1:]:
            if changed_path.startswith(distribution_prefix):
                relative = changed_path.removeprefix(distribution_prefix)
                version = relative.split("/", 1)[0]
                if version in distribution_versions:
                    protected.add(changed_path)
                continue
            if changed_path.startswith(release_prefix):
                relative = changed_path.removeprefix(release_prefix)
                version = relative.split("/", 1)[0]
                if version in release_versions:
                    protected.add(changed_path)
    if protected:
        failures.append(
            "accepted release files are immutable; publish a new semantic version instead: "
            f"{sorted(protected)}"
        )
    return True


def validate_accepted_release(version: str, failures: list[str]) -> Path | None:
    release_root = RELEASES / version
    package = release_root / "package" / PACKAGE_NAME
    manifest_path = release_root / "manifest.yaml"
    distributions = DISTRIBUTIONS / version

    if not release_root.is_dir() or release_root.is_symlink():
        failures.append(f"accepted release {version} is missing or invalid")
        return None
    if not package.is_dir() or package.is_symlink():
        failures.append(f"accepted release {version} package is missing or invalid")
        return None
    if not manifest_path.is_file() or manifest_path.is_symlink():
        failures.append(f"accepted release {version} manifest is missing or invalid")
        return None

    try:
        manifest = load_manifest(manifest_path)
    except (OSError, UnicodeError, yaml.YAMLError) as error:
        failures.append(f"accepted release {version} manifest could not be read: {error}")
        return package

    metadata = manifest.get("package", {})
    if not isinstance(metadata, dict):
        failures.append(f"accepted release {version} package metadata is malformed")
    else:
        if metadata.get("name") != PACKAGE_NAME:
            failures.append(f"accepted release {version} package name mismatch")
        if metadata.get("version") != version:
            failures.append(f"accepted release {version} manifest version mismatch")
        if metadata.get("state") != "accepted":
            failures.append(f"accepted release {version} state is not accepted")

    manifest_files: dict[str, str] = {}
    file_rows = manifest.get("files", [])
    if not isinstance(file_rows, list):
        failures.append(f"accepted release {version} file manifest is malformed")
    else:
        for row in file_rows:
            if not isinstance(row, dict) or not isinstance(row.get("path"), str) or not isinstance(row.get("sha256"), str):
                failures.append(f"accepted release {version} contains a malformed file record")
                continue
            if row["path"] in manifest_files:
                failures.append(f"accepted release {version} contains duplicate file record: {row['path']}")
            manifest_files[row["path"]] = row["sha256"]
    if manifest_files != file_map(package):
        failures.append(f"accepted release {version} files differ from its manifest")

    if not PLATFORM_TOOL.is_file():
        failures.append("platform distribution validator is missing")
    else:
        failures.extend(
            f"platform distribution: {failure}"
            for failure in platform_validation(distributions, version)
        )
    return package


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode",
        choices=("candidate", "release"),
        default="candidate",
        help="candidate permits source evolution; release requires source parity with an accepted release",
    )
    parser.add_argument(
        "--version",
        help="stable baseline or release version; defaults to the latest accepted stable version",
    )
    parser.add_argument(
        "--immutable-from",
        metavar="GIT_REF",
        help="reject changes to stable release versions that already exist at this Git ref",
    )
    args = parser.parse_args()
    failures: list[str] = []
    for required in (
        ROOT / "README.md",
        ROOT / "LICENSE",
        ROOT / "CONTRIBUTING.md",
        ROOT / "SECURITY.md",
        ROOT / "requirements-dev.txt",
        RELEASE_INTEGRITY,
    ):
        if not required.is_file():
            failures.append(f"missing repository document: {required.relative_to(ROOT)}")

    validate_runtime_source(failures)
    validate_public_skill_inventory(failures)
    immutability_checked = False
    if args.immutable_from:
        immutability_checked = validate_release_immutability(
            args.immutable_from,
            failures,
        )

    if args.version and not STABLE_VERSION.fullmatch(args.version):
        failures.append(f"version is not a stable semantic version: {args.version}")
        version = ""
    else:
        versions = accepted_versions()
        version = args.version or (versions[-1] if versions else "")
        if not version:
            failures.append("no accepted stable release could be discovered")

    package = validate_accepted_release(version, failures) if version else None
    if args.mode == "release" and package is not None and SOURCE.is_dir():
        if file_map(SOURCE) != file_map(package):
            failures.append(f"editable Runtime Package differs from accepted {version} release")

    if failures:
        print("FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("PASS")
    print(f"mode={args.mode}")
    print("runtime_source=valid")
    print("cross_agent_source=true")
    print(f"stable_baseline={version}")
    print("baseline_integrity=true")
    print(f"source_release_parity={'true' if args.mode == 'release' else 'not_required'}")
    if immutability_checked:
        immutability_state = "checked"
    elif args.immutable_from:
        immutability_state = "not_applicable"
    else:
        immutability_state = "not_requested"
    print(f"release_immutability={immutability_state}")
    print("platform_distributions=2")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
