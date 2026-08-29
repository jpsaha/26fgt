#!/usr/bin/env python3

"""
Fix canonical internal references in generated HTML.

Reads:
    generated/refmap.json

Processes:
    dist/pages/*.html

The reference map is the source of truth.

Example refmap entry:

    "defn-linmap": {
        "kind": "definition",
        "label": "Definition",
        "number": "1.3",
        "text": "Definition 1.3",
        "anchor": "defn-linmap",
        "lecture": "gt1",
        "lecture_title": "Groups",
        "category": "Group theory",
        "source": "gt/lec1.typ",
        "lecture_url": "pages/gt1.html",
        "pdf_url": "pdf/gt1.pdf",
        "url": "pages/gt1.html#defn-linmap"
    }

Generated HTML:

    Same page:
        href="#defn-linmap"

    Different page:
        href="gt2.html#defn-example"
"""

from pathlib import Path
import json
import re
import sys


# ============================================================
# Configuration
# ============================================================

from scripts.config import (
    ROOT,
    PAGES_DIR,
    GENERATED_DIR,
    REFMAP_JSON,
)

# ============================================================
# Match every href
# ============================================================
#
# We deliberately match ALL href attributes rather than only
# href="#...".
#
# This allows the script to repair links produced by Typst
# regardless of whether they currently look like:
#
#     #defn-x
#     gt1.html#defn-x
#     pages/gt1.html#defn-x
#
# ============================================================

HREF_RE = re.compile(
    r'(?P<prefix>\bhref=")'
    r'(?P<url>[^"]*)'
    r'(?P<suffix>")',
    re.IGNORECASE,
)


# ============================================================
# Load reference map
# ============================================================

def load_refmap():

    if not REFMAP_JSON.exists():

        print(
            f"ERROR: reference map not found:\n"
            f"    {REFMAP_JSON}\n\n"
            f"Run:\n"
            f"    python3 scripts/refs/build_refmap.py"
        )

        return None

    try:

        data = json.loads(
            REFMAP_JSON.read_text(
                encoding="utf-8"
            )
        )

    except json.JSONDecodeError as error:

        print(
            f"ERROR: invalid JSON in {REFMAP_JSON}\n"
            f"    {error}"
        )

        return None

    return data


# ============================================================
# Extract anchor from href
# ============================================================

def extract_anchor(url):
    """
    Extract the fragment/anchor from a URL.

    Examples:

        #defn-x
            -> defn-x

        gt1.html#defn-x
            -> defn-x

        pages/gt1.html#defn-x
            -> defn-x

        https://example.com/page#defn-x
            -> defn-x

    Returns None when there is no fragment.
    """

    if "#" not in url:
        return None

    return url.split(
        "#",
        1,
    )[1]


# ============================================================
# Build browser-relative URL
# ============================================================

def relative_reference(
    html_path,
    reference,
):
    """
    Convert the canonical refmap URL into a URL relative to
    the HTML file being modified.

    Examples:

        Current:
            dist/pages/gt1.html

        Reference:
            pages/gt1.html#defn-x

        Result:
            #defn-x


        Current:
            dist/pages/gt1.html

        Reference:
            pages/gt2.html#defn-x

        Result:
            gt2.html#defn-x
    """

    canonical_url = reference["url"]

    # --------------------------------------------------------
    # Split page and fragment
    # --------------------------------------------------------

    if "#" in canonical_url:

        page_url, anchor = canonical_url.split(
            "#",
            1,
        )

    else:

        page_url = canonical_url
        anchor = reference["anchor"]

    # --------------------------------------------------------
    # Absolute filesystem path of target page
    # --------------------------------------------------------

    target = ROOT / "dist" / page_url

    # --------------------------------------------------------
    # Same HTML page
    # --------------------------------------------------------

    if target.resolve() == html_path.resolve():

        return "#" + anchor

    # --------------------------------------------------------
    # Different HTML page
    # --------------------------------------------------------

    relative = target.relative_to(
        html_path.parent
    )

    return (
        relative.as_posix()
        + "#"
        + anchor
    )


# ============================================================
# Fix one HTML file
# ============================================================

