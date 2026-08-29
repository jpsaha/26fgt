#!/usr/bin/env python3

"""
Command dispatcher for the Typst mathematics lecture website.

This module provides a single command-line entry point for the
project's Python build, validation, generation, and diagnostic
modules.

Usage:

    python3 scripts/run.py <command>

Examples:

    python3 scripts/run.py metadata
    python3 scripts/run.py metadata-check
    python3 scripts/run.py generated
    python3 scripts/run.py imports
    python3 scripts/run.py html
    python3 scripts/run.py og-check
    python3 scripts/run.py report

The shell build script (build.sh) uses this dispatcher rather
than invoking individual Python modules directly.

This keeps:

    build.sh
        ↓
    scripts/run.py
        ↓
    individual Python modules

and provides one stable command interface for the Python
build layer.
"""


import subprocess
import sys


# ============================================================
# Command registry
# ============================================================
#
# Each command maps to a Python module that can be executed
# with:
#
#     python3 -m <module>
#
# This file provides a single entry point for build.sh and
# keeps the shell script independent of the individual Python
# module names.
#
# The registry contains atomic Python operations only.
#
# Composite build targets such as:
#
#     ./build.sh
#     ./build.sh allpdf
#     ./build.sh og-refresh
#
# are intentionally implemented by build.sh and are therefore
# not registered here.
#
# ------------------------------------------------------------
# Generation
# ------------------------------------------------------------
#
# python3 scripts/run.py metadata
#
# Generate metadata and metadata-driven Typst files.
#
# ------------------------------------------------------------
# Open Graph images
# ------------------------------------------------------------
#
# python3 scripts/run.py og-generate
# python3 scripts/run.py og-build
# python3 scripts/run.py og-publish
#
# og-generate:
#     Generate Asymptote source files under generated/og/.
#
# og-build:
#     Compile generated Asymptote sources into PNG images.
#
# og-publish:
#     Copy generated OG PNG images into:
#
#         dist/assets/og/
#
# The composite:
#
#     ./build.sh og-refresh
#
# performs all three operations as one explicit refresh.
#
# ------------------------------------------------------------
# Validation
# ------------------------------------------------------------
#
# python3 scripts/run.py config
# python3 scripts/run.py metadata-check
# python3 scripts/run.py generated
# python3 scripts/run.py imports
# python3 scripts/run.py links
# python3 scripts/run.py og-check
#
# config:
#     Audit project-wide configuration usage.
#
# metadata-check:
#     Validate source metadata.
#
# generated:
#     Validate generated files against source metadata.
#
# imports:
#     Validate Typst import dependencies and cycles.
#
# links:
#     Check links in generated HTML.
#
# og-check:
#     Validate Open Graph metadata and referenced images
#     in the final dist/ output.
#
# ------------------------------------------------------------
# Build infrastructure
# ------------------------------------------------------------
#
# python3 scripts/run.py prepare-dist
# python3 scripts/run.py prepare-diagnostics
#
# prepare-dist:
#     Remove/recreate dist/ and prepare the distribution
#     directory and static/generated assets.
#
# prepare-diagnostics:
#     Prepare the diagnostics directory for a new build.
#
# ------------------------------------------------------------
# Website output
# ------------------------------------------------------------
#
# python3 scripts/run.py html
#
# Build the generated HTML pages.
#
# ------------------------------------------------------------
# PDF output
# ------------------------------------------------------------
#
# python3 scripts/run.py pdf
# python3 scripts/run.py categories
# python3 scripts/run.py book
# python3 scripts/run.py pages-pdf
#
# pdf:
#     Build individual page PDFs.
#
# categories:
#     Build category PDFs.
#
# book:
#     Build the complete course/book PDF.
#
# pages-pdf:
#     Build the combined pages PDF.
#
# The composite:
#
#     ./build.sh allpdf
#
# runs all four PDF operations.
#
# ------------------------------------------------------------
# Site files
# ------------------------------------------------------------
#
# python3 scripts/run.py sitemap
# python3 scripts/run.py robots
#
# sitemap:
#     Generate sitemap.xml.
#
# robots:
#     Generate robots.txt.
#
# ------------------------------------------------------------
# Diagnostics
# ------------------------------------------------------------
#
# python3 scripts/run.py report
#
# Generate diagnostics/build_report.txt and print the final
# build diagnostics summary.
#
# ============================================================


