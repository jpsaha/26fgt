import json
import re
import sys

from scripts.config import (
    DIST_DIR,
    HOMEPAGE_JSON,
    SITE_OG_IMAGE,
    SITE_URL,
)


# ============================================================
# Open Graph image validation
# ============================================================
#
# This checker validates the Open Graph image references in
# the generated HTML files.
#
# The source of the expected pages is:
#
#     generated/homepage.json
#
# The actual OG image reference is taken from the generated
# HTML itself.
#
# This is important because homepage.json may contain the
# correct value while the HTML generator could still produce
# an incorrect path.
#
# Checks performed:
#
#   1. Every page listed in homepage.json has an HTML file.
#   2. Every HTML file contains an og:image meta tag.
#   3. The OG image URL uses the configured site URL or is
#      root-relative.
#   4. The OG image URL points to /assets/og/.
#   5. The referenced PNG actually exists under dist/.
#
# Run with:
#
#     python3 scripts/run.py og-check
#
# ============================================================


# ============================================================
# Regular expression for og:image
# ============================================================

OG_IMAGE_RE = re.compile(
    r'<meta\b'
    r'(?=[^>]*\bproperty\s*=\s*["\']og:image["\'])'
    r'(?=[^>]*\bcontent\s*=\s*["\'][^"\']+["\'])'
    r'[^>]*>',
    re.IGNORECASE,
)


# ============================================================
# Extract content attribute
# ============================================================

CONTENT_RE = re.compile(
    r'\bcontent\s*=\s*["\']([^"\']+)["\']',
    re.IGNORECASE,
)


# ============================================================
# Helpers
# ============================================================

def load_pages():
    """
    Read homepage.json and return all page records.

    homepage.json has the following structure:

        {
            "Category A": [
                {...},
                {...}
            ],
            "Category B": [
                {...},
                {...}
            ]
        }
    """

    if not HOMEPAGE_JSON.exists():
        print()
        print("ERROR: homepage.json not found:")
        print(f"       {HOMEPAGE_JSON}")
        return None

    with HOMEPAGE_JSON.open(
        "r",
        encoding="utf-8",
    ) as file:
        data = json.load(file)

    pages = []

    for category, entries in data.items():

        if not isinstance(entries, list):
            continue

        for entry in entries:

            if not isinstance(entry, dict):
                continue

            page = dict(entry)
            page["category"] = category

            pages.append(page)

    return pages


def extract_og_image(html):
    """
    Extract the content value from the og:image meta tag.

    Returns None if no og:image tag is found.
    """

    match = OG_IMAGE_RE.search(html)

    if match is None:
        return None

    content = CONTENT_RE.search(match.group(0))

    if content is None:
        return None

    return content.group(1)


def resolve_og_path(og_url):
    """
    Convert a public OG image URL into a local dist path.

    Supported forms:

        /assets/og/fgt1.png

    and:

        https://jpsaha.github.io/typst-site/assets/og/fgt1.png
    """

    if og_url.startswith(SITE_URL):
        relative_url = og_url[len(SITE_URL):]

    elif og_url.startswith("/"):
        relative_url = og_url

    else:
        return None

    relative_url = relative_url.lstrip("/")

    return DIST_DIR / relative_url


def is_correct_og_location(og_url):
    """
    Check that the public OG image URL points to:

        /assets/og/
    """

    if og_url.startswith(SITE_URL):
        relative_url = og_url[len(SITE_URL):]

    elif og_url.startswith("/"):
        relative_url = og_url

    else:
        return False

    relative_url = relative_url.lstrip("/")

    return relative_url.startswith("assets/og/")


# ============================================================
# Main checker
# ============================================================

