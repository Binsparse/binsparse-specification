#!/usr/bin/env python3
"""Check whether a SemVer version may be published as a new release."""

from __future__ import annotations

import argparse
from pathlib import Path
import subprocess

from semantic_version import Version

from build_spec_release import read_spec_version


def existing_tags() -> list[str]:
    result = subprocess.run(
        ["git", "tag", "--list"],
        check=True,
        text=True,
        stdout=subprocess.PIPE,
    )
    return result.stdout.splitlines()


def check_release_version(source: Path, tags: list[str]) -> str:
    requested = Version(read_spec_version(source))
    requested_tag = f"v{requested}"
    if requested_tag in tags:
        raise ValueError(f"release tag {requested_tag} already exists")

    existing: list[tuple[Version, str]] = []
    for tag in tags:
        if not tag.startswith("v"):
            continue
        try:
            parsed = Version(tag[1:])
        except ValueError:
            continue
        existing.append((parsed, tag))

    if not existing:
        return str(requested)

    highest, highest_tag = max(existing, key=lambda item: item[0])
    if not requested > highest:
        raise ValueError(
            f"release {requested_tag} must be greater than the current highest "
            f"release {highest_tag}"
        )
    return str(requested)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path, help="Bikeshed specification to release")
    args = parser.parse_args()
    print(check_release_version(args.source, existing_tags()))


if __name__ == "__main__":
    main()