COMMANDS = {

    # ========================================================
    # Generation
    # ========================================================

    "metadata":
        "scripts.build.generate_metadata",

    "refmap":
        "scripts.refs.build_refmap",

    "fix-refs":
        "scripts.refs.fix_html_refs",

    "fix-equations":
        "scripts.refs.fix_html_equations",


    # ========================================================
    # Open Graph images
    # ========================================================
    #
    # "og-generate":
    #     Generate Asymptote source files.
    #
    # "og-build":
    #     Build generated Asymptote files into PNG images.
    #
    # "og-publish":
    #     Copy the generated OG PNG images from generated/og/
    #     into dist/assets/og/.
    #
    # This is deliberately separate from "prepare-dist".
    # --------------------------------------------------------

    "og-generate":
        "scripts.og.generate_og",

    "og-build":
        "scripts.og.build_og",

    "og-publish":
        "scripts.og.publish_og",


    # ========================================================
    # Validation
    # ========================================================
    #
    # These commands inspect the project and generated output.
    #
    # config:
    #     Checks whether project-wide configuration is properly
    #     centralized in scripts/config.py.
    #
    # metadata-check:
    #     Checks source metadata.
    #
    # generated:
    #     Checks generated files against source metadata.
    #
    # imports:
    #     Checks Typst imports.
    #
    # links:
    #     Checks links in generated HTML.
    #
    # og-check:
    #     Checks that generated HTML contains correct OG image
    #     URLs and that the referenced images exist.
    # --------------------------------------------------------
    "config":
        "scripts.lint.check_config",

    "metadata-check":
        "scripts.lint.check_metadata",

    "generated":
        "scripts.lint.check_generated",

    "imports":
        "scripts.lint.check_imports",

    "links":
        "scripts.lint.check_links",

    "og-check":
        "scripts.lint.check_og",


    # ========================================================
    # Build infrastructure
    # ========================================================

    "prepare-dist":
        "scripts.build.prepare_dist",

    "prepare-diagnostics":
        "scripts.build.prepare_diagnostics",


    # ========================================================
    # Website output
    # ========================================================

    "html":
        "scripts.build.build_html",

    "sitemap":
        "scripts.build.build_sitemap",

    "robots":
        "scripts.build.build_robots",


    # ========================================================
    # PDF output
    # ========================================================

    "pdf":
        "scripts.build.build_pdfs",

    "categories":
        "scripts.build.build_categories",

    "book":
        "scripts.build.build_book",

    "pages-pdf":
        "scripts.build.build_pages_pdf",


    # ========================================================
    # Diagnostics
    # ========================================================

    "report":
        "scripts.build.build_report",
}

# ============================================================
# Command groups
# ============================================================
#
# Used only for help output.
#
# The order here represents the conceptual build pipeline.
# ============================================================

COMMAND_GROUPS = {

    "Generation": (
        "metadata",
        "refmap",
        "fix-equations",
        "fix-refs",
    ),

    "Open Graph": (
        "og-generate",
        "og-build",
        "og-publish",
    ),

    "Validation": (
        "config",
        "metadata-check",
        "generated",
        "imports",
        "links",
        "og-check",
    ),

    "Build preparation": (
        "prepare-dist",
        "prepare-diagnostics",
    ),

    "Website output": (
        "html",
        "sitemap",
        "robots",
    ),

    "PDF output": (
        "pdf",
        "categories",
        "book",
        "pages-pdf",
    ),

    "Diagnostics": (
        "report",
    ),
}


# ============================================================
# Composite commands
# ============================================================
#
# These are implemented by build.sh rather than this dispatcher.
# ============================================================

COMPOSITE_COMMANDS = (
    "all",
    "allpdf",
    "og-refresh",
)


# ============================================================
# Help
# ============================================================

def print_help():
    """Print command-line usage information."""

    print()
    print("Typst Mathematics Lecture Website")
    print("=" * 42)

    print()
    print("Usage:")
    print()
    print("    python3 scripts/run.py <command>")

    print()

    for group, commands in COMMAND_GROUPS.items():

        print(f"{group}:")
        print()

        for command in commands:

            print(
                f"    {command:<20}"
                f"{COMMANDS[command]}"
            )

        print()

    print("Composite commands:")
    print()

    for command in COMPOSITE_COMMANDS:
        print(f"    {command}")

    print()

    print("Composite commands are orchestrated by build.sh.")
    print()

    print("Examples:")
    print()
    print("    ./build.sh")
    print("    ./build.sh og-refresh")
    print("    ./build.sh allpdf")
    print()


# ============================================================
# Execute command
# ============================================================

def run_command(command):
    """
    Execute one registered Python command.

    The same Python interpreter that launched run.py is used.
    """

    module = COMMANDS[command]

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            module,
        ]
    )

    return result.returncode


# ============================================================
# Main
# ============================================================

def main():
    """Dispatch the requested command."""

    if len(sys.argv) == 1:

        print_help()

        return 0


    if len(sys.argv) == 2 and sys.argv[1] in (
        "-h",
        "--help",
        "help",
    ):

        print_help()

        return 0


    if len(sys.argv) != 2:

        print(
            "ERROR: exactly one command is required."
        )

        print()

        print_help()

        return 1


    command = sys.argv[1]


    # --------------------------------------------------------
    # Atomic Python command
    # --------------------------------------------------------

    if command in COMMANDS:

        return run_command(command)


    # --------------------------------------------------------
    # Composite command
    # --------------------------------------------------------

    if command in COMPOSITE_COMMANDS:

        print(
            f"ERROR: '{command}' is a composite build command."
        )

        print(
            "Run it through build.sh instead:"
        )

        print()

        print(
            f"    ./build.sh {command}"
        )

        return 1


    # --------------------------------------------------------
    # Unknown command
    # --------------------------------------------------------

    print(
        f"ERROR: unknown command: {command}"
    )

    print()

    print(
        "Run "
        "'python3 scripts/run.py --help' "
        "to see the available commands."
    )

    return 1


# ============================================================
# Entry point
# ============================================================

if __name__ == "__main__":
    sys.exit(main())