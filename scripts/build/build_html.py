#!/usr/bin/env python3

"""
Build individual HTML pages and the homepage.

Reads:
    generated/homepage.json

Generates:
    dist/index.html
    dist/pages/*.html

PDF files are built separately by build_pdfs.py,
build_categories.py, build_book.py, and build_pages_pdf.py.
"""

from pathlib import Path
import json
import re
import subprocess

from scripts.config import (
    ROOT,
    PAGES_DIR,
    CONTENT_DIR,
    HOMEPAGE_JSON,
    INDEX_HTML,
    SITE_TITLE,
    SITE_SUBTITLE,
    SITE_ICON,
    SITE_TAGLINE,
    SITE_DESCRIPTION,
    SITE_OG_IMAGE,
    GENERATED_OG_DIR,
    OG_DIR,
)

# from scripts.metadata.seo import seo_head
from scripts.metadata.seo import inject_seo

# ============================================================
# Compile one page
# ============================================================

def compile_page(lecture):
    """Compile one content page to HTML and inject SEO metadata."""

    # ========================================================
    # Basic lecture metadata
    # ========================================================

    title = lecture["title"]
    html = lecture["html"]
    source = lecture["source"]

    # --------------------------------------------------------
    # Resolve the Typst source and HTML output paths.
    #
    # Example:
    #
    #     source:
    #         lectures/lec1.typ
    #
    #     output:
    #         dist/pages/lec1.html
    # --------------------------------------------------------

    source_path = CONTENT_DIR / source
    html_path = PAGES_DIR / html

    print(f"📖 Compiling {title}")

    # ========================================================
    # Compile Typst source to HTML
    # ========================================================

    subprocess.run(
        [
            "typst",
            "compile",
            "--features",
            "html",
            "--root",
            str(ROOT),
            str(source_path),
            str(html_path),
            "--input",
            "format=html",
        ],
        check=True,
    )

    # ========================================================
    # Read generated HTML
    # ========================================================

    html_content = html_path.read_text(
        encoding="utf-8",
    )

    # ========================================================
    # SEO description
    # ========================================================
    #
    # Use the description supplied in the lecture metadata.
    #
    # If no lecture-specific description is provided, use the
    # site-wide default description.
    # ========================================================

    description = lecture.get(
        "description",
        SITE_DESCRIPTION,
    )


    # ========================================================
    # Determine Open Graph image
    # ========================================================
    #
    # Priority:
    #
    #   1. Explicit og_image from metadata.
    #   2. Generated OG image derived from source.
    #   3. Site-wide default OG image.
    #
    # Example:
    #
    #   source = "mopss/mopss_aug08.typ"
    #
    #   generated:
    #       generated/og/mopss/mopss_aug08.png
    #
    #   published:
    #       /assets/og/mopss/mopss_aug08.png
    # ========================================================

    explicit_og_image = lecture.get("og_image")

    if explicit_og_image:

        # ----------------------------------------------------
        # 1. Explicit OG image supplied in metadata
        # ----------------------------------------------------

        image = explicit_og_image

    else:

        source_path_relative = Path(source)

        relative_og_path = (
            source_path_relative.with_suffix(".png")
        )

        # ----------------------------------------------------
        # 2. Newly generated OG image
        #
        # Used when:
        #
        #     TYPST_OG=true
        #
        # and the current build generated:
        #
        #     generated/og/gt/lec2.png
        # ----------------------------------------------------

        generated_og_path = (
            GENERATED_OG_DIR
            / relative_og_path
        )

        # ----------------------------------------------------
        # 3. Existing/committed OG image
        #
        # Used when:
        #
        #     TYPST_OG=false
        #
        # but a previously generated PNG already exists in:
        #
        #     dist/assets/og/
        #
        # This allows normal builds and GitHub deployments to
        # reuse committed OG images without regenerating them.
        # ----------------------------------------------------

        published_og_path = (
            OG_DIR
            / relative_og_path
        )

        if generated_og_path.exists():

            image = (
                "/assets/og/"
                + str(relative_og_path)
            )

        elif published_og_path.exists():

            image = (
                "/assets/og/"
                + str(relative_og_path)
            )

        else:

            # ------------------------------------------------
            # 4. Site-wide default
            # ------------------------------------------------

            image = SITE_OG_IMAGE


    # ========================================================
    # Inject SEO / Open Graph / Twitter metadata
    # ========================================================

    html_content = inject_seo(
        html_content,
        title=title,
        description=description,
        path=f"pages/{html}",
        og_type="article",
        image=image,
    )

    # ========================================================
    # Write the HTML with the injected metadata
    # ========================================================

    html_path.write_text(
        html_content,
        encoding="utf-8",
    )


