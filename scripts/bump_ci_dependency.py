#!/usr/bin/env python3
"""Update Acoular CI Git-tag pins in every project manifest below a root."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

SKIP_DIRS = {".git", ".venv", "build", "dist", "node_modules"}
CI_URL = r"https://github\.com/acoular/ci\.git"


def manifests(root: Path) -> list[Path]:
    return [
        path
        for path in root.rglob("pyproject.toml")
        if not any(part in SKIP_DIRS for part in path.relative_to(root).parts)
    ]


def update_manifest(path: Path, package: str, tag: str) -> bool:
    """Replace only this package's Acoular CI tag pin, preserving TOML style."""
    text = path.read_text()
    escaped_package = re.escape(package)
    tag_prefix = re.escape(tag.split("-v", maxsplit=1)[0])
    patterns = (
        rf"(?P<package>{escaped_package}\s*@\s*git\+{CI_URL}@){tag_prefix}-v[\w.-]+",
        rf'(?P<package>{escaped_package}\s*=\s*\{{[^}}]*git\s*=\s*"{CI_URL}"[^}}]*tag\s*=\s*"){tag_prefix}-v[\w.-]+',
    )
    updated = text
    for pattern in patterns:
        updated = re.sub(pattern, rf"\g<package>{tag}", updated)
    if updated == text:
        return False
    path.write_text(updated)
    return True


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--package", required=True)
    parser.add_argument("--tag", required=True)
    args = parser.parse_args()

    if "-v" not in args.tag:
        parser.error("tag must contain -v")

    changed = [
        path.relative_to(args.root)
        for path in manifests(args.root)
        if update_manifest(path, args.package, args.tag)
    ]
    print("\n".join(map(str, changed)))


if __name__ == "__main__":
    main()
