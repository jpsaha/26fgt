#!/usr/bin/env python3

"""
Generate robots.txt.
"""

from scripts.config import (
    DIST_DIR,
    SITE_URL,
)


def main():

    sitemap = (
        SITE_URL.rstrip("/")
        + "/sitemap.xml"
    )

    content = (
        "User-agent: *\n"
        "Allow: /\n"
        "\n"
        f"Sitemap: {sitemap}\n"
    )

    output = DIST_DIR / "robots.txt"

    output.write_text(
        content,
        encoding="utf-8",
    )

    print(
        f"🤖 Wrote {output}"
    )


if __name__ == "__main__":
    main()