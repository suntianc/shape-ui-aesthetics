#!/usr/bin/env python3
"""Build and validate Codex and Claude Code distributions from one accepted release."""

from __future__ import annotations

import argparse
import hashlib
import os
import re
import shutil
import stat
import tempfile
import zipfile
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]
RELEASE_ROOT = ROOT / "releases" / "shape-ui-aesthetics"
PACKAGE_NAME = "shape-ui-aesthetics"
PLATFORM_ROOT = RELEASE_ROOT / "distributions"
LEGACY_FILES = {
    "aesthetic-generation.md",
    "collision-and-direction.md",
    "design-grammar-and-handoff.md",
    "mechanism-transfer.md",
    "orchestration.md",
    "validity-and-cognitive-economy.md",
}
FRONTMATTER = re.compile(r"\A---\n(?P<yaml>.*?)\n---\n(?P<body>.*)\Z", re.DOTALL)
STABLE_VERSION = re.compile(r"\A\d+\.\d+\.\d+\Z")


def digest_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def digest_path(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def file_bytes(root: Path) -> dict[str, bytes]:
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in sorted(item for item in root.rglob("*") if item.is_file())
    }


def make_read_only(root: Path) -> None:
    for path in sorted(root.rglob("*"), reverse=True):
        if path.is_file():
            path.chmod(stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)
        elif path.is_dir():
            path.chmod(
                stat.S_IRUSR
                | stat.S_IXUSR
                | stat.S_IRGRP
                | stat.S_IXGRP
                | stat.S_IROTH
                | stat.S_IXOTH
            )
    root.chmod(
        stat.S_IRUSR
        | stat.S_IXUSR
        | stat.S_IRGRP
        | stat.S_IXGRP
        | stat.S_IROTH
        | stat.S_IXOTH
    )


def writable_paths(root: Path) -> list[str]:
    return [
        path.relative_to(root).as_posix() or "."
        for path in [root, *root.rglob("*")]
        if path.is_file() or path.is_dir()
        if os.stat(path, follow_symlinks=False).st_mode & 0o222
    ]


def accepted_package(version: str) -> tuple[Path, dict[str, bytes]]:
    release = RELEASE_ROOT / version
    manifest_path = release / "manifest.yaml"
    package = release / "package" / PACKAGE_NAME
    if not release.is_dir() or release.is_symlink():
        raise ValueError(f"accepted release is missing or invalid: {release}")
    if not manifest_path.is_file() or manifest_path.is_symlink():
        raise ValueError(f"accepted release manifest is missing or invalid: {manifest_path}")
    if not package.is_dir() or package.is_symlink():
        raise ValueError(f"accepted package is missing or invalid: {package}")
    if any(path.is_symlink() for path in release.rglob("*")):
        raise ValueError("accepted release must not contain symlinks")

    manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    metadata = manifest.get("package", {})
    if metadata.get("name") != PACKAGE_NAME:
        raise ValueError("accepted release package name mismatch")
    if metadata.get("version") != version:
        raise ValueError("accepted release version mismatch")
    if metadata.get("state") != "accepted":
        raise ValueError("platform distributions require an accepted stable release")

    payload = file_bytes(package)
    manifest_hashes = {
        row.get("path"): row.get("sha256") for row in manifest.get("files", [])
    }
    payload_hashes = {path: digest_bytes(value) for path, value in payload.items()}
    if manifest_hashes != payload_hashes:
        raise ValueError("accepted release payload does not match its manifest")
    if any(Path(path).name in LEGACY_FILES for path in payload):
        raise ValueError("accepted release contains a rejected legacy filename")
    return package, payload


def claude_skill(source: bytes) -> bytes:
    text = source.decode("utf-8")
    match = FRONTMATTER.match(text)
    if not match:
        raise ValueError("SKILL.md frontmatter is malformed")
    metadata = yaml.safe_load(match.group("yaml"))
    if set(metadata) != {"name", "description"}:
        raise ValueError("SKILL.md frontmatter must contain only name and description")
    if metadata.get("name") != PACKAGE_NAME:
        raise ValueError("SKILL.md name does not match the package")
    description = metadata.get("description")
    if not isinstance(description, str) or description.count("Codex") != 1:
        raise ValueError("Codex source description must contain exactly one platform name")

    adapted = {
        "name": metadata["name"],
        "description": description.replace("Codex", "Claude"),
    }
    frontmatter = yaml.safe_dump(
        adapted,
        sort_keys=False,
        allow_unicode=True,
        width=4096,
    ).strip()
    output = f"---\n{frontmatter}\n---\n{match.group('body')}"
    if "Codex" in output:
        raise ValueError("Claude Code SKILL.md still contains a Codex-specific instruction")
    return output.encode("utf-8")


