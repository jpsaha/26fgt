#!/usr/bin/env python3

"""
Build diagnostics report.

This script generates the final build summary used by build.sh.

Reads generated output from:

    dist/pages/*.html
    dist/pdf/*.pdf
    dist/assets/og/*.png

Reads diagnostic reports from:

    diagnostics/metadata_report.txt
    diagnostics/generated_report.txt
    diagnostics/link_report.txt

Timing information is supplied by build.sh through environment
variables.

The report contains:

    - metadata summary
    - generated-file consistency summary
    - link summary
    - build output statistics
    - Open Graph statistics
    - stage timings in actual build order
    - compact final summary

The timing order follows the actual build.sh pipeline:

    1.  Prepare diagnostics
    2.  Generate metadata
    3.  Validate metadata
    4.  Validate generated files
    5.  Generate OG sources
    6.  Build OG PNGs
    7.  Configuration audit
    8.  Validate Typst imports
    9.  Prepare dist
    10. Build HTML
    11. Build sitemap
    12. Build robots.txt
    13. Validate OG output
    14. Build individual PDFs
    15. Build category PDFs
    16. Build book PDF
    17. Build pages PDF
    18. Validate links
    19. Total

The OG publishing stage is shown separately because it is used by
the explicit:

    ./build.sh og-refresh

operation.

Writes:

    diagnostics/build_report.txt

Usage:

    python3 scripts/run.py report

The report is informational. Validation failures are handled by
the individual validation stages in build.sh.
"""

import os

from contextlib import redirect_stdout
from io import StringIO

from scripts.config import (
    PAGES_DIR,
    PDF_DIR,
    DIST_DIR,
    METADATA_REPORT,
    GENERATED_REPORT,
    LINK_REPORT,
    BUILD_REPORT,
)


# ============================================================
# Environment helpers
# ============================================================

def env_int(name):
    """
    Return an integer environment variable.

    Missing or empty values are treated as zero.
    """

    value = os.environ.get(
        name,
        "0",
    ).strip()

    if not value:
        return 0

    try:
        return int(value)

    except ValueError:
        return 0


# ============================================================
# File helpers
# ============================================================

def count_files(directory, pattern):
    """
    Count files matching a glob pattern recursively.

    Returns zero if the directory does not exist.
    """

    if not directory.exists():
        return 0

    return sum(
        1
        for path in directory.rglob(pattern)
        if path.is_file()
    )


def report_value(report, label):
    """
    Read a numeric value from a diagnostic report.

    Expected format:

        Links checked : 136
        Broken links  : 0

    Returns zero when the report or value is unavailable.
    """

    if not report.exists():
        return 0

    try:

        with report.open(
            encoding="utf-8"
        ) as file:

            for line in file:

                if not line.startswith(label):
                    continue

                if ":" not in line:
                    continue

                value = line.split(
                    ":",
                    1,
                )[1].strip()

                try:
                    return int(value)

                except ValueError:
                    return 0

    except OSError:
        return 0

    return 0


def print_report_lines(report, labels):
    """
    Print selected lines from a diagnostic report.
    """

    if not report.exists():
        return

    try:

        with report.open(
            encoding="utf-8"
        ) as file:

            for line in file:

                if line.startswith(labels):

                    print(
                        line,
                        end="",
                    )

    except OSError:

        print(
            f"Unable to read report: {report}"
        )


# ============================================================
# Metadata report
# ============================================================

def print_metadata_report():
    """
    Print the metadata diagnostic summary.
    """

    print()
    print("## 📋 Metadata")
    print()

    if not METADATA_REPORT.exists():

        print(
            "Metadata report not found"
        )

        return

    print_report_lines(
        METADATA_REPORT,
        (
            "Total items",
            "Lectures",
            "Pages",
            "Categories",
        ),
    )

    print(
        f"Report      : {METADATA_REPORT}"
    )


# ============================================================
# Generated consistency report
# ============================================================

def print_generated_report():
    """
    Print the generated consistency summary.
    """

    print()
    print("## 🧩 Generated consistency")
    print()

    if not GENERATED_REPORT.exists():

        print(
            "Generated report not found"
        )

        return

    print_report_lines(
        GENERATED_REPORT,
        (
            "Source wrappers",
            "Source metadata",
            "Lectures",
            "Pages",
            "Errors",
        ),
    )

    print(
        f"Report      : {GENERATED_REPORT}"
    )


# ============================================================
# Link report
# ============================================================

def print_link_report():
    """
    Print the link diagnostic summary.
    """

    print()
    print("## 🔗 Links")
    print()

    if not LINK_REPORT.exists():

        print(
            "Link report not found"
        )

        return

    print_report_lines(
        LINK_REPORT,
        (
            "Links checked",
            "Working links",
            "Broken links",
        ),
    )

    print(
        f"Report      : {LINK_REPORT}"
    )


# ============================================================
# Open Graph statistics
# ============================================================