def main():

    print("=" * 70)
    print("Open Graph Image Check")
    print("=" * 70)

    print()
    print(f"Distribution : {DIST_DIR}")
    print(f"Metadata     : {HOMEPAGE_JSON}")
    print(f"Site URL     : {SITE_URL}")

    # --------------------------------------------------------
    # Load page metadata
    # --------------------------------------------------------

    pages = load_pages()

    if pages is None:
        return 1

    if not pages:
        print()
        print("WARNING: No page entries found in homepage.json")
        print("=" * 70)
        return 0

    # --------------------------------------------------------
    # Counters
    # --------------------------------------------------------

    checked = 0
    valid = 0
    missing_html = 0
    missing_tag = 0
    invalid_url = 0
    wrong_location = 0
    missing_image = 0

    # ========================================================
    # Check every page
    # ========================================================

    print()

    for page in pages:

        category = page.get(
            "category",
            "Unknown category",
        )

        html_name = page.get("html")

        source = page.get(
            "source",
            "",
        )

        expected_og_image = page.get(
            "og_image",
        )

        # ----------------------------------------------------
        # Metadata must specify an HTML file
        # ----------------------------------------------------

        if not html_name:

            print("INVALID")
            print(f"  Category : {category}")
            print("  HTML     : missing")
            print()

            missing_html += 1
            continue

        checked += 1

        html_file = DIST_DIR / "pages" / html_name

        # ----------------------------------------------------
        # Check HTML file
        # ----------------------------------------------------

        if not html_file.is_file():

            print("MISSING HTML")
            print(f"  Category : {category}")
            print(f"  HTML     : {html_name}")

            if source:
                print(f"  Source   : {source}")

            print()

            missing_html += 1
            continue

        # ----------------------------------------------------
        # Read HTML
        # ----------------------------------------------------

        html = html_file.read_text(
            encoding="utf-8",
        )

        # ----------------------------------------------------
        # Extract actual OG image from HTML
        # ----------------------------------------------------

        actual_og_image = extract_og_image(html)

        if actual_og_image is None:

            print("MISSING OG")
            print(f"  Category : {category}")
            print(f"  HTML     : {html_name}")

            if expected_og_image:
                print(
                    f"  Expected : {expected_og_image}"
                )
            else:
                print(
                    f"  Expected : {SITE_OG_IMAGE}"
                )

            if source:
                print(f"  Source   : {source}")

            print()

            missing_tag += 1
            continue

        # ----------------------------------------------------
        # Check URL format
        # ----------------------------------------------------

        if not (
            actual_og_image.startswith(SITE_URL)
            or actual_og_image.startswith("/")
        ):

            print("INVALID URL")
            print(f"  Category : {category}")
            print(f"  HTML     : {html_name}")
            print(f"  OG image : {actual_og_image}")

            if source:
                print(f"  Source   : {source}")

            print()

            invalid_url += 1
            continue

        # ----------------------------------------------------
        # Check /assets/og/ location
        # ----------------------------------------------------

        if not is_correct_og_location(
            actual_og_image
        ):

            print("WRONG LOCATION")
            print(f"  Category : {category}")
            print(f"  HTML     : {html_name}")
            print(f"  OG image : {actual_og_image}")
            print(
                "  Expected : /assets/og/"
            )

            if source:
                print(f"  Source   : {source}")

            print()

            wrong_location += 1
            continue

        # ----------------------------------------------------
        # Resolve local image path
        # ----------------------------------------------------

        image_file = resolve_og_path(
            actual_og_image
        )

        if image_file is None:

            print("INVALID PATH")
            print(f"  Category : {category}")
            print(f"  HTML     : {html_name}")
            print(f"  OG image : {actual_og_image}")

            print()

            invalid_url += 1
            continue

        # ----------------------------------------------------
        # Check that image exists
        # ----------------------------------------------------

        if not image_file.is_file():

            print("MISSING IMAGE")
            print(f"  Category : {category}")
            print(f"  HTML     : {html_name}")
            print(f"  OG image : {actual_og_image}")
            print(
                "  File     : "
                f"{image_file.relative_to(DIST_DIR)}"
            )

            if source:
                print(f"  Source   : {source}")

            print()

            missing_image += 1
            continue

        # ----------------------------------------------------
        # Valid page
        # ----------------------------------------------------

        valid += 1

        print("OK")
        print(f"  Category : {category}")
        print(f"  HTML     : {html_name}")
        print(f"  OG image : {actual_og_image}")

        if expected_og_image:
            print(
                f"  Metadata : {expected_og_image}"
            )

            if expected_og_image != actual_og_image:
                print(
                    "  WARNING  : HTML OG image differs "
                    "from homepage.json"
                )

        print()

    # ========================================================
    # Summary
    # ========================================================

    errors = (
        missing_html
        + missing_tag
        + invalid_url
        + wrong_location
        + missing_image
    )

    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)

    print(f"Pages checked       : {checked}")
    print(f"Valid               : {valid}")
    print(f"Missing HTML        : {missing_html}")
    print(f"Missing og:image    : {missing_tag}")
    print(f"Invalid URL         : {invalid_url}")
    print(f"Wrong location      : {wrong_location}")
    print(f"Missing image file  : {missing_image}")

    print()

    if errors == 0:

        print("RESULT: PASS")
        print(
            "All generated HTML files have valid "
            "Open Graph image references."
        )

        print("=" * 70)

        return 0

    print("RESULT: FAIL")
    print(f"Total errors: {errors}")

    print("=" * 70)

    return 1


# ============================================================
# Entry point
# ============================================================

if __name__ == "__main__":
    sys.exit(main())