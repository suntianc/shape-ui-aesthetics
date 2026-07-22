#!/usr/bin/env python3
"""Validate the public Shape UI Aesthetics repository without mutable local state."""

from __future__ import annotations

import hashlib
import importlib.util
import re
import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_NAME = "shape-ui-aesthetics"
SOURCE = ROOT / "packages" / PACKAGE_NAME
RELEASE = ROOT / "releases" / PACKAGE_NAME / "1.0.0" / "package" / PACKAGE_NAME
DISTRIBUTIONS = ROOT / "releases" / PACKAGE_NAME / "distributions" / "1.0.0"
PLATFORM_TOOL = ROOT / "evaluation" / PACKAGE_NAME / "package_platform_distributions.py"
FRONTMATTER = re.compile(r"\A---\n(?P<yaml>.*?)\n---\n", re.DOTALL)
MARKDOWN_LINK = re.compile(r"(?<!!)\[[^]]*\]\((?P<target>[^)]+)\)")
FORBIDDEN_RUNTIME_NAMES = {"README.md", "CHANGELOG.md", "CONTRIBUTING.md", "SECURITY.md"}


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
    match = FRONTMATTER.match(path.read_text(encoding="utf-8"))
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


def platform_validation() -> list[str]:
    spec = importlib.util.spec_from_file_location("platform_distributions", PLATFORM_TOOL)
    if spec is None or spec.loader is None:
        return ["could not load platform distribution validator"]
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module.validate_directory(DISTRIBUTIONS, "1.0.0", require_read_only=False)


def main() -> int:
    failures: list[str] = []
    for required in (ROOT / "README.md", ROOT / "LICENSE", ROOT / "CONTRIBUTING.md", ROOT / "SECURITY.md", ROOT / "requirements-dev.txt"):
        if not required.is_file():
            failures.append(f"missing repository document: {required.relative_to(ROOT)}")

    if not SOURCE.is_dir() or SOURCE.is_symlink():
        failures.append("editable Runtime Package is missing or invalid")
    else:
        validate_frontmatter(SOURCE / "SKILL.md", failures)
        forbidden = sorted(
            path.relative_to(SOURCE).as_posix()
            for path in SOURCE.rglob("*")
            if path.is_file() and (path.name in FORBIDDEN_RUNTIME_NAMES or path.name == ".DS_Store")
        )
        if forbidden:
            failures.append(f"non-runtime files found in Runtime Package: {forbidden}")
        validate_links(SOURCE, failures)

    if not RELEASE.is_dir() or RELEASE.is_symlink():
        failures.append("accepted runtime release is missing or invalid")
    elif SOURCE.is_dir() and file_map(SOURCE) != file_map(RELEASE):
        failures.append("editable Runtime Package differs from accepted 1.0.0 release")

    if not PLATFORM_TOOL.is_file():
        failures.append("platform distribution validator is missing")
    else:
        failures.extend(f"platform distribution: {failure}" for failure in platform_validation())

    if failures:
        print("FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("PASS")
    print("runtime_source=valid")
    print("source_release_parity=true")
    print("platform_distributions=2")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
