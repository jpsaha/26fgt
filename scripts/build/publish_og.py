#!/usr/bin/env python3

import shutil
from pathlib import Path

from scripts.config import (
    ASSETS_DIR,
    GENERATED_OG_DIR,
    TYPST_OG,
)


# ============================================================
# Publish generated Open Graph images
# ============================================================
#
# Copy:
#
#     generated/og/**/*.png
#
# to:
#
#     dist/assets/og/**/*.png
#
# The directory structure under generated/og/ is preserved.
#
# This operation is deliberately separate from prepare_dist().
#
# prepare_dist() prepares dist/ and handles committed/static
# assets.
#
# og-publish() is responsible only for publishing generated
# OG PNGs.
# ============================================================


def publish_og():
    """
    Publish generated OG PNG images to dist/assets/og/.

    Source:
        generated/og/**/*.png

    Destination:
        dist/assets/og/**/*.png

    The directory structure is preserved.
    """

    print("🖼️  Publishing Open Graph images...")

    # --------------------------------------------------------
    # Respect the effective OG configuration.
    #
    # Normally:
    #
    #     TYPST_OG=true
    #
    # for local OG generation.
    #
    # When false, committed OG images are used instead and
    # generated OG images must not be published.
    # --------------------------------------------------------

    if not TYPST_OG:

        print(
            "⏭️  TYPST_OG=false — "
            "generated OG images will not be published"
        )

        return

    # --------------------------------------------------------
    # Check source directory
    # --------------------------------------------------------

    if not GENERATED_OG_DIR.exists():

        print(
            f"ℹ️  No generated OG directory found: "
            f"{GENERATED_OG_DIR}"
        )

        return

    # --------------------------------------------------------
    # Destination
    # --------------------------------------------------------

    target_og_dir = ASSETS_DIR / "og"

    target_og_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    # --------------------------------------------------------
    # Copy PNG files
    # --------------------------------------------------------

    published_count = 0

    for source_png in GENERATED_OG_DIR.rglob("*.png"):

        relative_path = source_png.relative_to(
            GENERATED_OG_DIR
        )

        target_png = (
            target_og_dir
            / relative_path
        )

        target_png.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        shutil.copy2(
            source_png,
            target_png,
        )

        print(
            "📋 Published OG image: "
            f"{relative_path}"
        )

        published_count += 1

    # --------------------------------------------------------
    # Summary
    # --------------------------------------------------------

    if published_count == 0:

        print(
            "ℹ️  No generated OG PNG images found"
        )

    else:

        print(
            f"📋 Published {published_count} "
            f"generated OG image(s)"
        )


# ============================================================
# Entry point
# ============================================================

def main():
    publish_og()


if __name__ == "__main__":
    main()