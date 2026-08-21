#!/usr/bin/env python3
"""
Generate version switcher JSON files for documentation.

This module is the shared switcher generator used by docs workflows.
It generates a switcher.json file containing version information for a package.

Usage:
    generate_switcher.py --output PATH --package-path PATH
                        [--min-version VERSION] [--repo-path PATH]

Example:
    generate_switcher.py --output docs/_static/switcher.json \
                         --package-path /acoular \
                         --min-version v26.01 \
                         --repo-path ..
"""

import argparse
import json
import re
import subprocess
from pathlib import Path


def version_key(tag):
    match = re.match(r"v(\d+)\.(\d+)$", tag)
    if match:
        return (int(match.group(1)), int(match.group(2)))
    return (0, 0)


def normalize_version(tag):
    return tag.removeprefix("v")


def get_version_tags(
    repo_path=".",
    min_version="",
):
    """Get version tags from a git repository."""
    result = subprocess.run(
        ["git", "tag", "--merged", "HEAD", "--list", "v*"],
        capture_output=True,
        text=True,
        cwd=repo_path,
        check=True,
    )
    tags = result.stdout.strip().split("\n") if result.stdout.strip() else []

    filtered = sorted(
        [tag for tag in tags if re.match(r"^v\d+\.\d+$", tag)],
        key=version_key,
        reverse=True,
    )

    # Filter by min_version if specified
    if min_version:
        min_key = version_key(min_version)
        filtered = [tag for tag in filtered if version_key(tag) >= min_key]

    return filtered


def generate_switcher_json(
    output_path,
    package_path="/acoular",
    min_version="",
    repo_path=".",
):
    """
    Generate a version switcher JSON file.

    Args:
        output_path: Path to write the switcher.json file
        package_path: URL path for the package (e.g., '/acoular')
        min_version: Minimum version to include (e.g., 'v26.01')
        repo_path: Path to the git repository containing version tags

    Returns:
        Dictionary containing the generated versions
    """
    tags = get_version_tags(repo_path, min_version)

    versions = [
        {
            "name": "dev",
            "version": "dev",
            "url": f"{package_path}/dev/",
            "type": "branch",
        }
    ]

    latest_stable = None
    for tag in tags:
        if latest_stable is None:
            latest_stable = tag
            versions.insert(
                1,
                {
                    "name": f"{tag} (stable)",
                    "version": normalize_version(tag),
                    "url": f"{package_path}/",
                    "type": "tag",
                    "preferred": True,
                },
            )
        else:
            versions.append(
                {
                    "name": tag,
                    "version": normalize_version(tag),
                    "url": f"{package_path}/{tag}/",
                    "type": "tag",
                }
            )

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w") as f:
        json.dump(versions, f, indent=2)

    return {
        "versions": versions,
        "count": len(versions),
        "latest_stable": latest_stable,
    }


def main():
    """Parse command line arguments and generate switcher.json."""
    parser = argparse.ArgumentParser(
        description="Generate version switcher JSON for documentation",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "--output",
        required=True,
        help="Output path for switcher.json file",
    )
    parser.add_argument(
        "--package-path",
        required=True,
        help="URL path for the package (e.g., '/acoular')",
    )
    parser.add_argument(
        "--min-version",
        default="",
        help="Minimum version to include (e.g., 'v26.01')",
    )
    parser.add_argument(
        "--repo-path",
        default=".",
        help="Path to the git repository containing version tags",
    )

    args = parser.parse_args()

    try:
        result = generate_switcher_json(
            output_path=args.output,
            package_path=args.package_path,
            min_version=args.min_version,
            repo_path=args.repo_path,
        )

        print(f"✓ Generated {result['count']} versions")
        print(f"  Latest stable: {result['latest_stable']}")
        print(f"  Output: {args.output}")
        return 0

    except Exception as e:
        print(f"✗ Error generating switcher.json: {e}")
        import traceback

        traceback.print_exc()
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
