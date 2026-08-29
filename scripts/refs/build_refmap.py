#!/usr/bin/env python3

"""
Build a site-wide reference map from generated HTML pages.

Reads:
    dist/pages/*.html
    generated/homepage.json

Generates:
    generated/refmap.json

The reference map contains information about every labelled
mathematical block that can be referenced from the website.
"""

from pathlib import Path
import json
import re
import sys


# ============================================================
# Project root
# ============================================================

from scripts.config import (
    ROOT,
    PAGES_DIR,
    GENERATED_DIR,
    HOMEPAGE_JSON,
    REFMAP_JSON,
)

# ============================================================
# Reference pattern
# ============================================================

REF_RE = re.compile(
    r'<figure\s+id="([^"]+)"[^>]*>'
    r'.*?'
    r'class="math-card\s+([^"]+)"'
    r'.*?'
    r'<strong>([^<]+)</strong>',
    re.DOTALL,
)


# ============================================================
# Lecture metadata
# ============================================================

def load_lecture_metadata():
    """
    Load lecture metadata from generated/homepage.json.

    homepage.json has the structure:

        {
            "Category": [
                {
                    "title": "...",
                    "html": "...",
                    "pdf": "...",
                    "source": "..."
                }
            ]
        }

    Returns:

        {
            "gt1.html": {
                ...
            }
        }
    """

    data = json.loads(
        HOMEPAGE_JSON.read_text(
            encoding="utf-8"
        )
    )

    lectures = {}

    for category, entries in data.items():

        for entry in entries:

            html = entry.get("html")

            if not html:
                continue

            lectures[html] = {
                "lecture": Path(html).stem,
                "lecture_title": entry.get(
                    "title",
                    "",
                ),
                "category": category,
                "source": entry.get(
                    "source",
                    "",
                ),
                "lecture_url": (
                    f"pages/{html}"
                ),
                "pdf_url": (
                    f"pdf/{entry['pdf']}"
                    if entry.get("pdf")
                    else ""
                ),
            }

    return lectures


# ============================================================
# Extract references from one HTML file
# ============================================================

def extract_references(
    html_path,
    lecture_metadata,
):
    """
    Extract mathematical block references from one HTML page.
    """

    text = html_path.read_text(
        encoding="utf-8"
    )

    html_name = html_path.name

    metadata = lecture_metadata.get(
        html_name,
        {
            "lecture": html_path.stem,
            "lecture_title": "",
            "category": "",
            "source": "",
            "lecture_url": (
                f"pages/{html_name}"
            ),
            "pdf_url": "",
        },
    )

    references = {}

    for match in REF_RE.finditer(text):

        anchor = match.group(1)
        class_name = match.group(2)
        label_text = match.group(3).strip()

        # ----------------------------------------------------
        # Extract label and number
        #
        # Example:
        #
        #     Exercise 1.1
        #     Definition 2.1
        # ----------------------------------------------------

        number_match = re.search(
            r"^(.*?)\s+(\d+(?:\.\d+)*)$",
            label_text,
        )

        if number_match:

            label = (
                number_match.group(1)
                .strip()
            )

            number = (
                number_match.group(2)
                .strip()
            )

        else:

            label = label_text
            number = ""

        references[anchor] = {
            "kind": class_name,
            "label": label,
            "number": number,
            "text": label_text,
            "anchor": anchor,

            "lecture": metadata[
                "lecture"
            ],

            "lecture_title": metadata[
                "lecture_title"
            ],

            "category": metadata[
                "category"
            ],

            "source": metadata[
                "source"
            ],

            "lecture_url": metadata[
                "lecture_url"
            ],

            "pdf_url": metadata[
                "pdf_url"
            ],

            "url": (
                metadata["lecture_url"]
                + "#"
                + anchor
            ),
        }

    return references


# ============================================================
# Build complete reference map
# ============================================================

def build_refmap():

    print()
    print("🔖 Building reference map")
    print("=========================")

    lecture_metadata = (
        load_lecture_metadata()
    )

    refmap = {}

    html_files = sorted(
        PAGES_DIR.glob("*.html")
    )

    for html_path in html_files:

        print(
            f"📖 {html_path.name}"
        )

        references = extract_references(
            html_path,
            lecture_metadata,
        )

        for anchor, data in references.items():

            if anchor in refmap:

                print(
                    f"  ⚠ Duplicate anchor: "
                    f"#{anchor}"
                )

                continue

            refmap[anchor] = data

            print(
                f"  ✓ "
                f"{data['text']:<25} "
                f"#{anchor}"
            )

    GENERATED_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    REFMAP_JSON.write_text(
        json.dumps(
            refmap,
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )

    print()
    print(
        f"✓ References : {len(refmap)}"
    )

    print(
        f"✓ Output     : {REFMAP_JSON}"
    )

    return refmap


# ============================================================
# Main
# ============================================================

if __name__ == "__main__":

    build_refmap()