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

# SITE_TITLE = "Mathematics Lecture Portal"
# SITE_ICON = "🧮"
# SITE_TAGLINE = (
#     "Interactive web modules & downloadable "
#     "print-ready course material"
# )

SITE_TITLE = "Notes in Galois Theory · Typeset with Typst"
SITE_ICON = "🧮"
SITE_TAGLINE = (
    "These notes may contain typos, "
    "and need not be a faithful representation of any lecture or a course. "
    "Please report any errors you find to the author."
)


# ============================================================
# SEO / Website
# ============================================================

# GitHub
# GITHUB_USERNAME = "username"
# REPO_NAME = "reponame"
GITHUB_USERNAME = "jpsaha"
REPO_NAME = "26fgt"


# Website
SITE_URL = f"https://{GITHUB_USERNAME}.github.io/{REPO_NAME}"
# Do not put a trailing / on SITE_URL.

SITE_DESCRIPTION = (
    "Mathematics lectures, notes, and problem-solving resources."
)

SITE_AUTHOR = ""

# Default OpenGraph image
SITE_OG_IMAGE = "/assets/og/default.png"

# Language
SITE_LANGUAGE = "en"

# Robots
SITE_ROBOTS = "index, follow"
