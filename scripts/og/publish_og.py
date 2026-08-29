#!/usr/bin/env python3

"""
Publish generated Open Graph PNG images.

Input:
    generated/og/**/*.png

Output:
    dist/assets/og/**/*.png

The directory structure is preserved.
"""

import shutil

from scripts.config import (
    ROOT,
    GENERATED_OG_DIR,
    ASSETS_DIR,
)


def publish_og_image(source):
    relative = source.relative_to(
        GENERATED_OG_DIR
    )

    destination = (
        ASSETS_DIR
        / "og"
        / relative
    )

    destination.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    shutil.copy2(
        source,
        destination,
    )

    print(
        f"📤 Published "
        f"{source.relative_to(ROOT)}"
        f" → "
        f"{destination.relative_to(ROOT)}"
    )


def main():

    if not GENERATED_OG_DIR.exists():
        print(
            "ℹ️  No generated OG directory found."
        )
        return

    sources = sorted(
        GENERATED_OG_DIR.rglob("*.png")
    )

    if not sources:
        print(
            "ℹ️  No generated OG PNG files found."
        )
        return

    print(
        f"📤 Found {len(sources)} "
        f"generated OG PNG(s)"
    )

    print()

    for source in sources:
        publish_og_image(source)

    print()

    print(
        "OG image publishing complete."
    )


if __name__ == "__main__":
    main()