def expected_payloads(version: str) -> tuple[dict[str, bytes], dict[str, bytes]]:
    _, codex = accepted_package(version)
    if "SKILL.md" not in codex or "agents/openai.yaml" not in codex:
        raise ValueError("accepted Codex package lacks required platform files")
    unexpected_agents = sorted(
        path for path in codex if path.startswith("agents/") and path != "agents/openai.yaml"
    )
    if unexpected_agents:
        raise ValueError(f"unclassified Codex agent metadata: {unexpected_agents}")

    claude = {
        path: value for path, value in codex.items() if path != "agents/openai.yaml"
    }
    claude["SKILL.md"] = claude_skill(codex["SKILL.md"])
    return codex, claude


def write_zip(path: Path, payload: dict[str, bytes]) -> None:
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for relative, value in sorted(payload.items()):
            info = zipfile.ZipInfo(
                filename=f"{PACKAGE_NAME}/{relative}",
                date_time=(1980, 1, 1, 0, 0, 0),
            )
            info.create_system = 3
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = (stat.S_IFREG | 0o444) << 16
            archive.writestr(info, value)


def read_zip(path: Path) -> dict[str, bytes]:
    with zipfile.ZipFile(path) as archive:
        names = [item.filename for item in archive.infolist() if not item.is_dir()]
        if len(names) != len(set(names)):
            raise ValueError(f"duplicate archive entry in {path.name}")
        prefix = f"{PACKAGE_NAME}/"
        if any(not name.startswith(prefix) for name in names):
            raise ValueError(f"archive root mismatch in {path.name}")
        return {name.removeprefix(prefix): archive.read(name) for name in names}


def validate_frontmatter(skill: bytes, platform: str) -> list[str]:
    failures: list[str] = []
    text = skill.decode("utf-8")
    match = FRONTMATTER.match(text)
    if not match:
        return [f"{platform}: malformed SKILL.md frontmatter"]
    metadata = yaml.safe_load(match.group("yaml"))
    if set(metadata) != {"name", "description"}:
        failures.append(f"{platform}: frontmatter must contain only name and description")
    if metadata.get("name") != PACKAGE_NAME:
        failures.append(f"{platform}: skill name mismatch")
    expected_agent = "Codex" if platform == "codex" else "Claude"
    unexpected_agent = "Claude" if platform == "codex" else "Codex"
    description = metadata.get("description", "")
    if expected_agent not in description:
        failures.append(f"{platform}: description lacks {expected_agent} platform identity")
    if unexpected_agent in text:
        failures.append(f"{platform}: SKILL.md contains {unexpected_agent}-specific text")
    return failures


def validate_directory(root: Path, version: str, require_read_only: bool) -> list[str]:
    failures: list[str] = []
    manifest_path = root / "manifest.yaml"
    codex_archive = root / f"{PACKAGE_NAME}-{version}-codex.zip"
    claude_archive = root / f"{PACKAGE_NAME}-{version}-claude-code.zip"
    for path in (manifest_path, codex_archive, claude_archive):
        if not path.is_file() or path.is_symlink():
            failures.append(f"missing or invalid distribution artifact: {path.name}")
    if failures:
        return failures

    try:
        expected_codex, expected_claude = expected_payloads(version)
        actual_codex = read_zip(codex_archive)
        actual_claude = read_zip(claude_archive)
    except (OSError, ValueError, zipfile.BadZipFile, UnicodeDecodeError) as error:
        return [str(error)]

    if actual_codex != expected_codex:
        failures.append("Codex archive lacks byte-level parity with the accepted release")
    if actual_claude != expected_claude:
        failures.append("Claude Code archive differs from the deterministic adaptation")
    if "agents/openai.yaml" not in actual_codex:
        failures.append("Codex archive lacks agents/openai.yaml")
    if any(path.startswith("agents/") for path in actual_claude):
        failures.append("Claude Code archive contains Codex agent metadata")
    if any(Path(path).name in LEGACY_FILES for path in [*actual_codex, *actual_claude]):
        failures.append("a distribution contains a rejected legacy filename")

    failures.extend(validate_frontmatter(actual_codex["SKILL.md"], "codex"))
    failures.extend(validate_frontmatter(actual_claude["SKILL.md"], "claude-code"))

    manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("package") != {
        "name": PACKAGE_NAME,
        "version": version,
        "source_release": f"releases/{PACKAGE_NAME}/{version}",
        "state": "accepted-derived",
    }:
        failures.append("distribution manifest package metadata mismatch")
    rows = {row.get("platform"): row for row in manifest.get("distributions", [])}
    expected_rows = {
        "codex": (codex_archive, actual_codex),
        "claude-code": (claude_archive, actual_claude),
    }
    if set(rows) != set(expected_rows):
        failures.append("distribution manifest must contain Codex and Claude Code rows")
    else:
        for platform, (archive_path, payload) in expected_rows.items():
            row = rows[platform]
            if row.get("archive") != archive_path.name:
                failures.append(f"{platform}: archive name mismatch in manifest")
            if row.get("archive_sha256") != digest_path(archive_path):
                failures.append(f"{platform}: archive checksum mismatch in manifest")
            if row.get("runtime_files") != len(payload):
                failures.append(f"{platform}: runtime file count mismatch in manifest")
            if row.get("skill_sha256") != digest_bytes(payload["SKILL.md"]):
                failures.append(f"{platform}: SKILL.md checksum mismatch in manifest")

    if require_read_only:
        writable = writable_paths(root)
        if writable:
            failures.append(f"writable distribution paths found: {writable}")
    return failures


