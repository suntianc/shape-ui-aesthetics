"""Shared platform-distribution builder/validator for any public Runtime Package."""

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
STABLE_VERSION = re.compile(r"\A\d+\.\d+\.\d+\Z")
FRONTMATTER = re.compile(r"\A---\n(?P<yaml>.*?)\n---\n(?P<body>.*)\Z", re.DOTALL)


def _digest_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _digest_path(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _file_bytes(root: Path) -> dict[str, bytes]:
    return {
        p.relative_to(root).as_posix(): p.read_bytes()
        for p in sorted(item for item in root.rglob("*") if item.is_file())
    }


def _make_read_only(root: Path) -> None:
    for p in sorted(root.rglob("*"), reverse=True):
        if p.is_file():
            p.chmod(stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)
        elif p.is_dir():
            p.chmod(0o555)
    root.chmod(0o555)


def _writable_paths(root: Path) -> list[str]:
    return [
        p.relative_to(root).as_posix() or "."
        for p in [root, *root.rglob("*")]
        if (p.is_file() or p.is_dir()) and os.stat(p, follow_symlinks=False).st_mode & 0o222
    ]


class PackageSpec:
    """Per-skill configuration for the shared packaging pipeline."""

    def __init__(self, name: str, legacy_files: set[str] | None = None,
                 shared_payload: dict | None = None, pure_portable: bool = False):
        self.name = name
        self.release_root = ROOT / "releases" / name
        self.distribution_root = self.release_root / "distributions"
        self.legacy_files = legacy_files or set()
        self.shared_payload = shared_payload or {}
        # pure_portable: skill ships no platform-specific agent metadata; both archives are identical.
        self.pure_portable = pure_portable

    def accepted_package(self, version: str) -> tuple[Path, dict[str, bytes]]:
        release = self.release_root / version
        manifest_path = release / "manifest.yaml"
        package = release / "package" / self.name
        if not release.is_dir() or release.is_symlink():
            raise ValueError(f"accepted release is missing or invalid: {release}")
        if not manifest_path.is_file() or manifest_path.is_symlink():
            raise ValueError(f"accepted release manifest is missing or invalid: {manifest_path}")
        if not package.is_dir() or package.is_symlink():
            raise ValueError(f"accepted package is missing or invalid: {package}")
        if any(p.is_symlink() for p in release.rglob("*")):
            raise ValueError("accepted release must not contain symlinks")
        manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
        metadata = manifest.get("package", {})
        if metadata.get("name") != self.name:
            raise ValueError("accepted release package name mismatch")
        if metadata.get("version") != version:
            raise ValueError("accepted release version mismatch")
        if metadata.get("state") != "accepted":
            raise ValueError("platform distributions require an accepted stable release")
        payload = _file_bytes(package)
        manifest_hashes = {row.get("path"): row.get("sha256") for row in manifest.get("files", [])}
        payload_hashes = {p: _digest_bytes(v) for p, v in payload.items()}
        if manifest_hashes != payload_hashes:
            raise ValueError("accepted release payload does not match its manifest")
        if any(Path(p).name in self.legacy_files for p in payload):
            raise ValueError("accepted release contains a rejected legacy filename")
        return package, payload

    def _skill_document(self, source: bytes) -> tuple[dict, str, str]:
        text = source.decode("utf-8")
        m = FRONTMATTER.match(text)
        if not m:
            raise ValueError("SKILL.md frontmatter is malformed")
        metadata = yaml.safe_load(m.group("yaml"))
        if not isinstance(metadata, dict) or set(metadata) != {"name", "description"}:
            raise ValueError("SKILL.md frontmatter must contain only name and description")
        if metadata.get("name") != self.name:
            raise ValueError("SKILL.md name does not match the package")
        desc = metadata.get("description")
        if not isinstance(desc, str) or not desc.strip():
            raise ValueError("SKILL.md description is missing")
        return metadata, m.group("body"), text

    def _is_portable(self, source: bytes) -> bool:
        _, _, text = self._skill_document(source)
        return "Codex" not in text and "Claude" not in text

    def expected_payloads(self, version: str) -> tuple[dict[str, bytes], dict[str, bytes]]:
        _, codex = self.accepted_package(version)
        if "SKILL.md" not in codex:
            raise ValueError("accepted package lacks SKILL.md")
        if not self._is_portable(codex["SKILL.md"]):
            raise ValueError("accepted Runtime Package SKILL.md must be platform-neutral")
        if self.pure_portable:
            unexpected = sorted(p for p in codex if p.startswith("agents/"))
            if unexpected:
                raise ValueError(f"pure-portable package must not carry agent metadata: {unexpected}")
            return codex, codex
        if "agents/openai.yaml" not in codex:
            raise ValueError("accepted Codex package lacks required platform files")
        unexpected = sorted(p for p in codex if p.startswith("agents/") and p != "agents/openai.yaml")
        if unexpected:
            raise ValueError(f"unclassified Codex agent metadata: {unexpected}")
        claude = {p: v for p, v in codex.items() if p != "agents/openai.yaml"}
        return codex, claude

    def _write_zip(self, path: Path, payload: dict[str, bytes]) -> None:
        with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
            for relative, value in sorted(payload.items()):
                info = zipfile.ZipInfo(
                    filename=f"{self.name}/{relative}",
                    date_time=(1980, 1, 1, 0, 0, 0),
                )
                info.create_system = 3
                info.compress_type = zipfile.ZIP_DEFLATED
                info.external_attr = (stat.S_IFREG | 0o444) << 16
                archive.writestr(info, value)

    def _read_zip(self, path: Path) -> dict[str, bytes]:
        with zipfile.ZipFile(path) as archive:
            names = [item.filename for item in archive.infolist() if not item.is_dir()]
            if len(names) != len(set(names)):
                raise ValueError(f"duplicate archive entry in {path.name}")
            prefix = f"{self.name}/"
            if any(not n.startswith(prefix) for n in names):
                raise ValueError(f"archive root mismatch in {path.name}")
            return {n.removeprefix(prefix): archive.read(n) for n in names}

    def _validate_frontmatter(self, skill: bytes, platform: str) -> list[str]:
        failures: list[str] = []
        text = skill.decode("utf-8")
        m = FRONTMATTER.match(text)
        if not m:
            return [f"{platform}: malformed SKILL.md frontmatter"]
        metadata = yaml.safe_load(m.group("yaml"))
        if not isinstance(metadata, dict) or set(metadata) != {"name", "description"}:
            return [f"{platform}: frontmatter must contain only name and description"]
        if metadata.get("name") != self.name:
            failures.append(f"{platform}: skill name mismatch")
        desc = metadata.get("description", "")
        if not isinstance(desc, str) or not desc.strip():
            failures.append(f"{platform}: description is missing")
            return failures
        if "Codex" in text or "Claude" in text:
            failures.append(f"{platform}: SKILL.md must be platform-neutral")
        return failures

    def validate_directory(self, root: Path, version: str, require_read_only: bool) -> list[str]:
        failures: list[str] = []
        manifest_path = root / "manifest.yaml"
        codex_archive = root / f"{self.name}-{version}-codex.zip"
        claude_archive = root / f"{self.name}-{version}-claude-code.zip"
        for path in (manifest_path, codex_archive, claude_archive):
            if not path.is_file() or path.is_symlink():
                failures.append(f"missing or invalid distribution artifact: {path.name}")
        if failures:
            return failures
        try:
            expected_codex, expected_claude = self.expected_payloads(version)
            actual_codex = self._read_zip(codex_archive)
            actual_claude = self._read_zip(claude_archive)
        except (OSError, ValueError, zipfile.BadZipFile, UnicodeDecodeError) as error:
            return [str(error)]
        if actual_codex != expected_codex:
            failures.append("Codex archive lacks byte-level parity with the accepted release")
        if actual_claude != expected_claude:
            failures.append("Claude Code archive differs from the deterministic platform payload")
        if not self.pure_portable:
            if "agents/openai.yaml" not in actual_codex:
                failures.append("Codex archive lacks agents/openai.yaml")
            if any(p.startswith("agents/") for p in actual_claude):
                failures.append("Claude Code archive contains Codex agent metadata")
        else:
            if any(p.startswith("agents/") for p in actual_codex) or any(p.startswith("agents/") for p in actual_claude):
                failures.append("pure-portable distribution carries agent metadata")
        if any(Path(p).name in self.legacy_files for p in [*actual_codex, *actual_claude]):
            failures.append("a distribution contains a rejected legacy filename")
        failures.extend(self._validate_frontmatter(actual_codex["SKILL.md"], "codex"))
        failures.extend(self._validate_frontmatter(actual_claude["SKILL.md"], "claude-code"))
        manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
        if manifest.get("package") != {
            "name": self.name,
            "version": version,
            "source_release": f"releases/{self.name}/{version}",
            "state": "accepted-derived",
        }:
            failures.append("distribution manifest package metadata mismatch")
        rows = {row.get("platform"): row for row in manifest.get("distributions", [])}
        expected_rows = {"codex": (codex_archive, actual_codex), "claude-code": (claude_archive, actual_claude)}
        if set(rows) != set(expected_rows):
            failures.append("distribution manifest must contain Codex and Claude Code rows")
        else:
            for platform, (archive_path, payload) in expected_rows.items():
                row = rows[platform]
                if row.get("archive") != archive_path.name:
                    failures.append(f"{platform}: archive name mismatch in manifest")
                if row.get("archive_sha256") != _digest_path(archive_path):
                    failures.append(f"{platform}: archive checksum mismatch in manifest")
                if row.get("runtime_files") != len(payload):
                    failures.append(f"{platform}: runtime file count mismatch in manifest")
                if row.get("skill_sha256") != _digest_bytes(payload["SKILL.md"]):
                    failures.append(f"{platform}: SKILL.md checksum mismatch in manifest")
        shared = manifest.get("shared_payload", {})
        if "skill_byte_identical" in shared:
            actual = actual_codex["SKILL.md"] == actual_claude["SKILL.md"]
            if shared.get("skill_byte_identical") is not actual:
                failures.append("shared payload SKILL.md parity record mismatch")
        if require_read_only:
            w = _writable_paths(root)
            if w:
                failures.append(f"writable distribution paths found: {w}")
        return failures

    def build(self, version: str) -> None:
        if not STABLE_VERSION.match(version):
            raise SystemExit("platform distributions require a stable semantic version")
        destination = self.distribution_root / version
        if destination.exists() or destination.is_symlink():
            raise SystemExit(f"refusing to overwrite immutable distributions: {destination}")
        codex, claude = self.expected_payloads(version)
        portable = codex["SKILL.md"] == claude["SKILL.md"]
        self.distribution_root.mkdir(parents=True, exist_ok=True)
        temporary = Path(tempfile.mkdtemp(prefix=f".{self.name}-{version}-", dir=self.distribution_root))
        try:
            codex_archive = temporary / f"{self.name}-{version}-codex.zip"
            claude_archive = temporary / f"{self.name}-{version}-claude-code.zip"
            self._write_zip(codex_archive, codex)
            self._write_zip(claude_archive, claude)
            manifest = {
                "package": {
                    "name": self.name,
                    "version": version,
                    "source_release": f"releases/{self.name}/{version}",
                    "state": "accepted-derived",
                },
                "distributions": [
                    {"platform": "codex", "archive": codex_archive.name,
                     "archive_sha256": _digest_path(codex_archive), "runtime_files": len(codex),
                     "skill_sha256": _digest_bytes(codex["SKILL.md"]), "excluded": []},
                    {"platform": "claude-code", "archive": claude_archive.name,
                     "archive_sha256": _digest_path(claude_archive), "runtime_files": len(claude),
                     "skill_sha256": _digest_bytes(claude["SKILL.md"]),
                     "excluded": [] if self.pure_portable else ["agents/openai.yaml"],
                     "adaptation": "identical to Codex (pure-portable skill)" if self.pure_portable
                                   else "omit Codex-only agents/openai.yaml; preserve portable SKILL.md"},
                ],
                "shared_payload": {**self.shared_payload, "skill_byte_identical": portable},
            }
            (temporary / "manifest.yaml").write_text(
                yaml.safe_dump(manifest, sort_keys=False, allow_unicode=True), encoding="utf-8")
            failures = self.validate_directory(temporary, version, require_read_only=False)
            if failures:
                raise ValueError("; ".join(failures))
            _make_read_only(temporary)
            temporary.rename(destination)
        except Exception:
            if temporary.exists():
                for p in [temporary, *temporary.rglob("*")]:
                    try:
                        p.chmod(0o700 if p.is_dir() else 0o600)
                    except OSError:
                        pass
                shutil.rmtree(temporary)
            raise
        failures = self.validate_directory(destination, version, require_read_only=True)
        if failures:
            raise SystemExit("distribution post-build validation failed:\n- " + "\n- ".join(failures))
        print(f"created={destination}")
        print(f"codex_runtime_files={len(codex)}")
        print(f"claude_code_runtime_files={len(claude)}")
        print(f"portable_skill={str(portable).lower()}")
        print("references_byte_identical=true")
        print("writable_distribution_paths=0")

    def validate(self, version: str) -> int:
        if not STABLE_VERSION.match(version):
            raise SystemExit("platform distributions require a stable semantic version")
        destination = self.distribution_root / version
        if not destination.is_dir() or destination.is_symlink():
            raise SystemExit(f"distribution directory is missing or invalid: {destination}")
        failures = self.validate_directory(destination, version, require_read_only=True)
        if failures:
            print("FAIL")
            for f in failures:
                print(f"- {f}")
            return 1
        manifest = yaml.safe_load((destination / "manifest.yaml").read_text(encoding="utf-8"))
        rows = {row["platform"]: row for row in manifest["distributions"]}
        shared = manifest.get("shared_payload", {})
        print("PASS")
        print(f"release_version={version}")
        print(f"codex_runtime_files={rows['codex']['runtime_files']}")
        print(f"claude_code_runtime_files={rows['claude-code']['runtime_files']}")
        print("platform_distributions=2")
        print(f"portable_skill={str(bool(shared.get('skill_byte_identical'))).lower()}")
        print("writable_distribution_paths=0")
        return 0


# Per-skill configurations (keepaligned with the public roster in validate_repository.py)
SPECS: dict[str, PackageSpec] = {
    "shape-ui-aesthetics": PackageSpec(
        "shape-ui-aesthetics",
        legacy_files={
            "aesthetic-generation.md", "collision-and-direction.md", "design-grammar-and-handoff.md",
            "mechanism-transfer.md", "orchestration.md", "validity-and-cognitive-economy.md",
        },
        shared_payload={"capability_contracts": 32, "domain_indexes": 9, "cross_cutting_references": 2,
                        "references_byte_identical": True},
    ),
    "renovate-ui": PackageSpec(
        "renovate-ui",
        legacy_files=set(),
        shared_payload={},
        pure_portable=True,
    ),
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=("build", "validate"))
    parser.add_argument("skill", choices=sorted(SPECS))
    parser.add_argument("version")
    args = parser.parse_args()
    spec = SPECS[args.skill]
    if args.action == "build":
        spec.build(args.version)
        return 0
    return spec.validate(args.version)


if __name__ == "__main__":
    raise SystemExit(main())
