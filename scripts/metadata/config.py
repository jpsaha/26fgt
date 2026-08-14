
# ============================================================
# Project paths
# ============================================================

from scripts.config import GENERATED_DIR

# ============================================================
# Generated files
# ============================================================

LECTURES_TYP = GENERATED_DIR / "lectures.typ"

PAGES_TYP = GENERATED_DIR / "pages.typ"

PAGES_META_TYP = GENERATED_DIR / "pages_meta.typ"

BOOK_TYP = GENERATED_DIR / "book.typ"

HOMEPAGE_TYP = GENERATED_DIR / "homepage.typ"

HOMEPAGE_JSON = GENERATED_DIR / "homepage.json"

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
CATEGORY_BOOK_DIR = GENERATED_DIR

# ============================================================
# Metadata
# ============================================================

LECTURE_METADATA_PATTERN = (
    r"#let\s+lecture\s*=\s*\((.*?)\)"
)