def print_og_statistics():
    """
    Print Open Graph image statistics.

    OG images are expected under:

        dist/assets/og/
    """

    og_dir = (
        DIST_DIR
        / "assets"
        / "og"
    )

    og_count = count_files(
        og_dir,
        "*.png",
    )

    print()
    print("## 🖼️ Open Graph")
    print()

    print(
        f"OG PNG images:     {og_count}"
    )

    print(
        f"OG directory:      {og_dir}"
    )


# ============================================================
# Build statistics
# ============================================================

def print_build_statistics(
    page_count,
    pdf_count,
    category_count,
    og_count,
    build_time,
):
    """
    Print generated-output statistics.
    """

    print()
    print("## 📦 Build output")
    print()

    print(
        f"🌐 HTML pages:      {page_count}"
    )

    print(
        f"📚 Category books:  {category_count}"
    )

    print(
        f"📄 PDF files:       {pdf_count}"
    )

    print(
        f"🖼️ OG PNG images:   {og_count}"
    )

    print(
        f"⏱ Build time:       {build_time}s"
    )


# ============================================================
# Build timing
# ============================================================

def print_build_timing(
    time_prepare_diagnostics,
    time_metadata,
    time_refmap,
    time_fix_refs,
    time_metadata_check,
    time_generated_check,
    time_og_generate,
    time_og_build,
    time_config,
    time_import_check,
    time_prepare_dist,
    time_html,
    time_sitemap,
    time_robots,
    time_og_check,
    time_pdf,
    time_categories,
    time_book,
    time_pages,
    time_links,
    time_og_publish,
    build_time,
):
    """
    Print elapsed time for each build stage.

    The primary timing order exactly follows the normal
    build.sh "all" pipeline.

    OG publishing is displayed separately because it is used
    by the explicit "og-refresh" operation and is not part of
    the normal "all" pipeline.
    """

    print()
    print("## ⏱ Build timing")
    print()

    # --------------------------------------------------------
    # Actual build.sh pipeline
    # --------------------------------------------------------

    print(
        f"Diagnostics preparation   {time_prepare_diagnostics:>6}s"
    )

    print(
        f"Metadata generation       {time_metadata:>6}s"
    )

    print(
        f"Reference map             {time_refmap:>6}s"
    )

    print(
        f"HTML reference fixing     {time_fix_refs:>6}s"
    )

    print(
        f"Metadata validation       {time_metadata_check:>6}s"
    )

    print(
        f"Generated validation      {time_generated_check:>6}s"
    )

    print(
        f"OG source generation      {time_og_generate:>6}s"
    )

    print(
        f"OG PNG build              {time_og_build:>6}s"
    )

    print(
        f"Configuration audit       {time_config:>6}s"
    )

    print(
        f"Typst import validation   {time_import_check:>6}s"
    )

    print(
        f"Distribution preparation  {time_prepare_dist:>6}s"
    )

    print(
        f"HTML pages                {time_html:>6}s"
    )

    print(
        f"Sitemap                   {time_sitemap:>6}s"
    )

    print(
        f"robots.txt                {time_robots:>6}s"
    )

    print(
        f"OG validation             {time_og_check:>6}s"
    )

    print(
        f"Individual PDFs           {time_pdf:>6}s"
    )

    print(
        f"Category PDFs             {time_categories:>6}s"
    )

    print(
        f"Book PDF                  {time_book:>6}s"
    )

    print(
        f"Pages PDF                 {time_pages:>6}s"
    )

    print(
        f"Link checking             {time_links:>6}s"
    )

    # --------------------------------------------------------
    # Explicit OG refresh operation
    # --------------------------------------------------------

    print()
    print("## 🔄 Open Graph refresh timing")
    print()

    print(
        f"OG publishing             {time_og_publish:>6}s"
    )

    print()

    print(
        f"Total                     {build_time:>6}s"
    )


# ============================================================
# Compact summary
# ============================================================

def print_compact_summary(
    page_count,
    pdf_count,
    category_count,
    og_count,
):
    """
    Print the compact one-line build summary.
    """

    link_count = report_value(
        LINK_REPORT,
        "Links checked",
    )

    broken_count = report_value(
        LINK_REPORT,
        "Broken links",
    )

    print()
    print("## 📌 Summary")
    print()

    print(
        f"{page_count} HTML · "
        f"{pdf_count} PDFs · "
        f"{category_count} categories · "
        f"{og_count} OG images · "
        f"{link_count} links · "
        f"{broken_count} broken"
    )


# ============================================================
# Final status
# ============================================================

def print_final_status(
    build_time,
    broken_links,
):
    """
    Print the final build status.
    """

    print()
    print(
        "=============================================="
    )

    if broken_links:

        print(
            f"⚠️ Build completed with "
            f"{broken_links} broken links "
            f"in {build_time}s"
        )

    else:

        print(
            f"✅ Build completed successfully "
            f"in {build_time}s"
        )

    print(
        "=============================================="
    )


# ============================================================
# Main report generation
# ============================================================

