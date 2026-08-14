#!/usr/bin/env python3

"""
Generate metadata and generated Typst files.

This script is the entry point for the metadata generation pipeline.

The actual work is split into modules under:

scripts/metadata/
"""

import sys
import shutil
from pathlib import Path

# ------------------------------------------------------------
# Make scripts/ available for imports
# ------------------------------------------------------------

SCRIPTS_DIR = Path(__file__).resolve().parent.parent

if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

# ============================================================
# Project root
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

# ============================================================
# Import project metadata package
# ============================================================

# When this file is executed directly, Python places
# scripts/build/ on sys.path rather than the project root.
# Add PROJECT_ROOT so that scripts.metadata can be imported.

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# ------------------------------------------------------------
# Import metadata modules
# ------------------------------------------------------------

from metadata.discover import discover_content

from metadata.navigation import (
    sort_lectures,
    add_navigation,
)

from metadata.write_lectures import (
    write_lectures,
)

from metadata.write_pages import (
    write_pages,
    write_pages_meta,
)

from metadata.write_homepage import (
    write_homepage,
)

from metadata.write_book import (
    write_book,
    write_category_books,
)

from metadata.write_report import (
    write_metadata_report,
)

from metadata.config import (
    CATEGORY_BOOK_DIR,
    GENERATED_DIR,
)

# ------------------------------------------------------------
# Helpers
# ------------------------------------------------------------

def prepare_generated_dir():
    """Remove previous generated files and recreate the directory."""

    if GENERATED_DIR.exists():
        shutil.rmtree(GENERATED_DIR)

    GENERATED_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

# ------------------------------------------------------------
# Main
# ------------------------------------------------------------

def main():

    # --------------------------------------------------------
    # Prepare generated directory
    # --------------------------------------------------------

    prepare_generated_dir()

    # --------------------------------------------------------
    # Discover
    # --------------------------------------------------------

    lectures, pages = discover_content()

    # --------------------------------------------------------
    # Combine all content
    #
    # Keep lectures and pages separate because the existing
    # homepage, navigation, and course-book generators need
    # that distinction.
    #
    # Category books, however, should contain every
    # metadata-bearing item regardless of its type.
    # --------------------------------------------------------

    all_content = lectures + pages

    # --------------------------------------------------------
    # Sort
    # --------------------------------------------------------

    sort_lectures(lectures)

    # --------------------------------------------------------
    # Navigation
    # --------------------------------------------------------

    add_navigation(lectures)

    # --------------------------------------------------------
    # Generated files
    # --------------------------------------------------------

    write_lectures(lectures)

    write_pages(pages)

    write_pages_meta(pages)

    write_homepage(
        lectures,
        pages,
    )

    # --------------------------------------------------------
    # Complete course book
    # --------------------------------------------------------

    # Preserve the existing combined course book.
    #
    # This currently uses numbered lectures only.
    write_book(lectures, title="Combined")

    # --------------------------------------------------------
    # Category books
    # --------------------------------------------------------

    # Generate one Typst source for every category.
    #
    # Unlike the complete course book, category books use
    # ALL metadata-bearing content: lectures + pages.
    #
    # For example, this can generate:
    #
    # generated/category_developer.typ
    # generated/category_ioqm.typ
    # generated/category_lecture.typ
    # generated/category_linear_algebra.typ
    # generated/category_rmo.typ
    #
    # These will be compiled into PDFs later by build.sh.
    write_category_books(
        all_content,
        CATEGORY_BOOK_DIR,
    )

    write_metadata_report(
    lectures,
    pages,
)


if __name__ == "__main__":
    main()