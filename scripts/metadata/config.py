
# ============================================================
# Project paths
# ============================================================

from scripts.config import GENERATED_DIR
# , LECTURES_TYP, PAGES_TYP, PAGES_META_TYP, HOMEPAGE_JSON, HOMEPAGE_TYP, BOOK_TYP

# ============================================================
# Category books
# ============================================================

# Directory containing generated Typst sources for
# category-level combined books.
#
# At present this is the same generated/ directory.
# Keeping it as a separate constant makes the purpose
# explicit and allows us to move category books later
# without changing write_book.py.
# CATEGORY_BOOK_DIR = GENERATED_DIR

# ============================================================
# Metadata
# ============================================================

LECTURE_METADATA_PATTERN = (
    r"#let\s+lecture\s*=\s*\((.*?)\)"
)