def generate_report():
    """
    Generate the complete build diagnostics report.
    """

    # ========================================================
    # Timing information
    # ========================================================

    build_time = env_int(
        "BUILD_TIME"
    )

    time_prepare_diagnostics = env_int(
        "TIME_PREPARE_DIAGNOSTICS"
    )

    time_metadata = env_int(
        "TIME_METADATA"
    )

    time_refmap = env_int(
        "TIME_REFMAP"
    )

    time_fix_refs = env_int(
        "TIME_FIX_REFS"
    )

    time_metadata_check = env_int(
        "TIME_METADATA_CHECK"
    )

    time_generated_check = env_int(
        "TIME_GENERATED_CHECK"
    )

    time_og_generate = env_int(
        "TIME_OG_GENERATE"
    )

    time_og_build = env_int(
        "TIME_OG_BUILD"
    )

    time_config = env_int(
        "TIME_CONFIG"
    )

    time_import_check = env_int(
        "TIME_IMPORT_CHECK"
    )

    time_prepare_dist = env_int(
        "TIME_PREPARE_DIST"
    )

    time_html = env_int(
        "TIME_HTML"
    )

    time_sitemap = env_int(
        "TIME_SITEMAP"
    )

    time_robots = env_int(
        "TIME_ROBOTS"
    )

    time_og_check = env_int(
        "TIME_OG_CHECK"
    )

    time_pdf = env_int(
        "TIME_PDF"
    )

    time_categories = env_int(
        "TIME_CATEGORIES"
    )

    time_book = env_int(
        "TIME_BOOK"
    )

    time_pages = env_int(
        "TIME_PAGES"
    )

    time_links = env_int(
        "TIME_LINKS"
    )

    time_og_publish = env_int(
        "TIME_OG_PUBLISH"
    )

    # ========================================================
    # Generated-output counts
    # ========================================================

    page_count = count_files(
        PAGES_DIR,
        "*.html",
    )

    pdf_count = count_files(
        PDF_DIR,
        "*.pdf",
    )

    category_count = count_files(
        PDF_DIR,
        "category_*.pdf",
    )

    og_dir = (
        DIST_DIR
        / "assets"
        / "og"
    )

    og_count = count_files(
        og_dir,
        "*.png",
    )

    # ========================================================
    # Link statistics
    # ========================================================

    broken_count = report_value(
        LINK_REPORT,
        "Broken links",
    )

    # ========================================================
    # Header
    # ========================================================

    print()
    print(
        "=============================================="
    )

    print(
        "📊 Build diagnostics summary"
    )

    print(
        "=============================================="
    )

    # ========================================================
    # Diagnostic reports
    # ========================================================

    print_metadata_report()

    print_generated_report()

    print_link_report()

    # ========================================================
    # Open Graph
    # ========================================================

    print_og_statistics()

    # ========================================================
    # Build statistics
    # ========================================================

    print_build_statistics(
        page_count=page_count,
        pdf_count=pdf_count,
        category_count=category_count,
        og_count=og_count,
        build_time=build_time,
    )

    # ========================================================
    # Timing
    # ========================================================

    print_build_timing(
        time_prepare_diagnostics=time_prepare_diagnostics,
        time_metadata=time_metadata,
        time_refmap=time_refmap,
        time_fix_refs=time_fix_refs,
        time_metadata_check=time_metadata_check,
        time_generated_check=time_generated_check,
        time_og_generate=time_og_generate,
        time_og_build=time_og_build,
        time_config=time_config,
        time_import_check=time_import_check,
        time_prepare_dist=time_prepare_dist,
        time_html=time_html,
        time_sitemap=time_sitemap,
        time_robots=time_robots,
        time_og_check=time_og_check,
        time_pdf=time_pdf,
        time_categories=time_categories,
        time_book=time_book,
        time_pages=time_pages,
        time_links=time_links,
        time_og_publish=time_og_publish,
        build_time=build_time,
    )

    # ========================================================
    # Compact summary
    # ========================================================

    print_compact_summary(
        page_count=page_count,
        pdf_count=pdf_count,
        category_count=category_count,
        og_count=og_count,
    )

    # ========================================================
    # Final status
    # ========================================================

    print_final_status(
        build_time=build_time,
        broken_links=broken_count,
    )


# ============================================================
# Entry point
# ============================================================

def main():

    buffer = StringIO()

    with redirect_stdout(buffer):

        generate_report()

    report = buffer.getvalue()

    # ========================================================
    # Write diagnostic report
    # ========================================================

    BUILD_REPORT.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    BUILD_REPORT.write_text(
        "============================================================\n"
        "BUILD REPORT\n"
        "\n"
        "This file is generated by:\n"
        "    python3 scripts/run.py report\n"
        "\n"
        "DO NOT EDIT MANUALLY.\n"
        "============================================================\n\n"
        + report,
        encoding="utf-8",
    )

    # ========================================================
    # Display report
    # ========================================================

    print(
        report,
        end="",
    )


if __name__ == "__main__":
    main()