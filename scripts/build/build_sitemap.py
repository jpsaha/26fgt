#!/usr/bin/env python3

"""
Generate sitemap.xml from generated homepage metadata.
"""

import json

from scripts.config import (
    HOMEPAGE_JSON,
    DIST_DIR,
    SITE_URL,
)


# ============================================================
# URL
# ============================================================

def absolute_url(path):
    return (
        SITE_URL.rstrip("/")
        + "/"
        + path.lstrip("/")
    )


# ============================================================
# Sitemap
# ============================================================

def build_sitemap(categories):

    urls = [
        (
            absolute_url(""),
            "1.0",
        )
    ]

    for lectures in categories.values():

        for lecture in lectures:

            html = lecture["html"]

            urls.append(
                (
                    absolute_url(
                        f"pages/{html}"
                    ),
                    "0.8",
                )
            )

    sitemap = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]

    for url, priority in urls:

        sitemap.extend(
            [
                "    <url>",
                f"        <loc>{url}</loc>",
                f"        <priority>{priority}</priority>",
                "    </url>",
            ]
        )

    sitemap.append("</urlset>")

    output = DIST_DIR / "sitemap.xml"

    output.write_text(
        "\n".join(sitemap) + "\n",
        encoding="utf-8",
    )

    print(
        f"🗺️ Wrote {output}"
    )


# ============================================================
# Main
# ============================================================

def main():

    if not HOMEPAGE_JSON.exists():

        raise FileNotFoundError(
            f"Missing {HOMEPAGE_JSON}"
        )

    with HOMEPAGE_JSON.open(
        encoding="utf-8"
    ) as file:

        categories = json.load(file)

    build_sitemap(categories)


if __name__ == "__main__":
    main()