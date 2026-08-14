#!/usr/bin/env python3

import subprocess

from scripts.config import GENERATED_DIR, PDF_DIR


def main():
    PDF_DIR.mkdir(parents=True, exist_ok=True)

    category_count = 0

    for category_source in sorted(GENERATED_DIR.glob("category_*.typ")):

        category_name = category_source.stem
        output = PDF_DIR / f"{category_name}.pdf"

        print(f"  📖 Building {category_name}...")

        subprocess.run(
            [
                "typst",
                "compile",
                "--root",
                ".",
                str(category_source),
                str(output),
                "--input",
                "format=pdf",
            ],
            check=True,
        )

        category_count += 1

    print(f"📚 Built {category_count} category books.")


if __name__ == "__main__":
    main()