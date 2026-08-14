#!/usr/bin/env python3

"""
Build diagnostics report.

Reads:
    dist/pages/*.html
    dist/pdf/*.pdf
    diagnostics/metadata_report.txt
    diagnostics/generated_report.txt
    diagnostics/link_report.txt

Timing information is supplied by build.sh through environment
variables.

Prints:
    Build statistics
    Diagnostic report summaries
    Stage timings
    Compact final summary

Writes:
    diagnostics/build_report.txt
"""

import os
from io import StringIO
from contextlib import redirect_stdout

from scripts.config import (
    PAGES_DIR,
    PDF_DIR,
    METADATA_REPORT,
    GENERATED_REPORT,
    LINK_REPORT,
    BUILD_REPORT,
)


# ============================================================
# Helpers
# ============================================================

def env_int(name):
    """Return an integer environment variable, defaulting to 0."""
    return int(os.environ.get(name, "0"))


def count_files(directory, pattern):
    """Count files matching a glob pattern."""
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
    """

    if not report.exists():
        return 0

    with report.open(encoding="utf-8") as file:

        for line in file:

            if not line.startswith(label):
                continue

            if ":" not in line:
                continue

            value = line.split(":", 1)[1].strip()

            try:
                return int(value)
            except ValueError:
                return 0

    return 0


def print_report_lines(report, labels):
    """Print selected lines from a diagnostic report."""

    if not report.exists():
        return

    with report.open(encoding="utf-8") as file:

        for line in file:

            if line.startswith(labels):
                print(line, end="")


# ============================================================
# Metadata report
# ============================================================

def print_metadata_report():
    """Print the metadata diagnostic summary."""

    print()
    print("## 📋 Metadata")
    print()

    if not METADATA_REPORT.exists():
        print("Metadata report not found")
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

    print(f"Report      : {METADATA_REPORT}")


# ============================================================
# Generated consistency report
# ============================================================

def print_generated_report():
    """Print the generated consistency summary."""

    print()
    print("## 🧩 Generated consistency")
    print()

    if not GENERATED_REPORT.exists():
        print("Generated report not found")
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

    print(f"Report      : {GENERATED_REPORT}")


# ============================================================
# Link report
# ============================================================

def print_link_report():
    """Print the link diagnostic summary."""

    print()
    print("## 🔗 Links")
    print()

    if not LINK_REPORT.exists():
        print("Link report not found")
        return

    print_report_lines(
        LINK_REPORT,
        (
            "Links checked",
            "Broken links",
            "Working links",
        ),
    )

    print(f"Report      : {LINK_REPORT}")


# ============================================================
# Build statistics
# ============================================================

def print_build_statistics(
    page_count,
    pdf_count,
    category_count,
    build_time,
):
    """Print generated-output statistics."""

    print()
    print("## 📦 Build")
    print()

    print(f"🌐 HTML pages:      {page_count}")
    print(f"📚 Category books:  {category_count}")
    print(f"📄 PDF files:       {pdf_count}")
    print(f"⏱ Build time:       {build_time}s")


# ============================================================
# Build timing
# ============================================================

def print_build_timing(
    time_metadata,
    time_metadata_check,
    time_generated_check,
    time_import_check,
    time_html,
    time_pdf,
    time_categories,
    time_book,
    time_pages,
    time_links,
    build_time,
):
    """Print elapsed time for each build stage."""

    print()
    print("## ⏱ Build timing")
    print()

    print(f"Metadata generation       {time_metadata:>6}s")
    print(f"Metadata validation       {time_metadata_check:>6}s")
    print(f"Generated validation      {time_generated_check:>6}s")
    print(f"Typst import validation   {time_import_check:>6}s")
    print(f"HTML pages                {time_html:>6}s")
    print(f"Individual PDFs           {time_pdf:>6}s")
    print(f"Category PDFs             {time_categories:>6}s")
    print(f"Book PDF                  {time_book:>6}s")
    print(f"Pages PDF                 {time_pages:>6}s")
    print(f"Link checking             {time_links:>6}s")
    print(f"Total                     {build_time:>6}s")


# ============================================================
# Compact summary
# ============================================================

def print_compact_summary(
    page_count,
    pdf_count,
    category_count,
):
    """Print the compact one-line build summary."""

    link_count = report_value(
        LINK_REPORT,
        "Links checked",
    )

    broken_count = report_value(
        LINK_REPORT,
        "Broken links",
    )

    print()
    print(
        f"{page_count} HTML · "
        f"{pdf_count} PDFs · "
        f"{category_count} categories · "
        f"{link_count} links · "
        f"{broken_count} broken"
    )


# ============================================================
# Final status
# ============================================================

def print_final_status(build_time):
    """Print the final successful-build message."""

    print()
    print("==============================================")
    print(f"✅ Build completed successfully in {build_time}s")
    print("==============================================")


# ============================================================
# Main report
# ============================================================

def generate_report():
    """Generate the complete build diagnostics report."""

    # --------------------------------------------------------
    # Timing information
    # --------------------------------------------------------

    build_time = env_int("BUILD_TIME")

    time_metadata = env_int("TIME_METADATA")
    time_metadata_check = env_int("TIME_METADATA_CHECK")
    time_generated_check = env_int("TIME_GENERATED_CHECK")
    time_import_check = env_int("TIME_IMPORT_CHECK")
    time_html = env_int("TIME_HTML")
    time_pdf = env_int("TIME_PDF")
    time_categories = env_int("TIME_CATEGORIES")
    time_book = env_int("TIME_BOOK")
    time_pages = env_int("TIME_PAGES")
    time_links = env_int("TIME_LINKS")

    # --------------------------------------------------------
    # Count generated files
    # --------------------------------------------------------

    page_count = count_files(PAGES_DIR, "*.html")
    pdf_count = count_files(PDF_DIR, "*.pdf")
    category_count = count_files(PDF_DIR, "category_*.pdf")

    # --------------------------------------------------------
    # Header
    # --------------------------------------------------------

    print()
    print("==============================================")
    print("📊 Build diagnostics summary")
    print("==============================================")

    # --------------------------------------------------------
    # Reports
    # --------------------------------------------------------

    print_metadata_report()
    print_generated_report()
    print_link_report()

    # --------------------------------------------------------
    # Build statistics
    # --------------------------------------------------------

    print_build_statistics(
        page_count=page_count,
        pdf_count=pdf_count,
        category_count=category_count,
        build_time=build_time,
    )

    # --------------------------------------------------------
    # Timing
    # --------------------------------------------------------

    print_build_timing(
        time_metadata=time_metadata,
        time_metadata_check=time_metadata_check,
        time_generated_check=time_generated_check,
        time_import_check=time_import_check,
        time_html=time_html,
        time_pdf=time_pdf,
        time_categories=time_categories,
        time_book=time_book,
        time_pages=time_pages,
        time_links=time_links,
        build_time=build_time,
    )

    # --------------------------------------------------------
    # Compact summary
    # --------------------------------------------------------

    print_compact_summary(
        page_count=page_count,
        pdf_count=pdf_count,
        category_count=category_count,
    )

    # --------------------------------------------------------
    # Final status
    # --------------------------------------------------------

    print_final_status(build_time)


# ============================================================
# Entry point
# ============================================================

def main():

    buffer = StringIO()

    with redirect_stdout(buffer):
        generate_report()

    report = buffer.getvalue()

    # --------------------------------------------------------
    # Write report
    # --------------------------------------------------------

    BUILD_REPORT.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    BUILD_REPORT.write_text(
        "============================================================\n"
        "GENERATED REPORT\n"
        "\n"
        "This file is generated by:\n"
        "    python3 scripts/run.py report\n"
        "\n"
        "DO NOT EDIT MANUALLY.\n"
        "============================================================\n\n"
        + report,
        encoding="utf-8",
    )

    # --------------------------------------------------------
    # Display report
    # --------------------------------------------------------

    print(report, end="")


if __name__ == "__main__":
    main()