def build(version: str) -> None:
    if not STABLE_VERSION.match(version):
        raise SystemExit("platform distributions require a stable semantic version")
    destination = PLATFORM_ROOT / version
    if destination.exists() or destination.is_symlink():
        raise SystemExit(f"refusing to overwrite immutable distributions: {destination}")

    codex, claude = expected_payloads(version)
    PLATFORM_ROOT.mkdir(parents=True, exist_ok=True)
    temporary = Path(tempfile.mkdtemp(prefix=f".{version}-", dir=PLATFORM_ROOT))
    try:
        codex_archive = temporary / f"{PACKAGE_NAME}-{version}-codex.zip"
        claude_archive = temporary / f"{PACKAGE_NAME}-{version}-claude-code.zip"
        write_zip(codex_archive, codex)
        write_zip(claude_archive, claude)
        manifest = {
            "package": {
                "name": PACKAGE_NAME,
                "version": version,
                "source_release": f"releases/{PACKAGE_NAME}/{version}",
                "state": "accepted-derived",
            },
            "distributions": [
                {
                    "platform": "codex",
                    "archive": codex_archive.name,
                    "archive_sha256": digest_path(codex_archive),
                    "runtime_files": len(codex),
                    "skill_sha256": digest_bytes(codex["SKILL.md"]),
                    "excluded": [],
                },
                {
                    "platform": "claude-code",
                    "archive": claude_archive.name,
                    "archive_sha256": digest_path(claude_archive),
                    "runtime_files": len(claude),
                    "skill_sha256": digest_bytes(claude["SKILL.md"]),
                    "excluded": ["agents/openai.yaml"],
                    "adaptation": "SKILL.md description platform identity: Codex -> Claude",
                },
            ],
            "shared_payload": {
                "capability_contracts": 32,
                "domain_indexes": 9,
                "cross_cutting_references": 2,
                "references_byte_identical": True,
            },
        }
        (temporary / "manifest.yaml").write_text(
            yaml.safe_dump(manifest, sort_keys=False, allow_unicode=True),
            encoding="utf-8",
        )
        failures = validate_directory(temporary, version, require_read_only=False)
        if failures:
            raise ValueError("; ".join(failures))
        make_read_only(temporary)
        temporary.rename(destination)
    except Exception:
        if temporary.exists():
            for path in [temporary, *temporary.rglob("*")]:
                try:
                    path.chmod(0o700 if path.is_dir() else 0o600)
                except OSError:
                    pass
            shutil.rmtree(temporary)
        raise

    failures = validate_directory(destination, version, require_read_only=True)
    if failures:
        raise SystemExit("distribution post-build validation failed:\n- " + "\n- ".join(failures))
    print(f"created={destination}")
    print(f"codex_runtime_files={len(codex)}")
    print(f"claude_code_runtime_files={len(claude)}")
    print("references_byte_identical=true")
    print("writable_distribution_paths=0")


def validate(version: str) -> int:
    if not STABLE_VERSION.match(version):
        raise SystemExit("platform distributions require a stable semantic version")
    destination = PLATFORM_ROOT / version
    failures = validate_directory(destination, version, require_read_only=True)
    if failures:
        print("FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1
    manifest = yaml.safe_load((destination / "manifest.yaml").read_text(encoding="utf-8"))
    rows = {row["platform"]: row for row in manifest["distributions"]}
    print("PASS")
    print(f"release_version={version}")
    print(f"codex_runtime_files={rows['codex']['runtime_files']}")
    print(f"claude_code_runtime_files={rows['claude-code']['runtime_files']}")
    print("platform_distributions=2")
    print("references_byte_identical=true")
    print("legacy_filename_hits=0")
    print("writable_distribution_paths=0")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=("build", "validate"))
    parser.add_argument("version")
    args = parser.parse_args()
    if args.action == "build":
        build(args.version)
        return 0
    return validate(args.version)


if __name__ == "__main__":
    raise SystemExit(main())
