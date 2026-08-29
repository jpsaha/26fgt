#!/usr/bin/env python3

"""
Build Open Graph PNG images from generated Asymptote sources.

Input:
    generated/og/**/*.asy

Output:
    generated/og/**/*.png

The directory structure is preserved.

Example:

    generated/og/lectures_dummy/lec1.asy
        ↓
    generated/og/lectures_dummy/lec1.png

Requirements:
    - Asymptote (`asy`)
    - ImageMagick (`magick`)
"""

import subprocess

from scripts.config import (
    ROOT,
    GENERATED_OG_DIR,
    OG_WIDTH,
    OG_HEIGHT,
    OG_DENSITY,
)


# ============================================================
# Open Graph source directory
# ============================================================
#
# Generated Asymptote sources are stored under:
#
#     generated/og/
#
# The directory structure of the corresponding content source
# is preserved.
#
# Example:
#
#     content/gt/lec1.typ
#             ↓
#     generated/og/gt/lec1.asy
#
#     content/mopss/mopss_aug29.typ
#             ↓
#     generated/og/mopss/mopss_aug29.asy
# ============================================================


# ============================================================
# Open Graph image settings
# ============================================================
#
# These values are defined centrally in scripts/config.py.
#
# OG_WIDTH
#     Final PNG width in pixels.
#
# OG_HEIGHT
#     Final PNG height in pixels.
#
# OG_DENSITY
#     Resolution used when rasterizing the intermediate
#     Asymptote-generated PDF.
# ============================================================


# ============================================================
# Rasterization density
# ============================================================
#
# Asymptote first produces the OG artwork as a PDF.
# ImageMagick then rasterizes that PDF to PNG.
#
# A higher density gives ImageMagick more source resolution
# before the final 1200 × 630 resize.
# ============================================================

# ============================================================
# Build one OG image
# ============================================================

def build_og_image(source):
    """
    Convert one Asymptote source into a 1200×630 PNG.

    The PNG is rebuilt only when:
        - it does not exist, or
        - the .asy source is newer than the PNG.
    """

    # --------------------------------------------------------
    # Determine output location
    #
    # Generated OG sources:
    #
    #     generated/og/fgt/lec1.asy
    #         →
    #     generated/og/fgt/lec1.png
    #
    # Default OG source:
    #
    #     assets/og/default.asy
    #         →
    #     assets/og/default.png
    # --------------------------------------------------------

    output_base = source.with_suffix("")
    pdf = output_base.with_suffix(".pdf")
    png = output_base.with_suffix(".png")

    # --------------------------------------------------------
    # Incremental check
    # --------------------------------------------------------

    if png.exists() and png.stat().st_mtime >= source.stat().st_mtime:
        print(
            f"⏭️  Skipping "
            f"{source.relative_to(ROOT)}"
            f" — PNG is up to date"
        )
        return False

    # --------------------------------------------------------
    # Ensure output directory exists
    # --------------------------------------------------------

    output_base.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    relative = source.relative_to(ROOT)

    # --------------------------------------------------------
    # Asymptote → PDF
    # --------------------------------------------------------

    print(
        f"📐 Building {relative}"
    )

    subprocess.run(
        [
            "asy",
            "-f",
            "pdf",
            "-o",
            str(output_base),
            str(source),
        ],
        check=True,
    )

    # --------------------------------------------------------
    # PDF → PNG
    # --------------------------------------------------------

    print(
        f"🖼️  Converting "
        f"{pdf.relative_to(ROOT)}"
        f" → "
        f"{png.relative_to(ROOT)}"
    )

    subprocess.run(
        [
            "magick",
            "-density",
            str(OG_DENSITY),
            str(pdf),
            "-resize",
            f"{OG_WIDTH}x{OG_HEIGHT}!",
            "-filter",
            "Lanczos",
            str(png),
        ],
        check=True,
    )

    # --------------------------------------------------------
    # Remove intermediate PDF
    # --------------------------------------------------------

    if pdf.exists():
        pdf.unlink()

    # --------------------------------------------------------
    # Verify output
    # --------------------------------------------------------

    if not png.exists():
        raise RuntimeError(
            f"PNG was not created: {png}"
        )

    print(
        f"✅ Created "
        f"{png.relative_to(ROOT)}"
    )

    return True


# ============================================================
# Main
# ============================================================

def main():

    # ========================================================
    # Collect OG sources
    # ========================================================

    sources = []

    # --------------------------------------------------------
    # Default OG image
    #
    # This is a manually maintained source asset.
    # --------------------------------------------------------

    # default_source = (
    #     ASSETS_SOURCE_DIR / "og" / "default.asy"
    # )

    # if default_source.exists():
    #     sources.append(default_source)

    # --------------------------------------------------------
    # Generated OG images
    # --------------------------------------------------------

    if GENERATED_OG_DIR.exists():
        sources.extend(
            sorted(
                GENERATED_OG_DIR.rglob("*.asy")
            )
        )

    # --------------------------------------------------------
    # Nothing to build
    # --------------------------------------------------------

    if not sources:
        print(
            "ℹ️  No OG .asy files found."
        )
        return

    print(
        f"📐 Found {len(sources)} OG source(s)"
    )

    print()

    # ========================================================
    # Build images
    # ========================================================

    built = 0
    skipped = 0

    for source in sources:

        if build_og_image(source):
            built += 1
        else:
            skipped += 1

        print()

    # ========================================================
    # Summary
    # ========================================================

    print(
        "OG image generation complete."
    )

    print(
        f"Built     : {built}"
    )

    print(
        f"Skipped   : {skipped}"
    )

# ============================================================
# Entry point
# ============================================================

if __name__ == "__main__":
    main()