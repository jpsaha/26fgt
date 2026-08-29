#!/usr/bin/env python3

"""
Central configuration for the Typst mathematics lecture website.

This module contains the project's shared configuration:

    - Project paths
    - Source directories
    - Generated-file paths
    - Distribution paths
    - Diagnostic paths
    - Website identity
    - SEO configuration
    - Open Graph configuration
    - Build-mode configuration

Build scripts should import project-specific paths and settings
from this module rather than constructing them independently.

This module should contain configuration only. Build operations
belong in the scripts/build/, scripts/metadata/, scripts/lint/,
and scripts/og/ modules.
"""

import os
from pathlib import Path

from scripts.site_config import (
    GITHUB_USERNAME,
    REPO_NAME,
    SITE_DESCRIPTION,
    SITE_TITLE,
    SITE_SUBTITLE,
    SITE_ICON,
    SITE_TAGLINE,
)


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
# ============================================================

ROOT = Path(
    __file__
).resolve().parents[1]


# ============================================================
# Project directories
# ============================================================
#
# Central definitions of the major project directories.
#
# Build, metadata, lint, reference, and OG scripts should use
# these paths rather than reconstructing them independently.
# ============================================================

CONTENT_DIR = ROOT / "content"

SCRIPTS_DIR = ROOT / "scripts"

TEMPLATES_DIR = ROOT / "templates"

GENERATED_DIR = ROOT / "generated"

DIAGNOSTICS_DIR = ROOT / "diagnostics"

DIST_DIR = ROOT / "dist"


# ============================================================
# Source assets
# ============================================================
#
# Static assets supplied by the project.
#
# These are copied into:
#
#     dist/assets/
#
# during dist preparation.
#
# ============================================================

ASSETS_SOURCE_DIR = ROOT / "assets"


# ============================================================
# Project source files
# ============================================================
#
# Top-level Typst source files belonging to the project.
# ============================================================

BOOK_SOURCE = ROOT / "book_source.typ"

PAGES_SOURCE = ROOT / "pages_source.typ"

PDFLAYOUT = TEMPLATES_DIR / "pdflayout.typ"


# ============================================================
# Project configuration files
# ============================================================
#
# Configuration files themselves are defined here so that
# scripts do not need to reconstruct their locations.
#
# ============================================================

CONFIG_FILE = SCRIPTS_DIR / "config.py"


# ============================================================
# Generated metadata / Typst files
# ============================================================
#
# These files are produced by the metadata/build pipeline.
#
# They should not normally be edited manually.
#
# ============================================================

LECTURES_TYP = (
    GENERATED_DIR / "lectures.typ"
)

BOOK_TYP = (
    GENERATED_DIR / "book.typ"
)

PAGES_TYP = (
    GENERATED_DIR / "pages.typ"
)

PAGES_META_TYP = (
    GENERATED_DIR / "pages_meta.typ"
)

HOMEPAGE_TYP = (
    GENERATED_DIR / "homepage.typ"
)

HOMEPAGE_JSON = (
    GENERATED_DIR / "homepage.json"
)

REFMAP_JSON = (
    GENERATED_DIR / "refmap.json"
)


# ============================================================
# Generated Open Graph files
# ============================================================
#
# OG generation happens outside dist/.
#
# Example:
#
#     generated/
#     └── og/
#         ├── lec1.asy
#         ├── lec1.png
#         └── ...
#
# These are working/generated files.
#
# Published OG images belong in:
#
#     dist/assets/og/
#
# ============================================================

GENERATED_OG_DIR = (
    GENERATED_DIR / "og"
)


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
#     ├── sitemap.xml
#     ├── robots.txt
#     ├── pages/
#     ├── pdf/
#     └── assets/
#         ├── css/
#         └── og/
#
# ============================================================

PAGES_DIR = (
    DIST_DIR / "pages"
)

PDF_DIR = (
    DIST_DIR / "pdf"
)

