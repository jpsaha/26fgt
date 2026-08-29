#!/usr/bin/env python3

"""
SEO and OpenGraph helpers.

Injects SEO metadata into generated Typst HTML.
"""

from html import escape
from urllib.parse import urljoin

from scripts.config import (
    SITE_URL,
    SITE_TITLE,
    SITE_DESCRIPTION,
    SITE_OG_IMAGE,
)


# ============================================================
# URL
# ============================================================

def absolute_url(path):
    """Return an absolute site URL."""

    return urljoin(
        SITE_URL.rstrip("/") + "/",
        path.lstrip("/"),
    )


# ============================================================
# SEO head
# ============================================================

def seo_tags(
    *,
    title,
    description,
    path,
    og_type="article",
    image=None,
):
    """Generate SEO/OpenGraph/Twitter HTML."""

    canonical = absolute_url(path)

    if image is None:
        image = SITE_OG_IMAGE

    image_url = absolute_url(image)

    title = escape(str(title), quote=True)
    description = escape(str(description), quote=True)
    canonical = escape(canonical, quote=True)
    image_url = escape(image_url, quote=True)
    site_title = escape(SITE_TITLE, quote=True)

    return f"""
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{canonical}">

<meta property="og:type" content="{og_type}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{canonical}">
<meta property="og:site_name" content="{site_title}">
<meta property="og:image" content="{image_url}">

<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{description}">
<meta name="twitter:image" content="{image_url}">
""".strip()


# ============================================================
# Inject into HTML
# ============================================================

def inject_seo(
    html,
    *,
    title,
    description,
    path,
    og_type="article",
    image=None,
):
    """Inject SEO metadata into the HTML <head>.

    Safe to call repeatedly: existing generated SEO tags
    are removed before new ones are inserted.
    """

    import re

    # --------------------------------------------------------
    # Remove previously generated SEO
    # --------------------------------------------------------

    patterns = [
        r'<title>.*?</title>',
        r'<meta name="description"[^>]*>\s*',
        r'<link rel="canonical"[^>]*>\s*',

        r'<meta property="og:type"[^>]*>\s*',
        r'<meta property="og:title"[^>]*>\s*',
        r'<meta property="og:description"[^>]*>\s*',
        r'<meta property="og:url"[^>]*>\s*',
        r'<meta property="og:site_name"[^>]*>\s*',
        r'<meta property="og:image"[^>]*>\s*',

        r'<meta name="twitter:card"[^>]*>\s*',
        r'<meta name="twitter:title"[^>]*>\s*',
        r'<meta name="twitter:description"[^>]*>\s*',
        r'<meta name="twitter:image"[^>]*>\s*',
    ]

    for pattern in patterns:
        html = re.sub(
            pattern,
            "",
            html,
            flags=re.IGNORECASE | re.DOTALL,
        )

    # --------------------------------------------------------
    # Generate new SEO
    # --------------------------------------------------------

    tags = seo_tags(
        title=title,
        description=description,
        path=path,
        og_type=og_type,
        image=image,
    )

    # --------------------------------------------------------
    # Insert before </head>
    # --------------------------------------------------------

    marker = "</head>"

    if marker not in html:
        raise ValueError(
            "Could not find </head> in generated HTML."
        )

    return html.replace(
        marker,
        tags + "\n" + marker,
        1,
    )