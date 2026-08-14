import json

from .config import HOMEPAGE_TYP, HOMEPAGE_JSON
from .typst import write_field, write_header


# ============================================================
# homepage.typ
# ============================================================

def write_homepage_typ(lectures):
    """Generate generated/homepage.typ."""

    fields = (
        "number",
        "title",
        "category",
        "date",
        "reading",
        "duration",
    )

    with HOMEPAGE_TYP.open(
        "w",
        encoding="utf-8",
    ) as file:

        write_header(file, "python3 scripts/run.py metadata")

        file.write(
            "#let homepage = (\n"
        )

        for lecture in lectures:

            # Homepage currently contains
            # numbered lectures only.
            if lecture.get("number") is None:
                continue

            file.write(
                "  (\n"
            )

            for key in fields:

                if key not in lecture:
                    continue

                write_field(
                    file,
                    key,
                    lecture[key],
                    indent=4,
                )

            write_field(
                file,
                "html",
                f'{lecture["file"]}.html',
                indent=4,
            )

            write_field(
                file,
                "pdf",
                f'{lecture["file"]}.pdf',
                indent=4,
            )

            file.write(
                "  ),\n"
            )

        file.write(
            ")\n"
        )

    print(
        f"Wrote {HOMEPAGE_TYP}"
    )


# ============================================================
# homepage.json
# ============================================================

def homepage_entry(item):
    """Convert one lecture/page into a homepage JSON entry."""

    return {
        "title": item["title"],
        "html": f'{item["file"]}.html',
        "pdf": f'{item["file"]}.pdf',

        **{
            key: value
            for key, value in item.items()
            if key not in (
                "file",
                "title",
                "category",
                "previous",
                "next",
            )
        },
    }


def build_homepage_data(lectures, pages):
    """Build the homepage data grouped by category."""

    homepage = {}

    for item in lectures + pages:

        category = item.get(
            "category",
            "Uncategorized",
        )

        homepage.setdefault(
            category,
            [],
        )

        homepage[category].append(
            homepage_entry(item)
        )

    return homepage


def write_homepage_json(lectures, pages):
    """Generate generated/homepage.json."""

    homepage = build_homepage_data(
        lectures,
        pages,
    )

    with HOMEPAGE_JSON.open(
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            homepage,
            file,
            indent=2,
            ensure_ascii=False,
        )

    print(
        f"Wrote {HOMEPAGE_JSON}"
    )


# ============================================================
# Public function
# ============================================================

def write_homepage(lectures, pages):
    """Generate all homepage files."""

    write_homepage_typ(
        lectures
    )

    write_homepage_json(
        lectures,
        pages
    )
