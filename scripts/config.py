from pathlib import Path

# ============================================================
# Project root
# ============================================================

ROOT = Path(__file__).resolve().parents[1]


# ============================================================
# Project directories
# ============================================================

CONTENT_DIR = ROOT / "content"
TEMPLATES_DIR = ROOT / "templates"
GENERATED_DIR = ROOT / "generated"
DIAGNOSTICS_DIR = ROOT / "diagnostics"

# ============================================================
# Source directories
# ============================================================

ASSETS_SOURCE_DIR = ROOT / "assets"

# ============================================================
# Project files
# ============================================================

BOOK_SOURCE = ROOT / "book_source.typ"
PAGES_SOURCE = ROOT / "pages_source.typ"
PDFLAYOUT = ROOT / "templates" / "pdflayout.typ"


# ============================================================
# Generated files
# ============================================================

LECTURES_TYP = GENERATED_DIR / "lectures.typ"
PAGES_TYP = GENERATED_DIR / "pages.typ"
PAGES_META_TYP = GENERATED_DIR / "pages_meta.typ"
HOMEPAGE_JSON = GENERATED_DIR / "homepage.json"

# ============================================================
# Distribution directories
# ============================================================

DIST_DIR = ROOT / "dist"

PAGES_DIR = DIST_DIR / "pages"
PDF_DIR = DIST_DIR / "pdf"
ASSETS_DIR = DIST_DIR / "assets"

INDEX_HTML = DIST_DIR / "index.html"


# ============================================================
# Diagnostic files
# ============================================================

IMPORTS_DOT = DIAGNOSTICS_DIR / "imports.dot"

METADATA_REPORT = DIAGNOSTICS_DIR / "metadata_report.txt"
GENERATED_REPORT = DIAGNOSTICS_DIR / "generated_report.txt"
LINK_REPORT = DIAGNOSTICS_DIR / "link_report.txt"

BUILD_REPORT = DIAGNOSTICS_DIR / "build_report.txt"


# DOT = DIAGNOSTICS_DIR / "imports.dot"


# ============================================================
# Site information
# ============================================================

SITE_TITLE = "Notes"
SITE_ICON = "🧮"
SITE_TAGLINE = (
    "These notes may contain typos, "
    "and need not be a faithful representation of any lecture or a course. "
    "Please report any errors you find to the author."
)
