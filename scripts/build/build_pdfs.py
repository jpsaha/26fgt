#!/usr/bin/env python3

"""
Build individual PDF pages.

Reads:
    generated/homepage.json

Generates:
    dist/pdf/*.pdf

HTML pages are built separately by build_html.py.
Category PDFs are built separately by build_categories.py.
The complete book is built separately by build_book.py.
The complete pages PDF is built separately by build_pages_pdf.py.
"""

import json
import subprocess

from scripts.config import (
    ROOT,
    CONTENT_DIR,
    PDF_DIR,
    HOMEPAGE_JSON,
)


# ============================================================
# Compile one PDF
# ============================================================

def compile_pdf(lecture):
    """Compile one content page to PDF."""

    title = lecture["title"]
    pdf = lecture["pdf"]
    source = lecture["source"]

    source_path = CONTENT_DIR / source
    pdf_path = PDF_DIR / pdf

    print(f"📄 Compiling {title}")

    subprocess.run(
        [
            "typst",
            "compile",
            "--root",
            str(ROOT),
            str(source_path),
            str(pdf_path),
            "--input",
            "format=pdf",
        ],
        check=True,
    )


# ============================================================
# Build PDFs
# ============================================================

def build_pdfs(categories):
    """Compile all individual lecture/page PDFs."""

    for lectures in categories.values():

        for lecture in lectures:

            compile_pdf(lecture)


# ============================================================
# Main
# ============================================================

def main():

    # --------------------------------------------------------
    # Check metadata
    # --------------------------------------------------------

    if not HOMEPAGE_JSON.exists():

        raise FileNotFoundError(
            f"Missing {HOMEPAGE_JSON}"
        )

    # --------------------------------------------------------
    # Prepare output directory
    # --------------------------------------------------------

    PDF_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    # --------------------------------------------------------
    # Read homepage metadata
    # --------------------------------------------------------

    with HOMEPAGE_JSON.open(
        encoding="utf-8",
    ) as file:

        categories = json.load(file)

    # --------------------------------------------------------
    # Build
    # --------------------------------------------------------

    build_pdfs(categories)


# ============================================================
# Entry point
# ============================================================

if __name__ == "__main__":
    main()