def fix_file(
    html_path,
    refmap,
):
    """
    Fix references in one HTML file.

    Returns number of changes.
    """

    html = html_path.read_text(
        encoding="utf-8"
    )

    changes = 0

    def replace(match):

        nonlocal changes

        prefix = match.group("prefix")
        old_url = match.group("url")
        suffix = match.group("suffix")

        # ----------------------------------------------------
        # We only care about URLs containing a fragment.
        # ----------------------------------------------------

        anchor = extract_anchor(
            old_url
        )

        if not anchor:
            return match.group(0)

        # ----------------------------------------------------
        # Look up the anchor in the generated reference map.
        # ----------------------------------------------------

        reference = refmap.get(
            anchor
        )

        if reference is None:
            return match.group(0)

        # ----------------------------------------------------
        # Canonical display text is handled separately below.
        # ----------------------------------------------------

        new_url = relative_reference(
            html_path,
            reference,
        )

        if new_url == old_url:

            # URL already correct. We still leave the visible
            # text alone here.
            return match.group(0)

        changes += 1

        print(
            f"  ✓ {anchor:<40}"
            f"{old_url} → {new_url}"
        )

        return (
            prefix
            + new_url
            + suffix
        )

    # --------------------------------------------------------
    # Fix hrefs
    # --------------------------------------------------------

    updated = HREF_RE.sub(
        replace,
        html,
    )

    # --------------------------------------------------------
    # Fix visible reference text.
    #
    # Example:
    #
    #     Exercise 1
    #
    # becomes:
    #
    #     Exercise 1.1
    #
    # We do this separately because HTML href replacement and
    # visible text replacement are different operations.
    # --------------------------------------------------------

    for anchor, reference in refmap.items():

        canonical_text = reference.get(
            "text"
        )

        if not canonical_text:
            continue

        # ----------------------------------------------------
        # Only operate on references whose anchor actually
        # appears in this page.
        # ----------------------------------------------------

        if (
            f'#{anchor}"' not in updated
            and f'#{anchor}">' not in updated
        ):

            continue

        # ----------------------------------------------------
        # Replace the text inside an <a> whose href points to
        # this anchor.
        #
        # We intentionally do not try to parse arbitrary HTML
        # with regex; this targeted replacement is sufficient
        # for the generated Typst HTML structure.
        # ----------------------------------------------------

        pattern = re.compile(
            r'(<a\b[^>]*href="[^"]*#'
            + re.escape(anchor)
            + r'"[^>]*>)'
            r'(.*?)'
            r'(</a>)',
            re.IGNORECASE | re.DOTALL,
        )

        def replace_text(match):

            old_text = match.group(2)

            # ------------------------------------------------
            # Don't replace if already canonical.
            # ------------------------------------------------

            if old_text.strip() == canonical_text:
                return match.group(0)

            return (
                match.group(1)
                + canonical_text
                + match.group(3)
            )

        updated = pattern.sub(
            replace_text,
            updated,
        )

    # --------------------------------------------------------
    # Write only if changed.
    # --------------------------------------------------------

    if updated != html:

        html_path.write_text(
            updated,
            encoding="utf-8",
        )

    return changes


# ============================================================
# Main
# ============================================================

def main():

    print()
    print("🔖 Fixing HTML references")
    print("=========================")

    refmap = load_refmap()

    if refmap is None:
        return 1

    html_files = sorted(
        PAGES_DIR.glob("*.html")
    )

    if not html_files:

        print(
            f"ERROR: no HTML files found in {PAGES_DIR}"
        )

        return 1

    total_changes = 0

    for html_path in html_files:

        print(
            f"📖 {html_path.name}"
        )

        changes = fix_file(
            html_path,
            refmap,
        )

        total_changes += changes

    print()
    print(
        f"✓ References in map : {len(refmap)}"
    )

    print(
        f"✓ HTML pages        : {len(html_files)}"
    )

    print(
        f"✓ URL changes       : {total_changes}"
    )

    print()

    return 0


# ============================================================
# Entry point
# ============================================================

if __name__ == "__main__":

    raise SystemExit(
        main()
    )