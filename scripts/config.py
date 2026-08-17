from pathlib import Path


# ============================================================
# Project root
# ============================================================
#
# This file is:
#
#     scripts/config.py
#
# Therefore:
#
#     parents[0] = scripts/
#     parents[1] = project root
#
# Keeping the project root here provides a single source of
# truth for all project paths used throughout the build system.
# ============================================================

ROOT = Path(__file__).resolve().parents[1]


# ============================================================
# Project directories
# ============================================================

CONTENT_DIR = ROOT / "content"
TEMPLATES_DIR = ROOT / "templates"
GENERATED_DIR = ROOT / "generated"
DIAGNOSTICS_DIR = ROOT / "diagnostics"

# Generated Open Graph sources and images.
#
# Example:
#
#     generated/og/gt/lec1.asy
#     generated/og/gt/lec1.png
#
GENERATED_OG_DIR = GENERATED_DIR / "og"


# ============================================================
# Source directories
# ============================================================

# Static assets supplied directly by the project.
#
# These are copied into:
#
#     dist/assets/
#
# during dist preparation.
# ============================================================

ASSETS_SOURCE_DIR = ROOT / "assets"


# ============================================================
# Project source files
# ============================================================

BOOK_SOURCE = ROOT / "book_source.typ"
PAGES_SOURCE = ROOT / "pages_source.typ"
PDFLAYOUT = ROOT / "templates" / "pdflayout.typ"


# ============================================================
# Generated files
# ============================================================
#
# These files are produced by the metadata/build pipeline.
# They should not normally be edited by hand.
# ============================================================

LECTURES_TYP = GENERATED_DIR / "lectures.typ"
BOOK_TYP = GENERATED_DIR / "book.typ"
PAGES_TYP = GENERATED_DIR / "pages.typ"
PAGES_META_TYP = GENERATED_DIR / "pages_meta.typ"
HOMEPAGE_TYP = GENERATED_DIR / "homepage.typ"
HOMEPAGE_JSON = GENERATED_DIR / "homepage.json"


# ============================================================
# Distribution directories
# ============================================================
#
# Everything under dist/ is generated and is suitable for
# publishing to GitHub Pages.
#
# Typical structure:
#
#     dist/
#     ├── index.html
#     ├── pages/
#     ├── pdf/
#     └── assets/
#         ├── css/
#         └── og/
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

# Historical/commented reference:
#
# DOT = DIAGNOSTICS_DIR / "imports.dot"


# ============================================================
# Site information
# ============================================================

# ------------------------------------------------------------
# Previous site configuration
# ------------------------------------------------------------
#
# Kept here for reference in case the site identity is changed
# back to the simpler portal-style presentation.
# ------------------------------------------------------------

# SITE_TITLE = "Mathematics Lecture Portal"
# SITE_ICON = "🧮"
# SITE_TAGLINE = (
#     "Interactive web modules & downloadable "
#     "print-ready course material"
# )


# ------------------------------------------------------------
# Current site identity
# ------------------------------------------------------------

SITE_TITLE = "Notes on Galois Theory"
SITE_SUBTITLE = "Typeset with Typst"

SITE_ICON = "🧮"

SITE_TAGLINE = (
    "These notes may contain typos, "
    "and need not be a faithful representation of any lecture or a course. "
    "The omitted proofs may be found in (m)any reference(s) on Galois theory. "
    "Please report any errors you find to the author."
)


# ============================================================
# SEO / Website
# ============================================================

# ------------------------------------------------------------
# GitHub repository
# ------------------------------------------------------------
#
# GitHub username and repository name are kept separately so
# that SITE_URL can be constructed automatically.
#
# Example:
#
#     https://jpsaha.github.io/typst-site
# ------------------------------------------------------------

# GITHUB_USERNAME = "username"
# REPO_NAME = "reponame"

GITHUB_USERNAME = "jpsaha"
REPO_NAME = "26fgt"


# ------------------------------------------------------------
# Website URL
# ------------------------------------------------------------
#
# Do not put a trailing "/" on SITE_URL.
#
# This value is used when constructing canonical URLs and
# absolute Open Graph / Twitter image URLs.
# ------------------------------------------------------------

SITE_URL = f"https://{GITHUB_USERNAME}.github.io/{REPO_NAME}"


# ------------------------------------------------------------
# Site-wide description
# ------------------------------------------------------------
#
# Used as the fallback description when an individual page
# does not provide its own description.
# ------------------------------------------------------------

SITE_DESCRIPTION = (
    "Mathematics lectures, notes, and problem-solving resources."
)


# ------------------------------------------------------------
# Site author
# ------------------------------------------------------------

SITE_AUTHOR = ""


# ------------------------------------------------------------
# Default Open Graph image
# ------------------------------------------------------------
#
# Used when a page does not have a page-specific OG image.
#
# The source image is:
#
#     assets/og/default.png
#
# and it is copied during dist preparation to:
#
#     dist/assets/og/default.png
#
# Its public URL is therefore:
#
#     /assets/og/default.png
#
# This is a PUBLIC URL, not a filesystem path.
# ------------------------------------------------------------

SITE_OG_IMAGE = "/assets/og/default.png"


# ------------------------------------------------------------
# Website language
# ------------------------------------------------------------

SITE_LANGUAGE = "en"


# ------------------------------------------------------------
# Robots policy
# ------------------------------------------------------------

SITE_ROBOTS = "index, follow"


# ============================================================
# Open Graph generation
# ============================================================
#
# The following settings are shared by the OG generation
# scripts. They belong here rather than being duplicated in:
#
#     scripts/og/generate_og.py
#     scripts/og/build_og.py
#
# This keeps OG-related configuration in one place.
# ============================================================


# ------------------------------------------------------------
# Asymptote template
# ------------------------------------------------------------
#
# Template used to generate Asymptote source files.
#
#     scripts/og/og_template.asy
#
# This is a project-level configuration path because changing
# the template location should not require modifying the OG
# generation code.
# ------------------------------------------------------------

OG_TEMPLATE_FILE = (
    ROOT
    / "scripts"
    / "og"
    / "og_template.asy"
)


# ------------------------------------------------------------
# Final Open Graph image dimensions
# ------------------------------------------------------------
#
# Standard Open Graph landscape dimensions:
#
#     1200 × 630 pixels
#
# These values are used by build_og.py when converting the
# intermediate PDF into the final PNG.
# ------------------------------------------------------------

OG_WIDTH = 1200
OG_HEIGHT = 630


# ------------------------------------------------------------
# Open Graph rasterization density
# ------------------------------------------------------------
#
# Asymptote first produces an intermediate PDF.
#
# ImageMagick then rasterizes that PDF at this density before
# resizing the result to OG_WIDTH × OG_HEIGHT.
# ------------------------------------------------------------

OG_DENSITY = 300