import subprocess

from scripts.config import PDF_DIR, ROOT


def main():
    PDF_DIR.mkdir(parents=True, exist_ok=True)

    output = PDF_DIR / "book.pdf"

    print("📚 Building complete course book...")

    subprocess.run(
        [
            "typst",
            "compile",
            "--root",
            str(ROOT),
            "book_source.typ",
            str(output),
            "--input",
            "format=pdf",
        ],
        check=True,
    )


if __name__ == "__main__":
    main()