# ============================================================
# Homepage entry
# ============================================================

def write_homepage_entry(file, lecture):
    """Write one lecture/page entry to index.html."""

    title = lecture["title"]
    html = lecture["html"]
    pdf = lecture["pdf"]

    file.write(
        f"""
<div class="lecture-row">

    <span>{title}</span>

    <div class="lecture-links">

        <a
            href="pages/{html}"
            class="btn btn-web"
        >
            🌐 View Web
        </a>

        <a
            href="pdf/{pdf}"
            class="btn btn-pdf"
            target="_blank"
        >
            📄 PDF Version
        </a>

    </div>

</div>
"""
    )


# ============================================================
# Category PDF filename
# ============================================================

def category_pdf_filename(category):
    """
    Convert a category name into the category PDF filename.

    Examples:

        Linear Algebra -> category_linear_algebra.pdf
        IOQM           -> category_ioqm.pdf
        R-M-O          -> category_r_m_o.pdf
    """

    name = category.lower().strip()

    name = re.sub(
        r"[^a-z0-9]+",
        "_",
        name,
    )

    name = name.strip("_")

    return f"category_{name}.pdf"


# ============================================================
# Build homepage
# ============================================================

def build_homepage(categories):
    """Write the generated index.html."""

    with INDEX_HTML.open(
        "w",
        encoding="utf-8",
    ) as index:

        # ----------------------------------------------------
        # Header
        # ----------------------------------------------------

        index.write(
            "<!DOCTYPE html>\n"
            "<html lang=\"en\">\n"
            "<head>\n"
            '    <meta charset="UTF-8">\n'
            '    <meta name="viewport" '
            'content="width=device-width, initial-scale=1.0">\n'
            f'    <title>{SITE_TITLE}</title>\n'
            '    <link rel="stylesheet" '
            'href="assets/css/style.css">\n'
            "</head>\n"
            "\n"
            "<body>\n"
            "\n"
            '<div class="index-container">\n'
            "\n"
            '<header class="index-header">\n'
            f"    <h1>{SITE_ICON} {SITE_TITLE}</h1>\n"
            f"    <p class=\"site-subtitle\">{SITE_SUBTITLE}</p>\n"
            f"    <p class=\"site-tagline\">{SITE_TAGLINE}</p>\n"
            "</header>\n"
            "\n"
            '<main class="lecture-list">\n'
        )

        # ----------------------------------------------------
        # Categories
        # ----------------------------------------------------

        for category, lectures in categories.items():

            index.write(
                f"""
        <div style="
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 12px 0;
        ">

            <h2 style="
                margin: 0;
            ">
                {category}
            </h2>

            <div class="lecture-links">

                <a
                    href="pdf/{category_pdf_filename(category)}"
                    class="btn btn-pdf"
                    target="_blank"
                >
                    📚 Download Complete PDF
                </a>

            </div>

        </div>
        """
            )

            # ------------------------------------------------
            # Lectures / pages
            # ------------------------------------------------

            for lecture in lectures:

                compile_page(lecture)

                write_homepage_entry(
                    index,
                    lecture,
                )

        # ----------------------------------------------------
        # Footer
        # ----------------------------------------------------

        index.write(
            """
</main>

</div>

</body>
</html>
"""
        )


    # --------------------------------------------------------
    # Inject homepage SEO
    # --------------------------------------------------------

    html_content = INDEX_HTML.read_text(
        encoding="utf-8",
    )

    html_content = inject_seo(
        html_content,
        title=SITE_TITLE,
        description=SITE_DESCRIPTION,
        path="",
        og_type="website",
    )

    INDEX_HTML.write_text(
        html_content,
        encoding="utf-8",
    )
# ============================================================
# Main
# ============================================================

def main():

    if not HOMEPAGE_JSON.exists():

        raise FileNotFoundError(
            f"Missing {HOMEPAGE_JSON}"
        )

    # --------------------------------------------------------
    # Prepare output directory
    # --------------------------------------------------------

    PAGES_DIR.mkdir(
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

    build_homepage(categories)

    print(
        f"🌐 Wrote {INDEX_HTML}"
    )


# ============================================================
# Entry point
# ============================================================

if __name__ == "__main__":
    main()