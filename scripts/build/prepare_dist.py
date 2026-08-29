#!/usr/bin/env python3

import shutil
import tempfile
from pathlib import Path

from scripts.config import (
    DIST_DIR,
    PAGES_DIR,
    PDF_DIR,
    ASSETS_DIR,
    ASSETS_SOURCE_DIR,
    HOMEPAGE_JSON,
    TYPST_OG,
)


# ============================================================
# Helpers
# ============================================================

def preserve_committed_og():
    """
    Preserve existing dist/assets/og/*.png files.

    This is used only when:

        TYPST_OG=false

    In that mode the OG PNGs are already committed to Git and
    must survive the cleaning of dist/.
    """

    existing_og_dir = ASSETS_DIR / "og"

    if not existing_og_dir.exists():
        print(
            "⚠️ No existing dist/assets/og/ directory found"
        )
        return None

    temp_root = Path(
        tempfile.mkdtemp(
            prefix="typst-og-"
        )
    )

    preserved_og_dir = temp_root / "og"

    shutil.copytree(
        existing_og_dir,
        preserved_og_dir,
    )

    count = sum(
        1
        for path in preserved_og_dir.rglob("*.png")
    )

    print(
        f"📦 Preserved {count} committed OG image(s)"
    )

    return preserved_og_dir


# ============================================================
# Main preparation
# ============================================================

def prepare_dist():
    """
    Prepare dist/ for a fresh build.

    TYPST_OG=true
        ----------------
        Remove dist completely.
        Static assets are copied from assets/.
        Generated OG images are NOT copied here.
        They are published separately by og-publish.

    TYPST_OG=false
        ----------------
        Preserve existing committed OG PNGs.
        Remove dist.
        Restore the committed OG PNGs.
        Do not use generated/og/.
    """

    print(
        f"🖼️  TYPST_OG = {TYPST_OG}"
    )

    # ========================================================
    # Preserve committed OG images
    #
    # Only necessary when OG generation is disabled.
    # ========================================================

    preserved_og_dir = None

    if not TYPST_OG:
        preserved_og_dir = preserve_committed_og()

    # ========================================================
    # Remove previous dist
    # ========================================================

    shutil.rmtree(
        DIST_DIR,
        ignore_errors=True,
    )

    # ========================================================
    # Create output directories
    # ========================================================

    for directory in (
        PAGES_DIR,
        PDF_DIR,
        ASSETS_DIR / "css",
        ASSETS_DIR / "js",
        ASSETS_DIR / "images",
        ASSETS_DIR / "og",
    ):
        directory.mkdir(
            parents=True,
            exist_ok=True,
        )

    # ========================================================
    # Restore committed OG images
    #
    # This happens only when:
    #
    #     TYPST_OG=false
    #
    # The images were committed in Git and existed in dist/
    # before this preparation step deleted dist/.
    # ========================================================

    if preserved_og_dir is not None:

        # Restore the preserved OG directory.
        #
        # The destination directory already exists because it was
        # created above. Copy the files individually so that this
        # works with older Python versions as well.

        for source_png in preserved_og_dir.rglob("*.png"):

            relative_path = source_png.relative_to(
                preserved_og_dir
            )

            target_png = (
                ASSETS_DIR
                / "og"
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
            "📋 Restored committed OG images"
        )

        # Remove temporary preservation directory.

        shutil.rmtree(
            preserved_og_dir.parent,
            ignore_errors=True,
        )

    # ========================================================
    # Copy CSS
    # ========================================================

    source_css_dir = (
        ASSETS_SOURCE_DIR
        / "css"
    )

    target_css_dir = (
        ASSETS_DIR
        / "css"
    )

    target_css_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    if source_css_dir.exists():

        css_files = sorted(
            source_css_dir.glob("*.css")
        )

        for source_css in css_files:

            target_css = (
                target_css_dir
                / source_css.name
            )

            shutil.copy2(
                source_css,
                target_css,
            )

            print(
                f"📋 Copied {source_css.name}"
            )

    else:

        print(
            "⚠️ Warning: assets/css directory not found"
        )

    # ========================================================
    # Copy project-supplied PNG images
    #
    # These come from:
    #
    #     assets/**/*.png
    #
    # They are NOT generated by the OG pipeline.
    #
    # Example:
    #
    #     assets/og/default.png
    #     assets/og/fgt1.png
    #
    # They are copied into:
    #
    #     dist/assets/og/
    #
    # Generated OG PNGs under generated/og/ are deliberately
    # excluded from this step.
    # ========================================================

    png_count = 0

    for source_png in ASSETS_SOURCE_DIR.rglob("*.png"):

        relative_path = source_png.relative_to(
            ASSETS_SOURCE_DIR
        )

        target_png = (
            ASSETS_DIR / relative_path
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
            f"📋 Copied {relative_path}"
        )

        png_count += 1

    print(
        f"📋 Copied {png_count} PNG image(s)"
    )

    # ========================================================
    # Generated OG images
    #
    # IMPORTANT:
    #
    # Generated OG PNGs are NOT copied here.
    #
    # They are produced in:
    #
    #     generated/og/
    #
    # and published later by:
    #
    #     python3 scripts/run.py og-publish
    #
    # This separation is necessary because prepare_dist()
    # deletes and recreates dist/.
    # ========================================================

    if TYPST_OG:

        print(
            "ℹ️ TYPST_OG=true — "
            "generated OG images will be published separately"
        )

    else:

        print(
            "ℹ️ TYPST_OG=false — "
            "using committed OG images"
        )

    # ========================================================
    # Check generated metadata
    # ========================================================

    if not HOMEPAGE_JSON.exists():

        raise FileNotFoundError(
            f"Missing {HOMEPAGE_JSON}"
        )


# ============================================================
# Entry point
# ============================================================

def main():
    prepare_dist()


if __name__ == "__main__":
    main()