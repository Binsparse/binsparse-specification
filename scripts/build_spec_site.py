#!/usr/bin/env python3
"""Build the draft and immutable GitHub Release artifacts for GitHub Pages."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

from semantic_version import Version

from build_spec_release import read_spec_version


def run(*args: str, capture: bool = False) -> str:
    result = subprocess.run(
        args,
        check=True,
        text=True,
        stdout=subprocess.PIPE if capture else None,
    )
    return result.stdout.strip() if capture else ""


def github_releases(repository: str) -> list[tuple[Version, str]]:
    raw = run(
        "gh",
        "release",
        "list",
        "--repo",
        repository,
        "--limit",
        "1000",
        "--json",
        "tagName,isDraft",
        capture=True,
    )
    releases: list[tuple[Version, str]] = []
    for release in json.loads(raw):
        tag = release["tagName"]
        if release["isDraft"] or not tag.startswith("v"):
            continue
        try:
            version = Version(tag[1:])
        except ValueError:
            continue
        releases.append((version, tag))
    return sorted(
        releases,
        key=lambda item: (item[0], item[1]),
        reverse=True,
    )


def build_draft(source: Path, destination: Path, base_url: str) -> None:
    destination.mkdir(parents=True)
    shutil.copy2(source, destination / "index.bs")
    run(
        "bikeshed",
        "--no-update",
        "spec",
        f"--md-ED={base_url}/versions/draft/",
        str(source),
        str(destination / "index.html"),
    )
    run("weasyprint", str(destination / "index.html"), str(destination / "index.pdf"))


def download_release(
    repository: str, version: Version, tag: str, destination: Path
) -> None:
    destination.mkdir(parents=True)
    artifact_name = f"binsparse-specification-{version}"
    with tempfile.TemporaryDirectory(prefix="binsparse-release-") as temp_name:
        temp = Path(temp_name)
        run(
            "gh",
            "release",
            "download",
            tag,
            "--repo",
            repository,
            "--dir",
            str(temp),
            "--pattern",
            f"{artifact_name}.*",
        )
        for extension in ("bs", "html", "pdf"):
            artifact = temp / f"{artifact_name}.{extension}"
            if not artifact.is_file():
                raise FileNotFoundError(f"GitHub Release {tag} is missing {artifact.name}")
            shutil.copy2(artifact, destination / f"index.{extension}")


def build_site(
    source: Path, template: Path, output: Path, repository: str, base_url: str
) -> None:
    read_spec_version(source)
    if output.exists():
        shutil.rmtree(output)
    shutil.copytree(template, output)
    versions_dir = output / "versions"
    releases = github_releases(repository)

    build_draft(source, versions_dir / "draft", base_url)
    for version, tag in releases:
        download_release(repository, version, tag, versions_dir / str(version))

    stable_versions = [version for version, _tag in releases if not version.prerelease]
    latest = stable_versions[0] if stable_versions else None
    data = {
        "latest_stable": str(latest) if latest is not None else None,
        "redirect": f"versions/{latest}/" if latest is not None else "versions/draft/",
        "releases": [
            {
                "version": str(version),
                "prerelease": bool(version.prerelease),
            }
            for version, _tag in releases
        ],
    }
    data_dir = output / "_data"
    data_dir.mkdir()
    (data_dir / "versions.json").write_text(
        json.dumps(data, indent=2) + "\n", encoding="utf-8"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("--template", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    repository = os.environ["GITHUB_REPOSITORY"]
    base_url = os.environ.get(
        "SITE_URL", f"https://{repository.split('/', 1)[0]}.github.io/{repository.split('/', 1)[1]}"
    ).rstrip("/")
    build_site(args.source, args.template, args.output, repository, base_url)


if __name__ == "__main__":
    main()
