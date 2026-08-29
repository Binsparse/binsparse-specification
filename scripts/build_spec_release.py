#!/usr/bin/env python3
"""Build release artifacts from a Bikeshed specification."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import re
import shutil
import subprocess

from semantic_version import Version

def run(*args: str) -> None:
    subprocess.run(args, check=True)


def read_spec_version(source: Path) -> str:
    macro = re.search(
        r"^Text Macro:\s+SPECVERSION\s+(\S+)\s*$",
        source.read_text(encoding="utf-8"),
        re.MULTILINE,
    )
    if macro is None:
        raise ValueError(f"{source} does not define Text Macro: SPECVERSION")
    try:
        return str(Version(macro.group(1)))
    except ValueError as error:
        raise ValueError(
            f"SPECVERSION in {source} is not valid Semantic Versioning"
        ) from error


def build(source: Path, output: Path) -> None:
    version = read_spec_version(source)
    output.mkdir(parents=True, exist_ok=True)

    artifact_name = f"binsparse-specification-{version}"
    source_artifact = output / f"{artifact_name}.bs"
    html_artifact = output / f"{artifact_name}.html"
    pdf_artifact = output / f"{artifact_name}.pdf"
    shutil.copy2(source, source_artifact)

    base_url = os.environ.get(
        "SITE_URL", "https://binsparse.github.io/binsparse-specification"
    ).rstrip("/")
    run(
        "bikeshed",
        "--no-update",
        "spec",
        f"--md-ED={base_url}/versions/{version}/",
        str(source_artifact),
        str(html_artifact),
    )
    run("weasyprint", str(html_artifact), str(pdf_artifact))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    build(args.source, args.output)


if __name__ == "__main__":
    main()
