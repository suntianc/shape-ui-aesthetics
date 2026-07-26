#!/usr/bin/env python3
"""Build and validate platform archives for the renovate-ui Runtime Package.

Thin façade over the shared per-skill packaging pipeline in
``tools/release/packaging.py``.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from tools.release.packaging import SPECS  # noqa: E402

SPEC = SPECS["renovate-ui"]


def main() -> int:
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=("build", "validate"))
    parser.add_argument("version")
    args = parser.parse_args()
    if args.action == "build":
        SPEC.build(args.version)
        return 0
    return SPEC.validate(args.version)


if __name__ == "__main__":
    raise SystemExit(main())