ASSETS_DIR = (
    DIST_DIR / "assets"
)

OG_DIR = (
    ASSETS_DIR / "og"
)

INDEX_HTML = (
    DIST_DIR / "index.html"
)

SITEMAP_XML = (
    DIST_DIR / "sitemap.xml"
)

ROBOTS_TXT = (
    DIST_DIR / "robots.txt"
)


# ============================================================
# Diagnostic files
# ============================================================
#
# Diagnostic output is kept separate from generated website
# output and is not intended for publication.
#
# ============================================================

IMPORTS_DOT = (
    DIAGNOSTICS_DIR / "imports.dot"
)

METADATA_REPORT = (
    DIAGNOSTICS_DIR / "metadata_report.txt"
)

GENERATED_REPORT = (
    DIAGNOSTICS_DIR / "generated_report.txt"
)

LINK_REPORT = (
    DIAGNOSTICS_DIR / "link_report.txt"
)

BUILD_REPORT = (
    DIAGNOSTICS_DIR / "build_report.txt"
)

CONFIG_REPORT = (
    DIAGNOSTICS_DIR / "config_report.txt"
)


# ============================================================
# Website identity
# ============================================================
#
# The basic site identity is defined in:
#
#     scripts/site_config.py
#
# This module imports that identity and derives URL/build
# related settings from it.
#
# ============================================================


# ------------------------------------------------------------
# Website URL
# ------------------------------------------------------------
#
# No trailing "/" is used.
#
# Example:
#
#     https://jpsaha.github.io/typst-site
#
# ============================================================

SITE_URL = (
    f"https://{GITHUB_USERNAME}.github.io/{REPO_NAME}"
)


# ------------------------------------------------------------
# Site author
# ------------------------------------------------------------

SITE_AUTHOR = ""


# ------------------------------------------------------------
# Website language
# ------------------------------------------------------------

SITE_LANGUAGE = "en"


# ------------------------------------------------------------
# Robots policy
# ------------------------------------------------------------

SITE_ROBOTS = "index, follow"


# ============================================================
# Open Graph build mode
# ============================================================
#
# These values define the default Open Graph generation policy.
#
#     TYPST_OG_BUILD
#         Default for local builds.
#
#     TYPST_OG_GITBUILD
#         Default for GitHub Actions builds.
#
# The effective setting used by the build is:
#
#     TYPST_OG
#
# See the "Effective Open Graph setting" section below for
# the complete precedence and environment-variable behavior.
#
# ------------------------------------------------------------
# Local builds
# ------------------------------------------------------------
#
# False:
#     Reuse existing/committed OG PNG images.
#
# True:
#     Generate OG .asy sources and PNG images.
#
# ------------------------------------------------------------
# GitHub Actions
# ------------------------------------------------------------
#
# False:
#     Reuse committed OG PNG images.
#
# True:
#     Generate OG images during the GitHub build.
#
# When enabled on GitHub, the workflow must provide:
#
#     Asymptote
#     TeX Live
#     ImageMagick
#
# ============================================================

TYPST_OG_BUILD = False

TYPST_OG_GITBUILD = False


# ============================================================
# ===========OLD GITHUB ACTION STUFF==========================
# ============================================================
# IS_GITHUB_ACTIONS = (
#     os.environ.get("GITHUB_ACTIONS", "").lower() == "true"
# )


# if not IS_GITHUB_ACTIONS and "TYPST_OG_BUILD" in os.environ:

#     TYPST_OG = (
#         os.environ["TYPST_OG_BUILD"].lower() == "true"
#     )

# else:

#     TYPST_OG = (
#         TYPST_OG_GITBUILD
#         if IS_GITHUB_ACTIONS
#         else TYPST_OG_BUILD
#     )
# ============================================================
# ===========OLD GITHUB ACTION STUFF==========================
# ============================================================


# ============================================================
# GitHub Actions detection
# ============================================================
#
# Used to distinguish local builds from GitHub Actions builds
# when determining the effective OG build mode.
#
# ============================================================

