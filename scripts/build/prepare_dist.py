#!/usr/bin/env python3

import shutil

from scripts.config import (
    DIST_DIR,
    PAGES_DIR,
    PDF_DIR,
    ASSETS_DIR,
    ASSETS_SOURCE_DIR,
    HOMEPAGE_JSON,
)


def prepare_dist():
    """Prepare the dist directory for a fresh build."""

    # --------------------------------------------------------
    # Remove previous generated output
    # --------------------------------------------------------

    shutil.rmtree(
        DIST_DIR,
        ignore_errors=True,
    )

    # --------------------------------------------------------
    # Create output directories
    # --------------------------------------------------------

    for directory in (
        PAGES_DIR,
        PDF_DIR,
        ASSETS_DIR / "css",
        ASSETS_DIR / "js",
        ASSETS_DIR / "images",
    ):
        directory.mkdir(
            parents=True,
            exist_ok=True,
        )

    # --------------------------------------------------------
    # Copy assets
    # --------------------------------------------------------

    source_css = ASSETS_SOURCE_DIR / "css" / "style.css"
    target_css = ASSETS_DIR / "css" / "style.css"

    if source_css.exists():

        shutil.copy2(
            source_css,
            target_css,
        )

        print("📋 Copied style.css")

    else:

        print(
            "⚠️ Warning: assets/css/style.css not found"
        )

    # --------------------------------------------------------
    # Check generated metadata
    # --------------------------------------------------------

    if not HOMEPAGE_JSON.exists():

        raise FileNotFoundError(
            f"Missing {HOMEPAGE_JSON}"
        )


def main():
    prepare_dist()


if __name__ == "__main__":
    main()