IS_GITHUB_ACTIONS = (
    os.environ.get(
        "GITHUB_ACTIONS",
        "",
    ).lower()
    == "true"
)


# ============================================================
# Boolean environment helper
# ============================================================
#
# Read a boolean environment variable.
#
# Accepted true values:
#
#     1
#     true
#     yes
#     on
#
# Accepted false values:
#
#     0
#     false
#     no
#     off
#
# Unknown values fall back to the supplied default.
#
# ============================================================

def env_bool(
    name,
    default=False,
):
    """
    Read a boolean environment variable.

    Accepted true values:

        1
        true
        yes
        on

    Accepted false values:

        0
        false
        no
        off

    Unknown values fall back to default.
    """

    value = os.environ.get(name)

    if value is None:
        return default

    value = value.strip().lower()

    if value in {
        "1",
        "true",
        "yes",
        "on",
    }:
        return True

    if value in {
        "0",
        "false",
        "no",
        "off",
    }:
        return False

    return default


# ============================================================
# Effective Open Graph setting
# ============================================================
#
# Priority:
#
#     GitHub Actions
#         → TYPST_OG_GITBUILD
#
#     Local + TYPST_OG_BUILD environment variable
#         → environment variable value
#
#     Normal local build
#         → TYPST_OG_BUILD from config.py
#
# Important:
#
# TYPST_OG_BUILD does not override TYPST_OG_GITBUILD
# on GitHub Actions.
#
# ============================================================

if IS_GITHUB_ACTIONS:

    TYPST_OG = TYPST_OG_GITBUILD

else:

    TYPST_OG = env_bool(
        "TYPST_OG_BUILD",
        default=TYPST_OG_BUILD,
    )


# ============================================================
# Default Open Graph image
# ============================================================
#
# This is a PUBLIC URL.
#
# It is NOT a filesystem path.
#
# Published file:
#
#     dist/assets/og/default.png
#
# Public URL:
#
#     /assets/og/default.png
#
# ============================================================

SITE_OG_IMAGE = (
    "/assets/og/default.png"
)


# ============================================================
# Open Graph directories
# ============================================================
#
# These names are kept separately because they describe the
# two different stages of the OG pipeline:
#
#     OG_GENERATED_DIR
#         Generated/intermediate OG files.
#
#     OG_PUBLISHED_DIR
#         Final public OG images under dist/.
#
# ============================================================

# Generated OG sources and intermediate PNG files.

OG_GENERATED_DIR = (
    GENERATED_DIR / "og"
)

# Published OG images.

OG_PUBLISHED_DIR = (
    DIST_DIR / "assets" / "og"
)


# ============================================================
# Open Graph template
# ============================================================
#
# Template used to generate Asymptote source files.
#
#     scripts/og/og_template.asy
#
# ============================================================

OG_TEMPLATE_FILE = (
    ROOT
    / "scripts"
    / "og"
    / "og_template.asy"
)


# ============================================================
# Open Graph image dimensions
# ============================================================
#
# Standard landscape Open Graph dimensions:
#
#     1200 × 630 pixels
#
# ============================================================

OG_WIDTH = 1200

OG_HEIGHT = 630


# ============================================================
# Open Graph rasterization
# ============================================================
#
# Asymptote first produces an intermediate PDF.
#
# ImageMagick then rasterizes that PDF at the configured
# density and resizes the result to exactly:
#
#     1200 × 630
#
# ============================================================

OG_DENSITY = 300

OG_FILTER = "Lanczos"


# ============================================================
# Open Graph file format
# ============================================================

OG_FORMAT = "png"


# ============================================================
# Open Graph public path
# ============================================================
#
# Public URL prefix for generated OG images.
#
# Example:
#
#     /assets/og/lec1.png
#
# ============================================================

OG_PUBLIC_PATH = (
    "/assets/og"
)
