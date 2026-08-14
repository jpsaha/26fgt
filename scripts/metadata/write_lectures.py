from .config import LECTURES_TYP
from .typst import write_field, write_header


def write_navigation(file, key, navigation):
    """Write a previous/next navigation field."""

    if navigation is None:

        write_field(
            file,
            key,
            None,
            indent=4,
        )

        return

    file.write(
        f"    {key}: (\n"
    )

    write_field(
        file,
        "title",
        navigation["title"],
        indent=6,
    )

    write_field(
        file,
        "html",
        navigation["html"],
        indent=6,
    )

    file.write(
        "    ),\n"
    )


def write_lecture(file, lecture):
    """Write one lecture record."""

    file.write(
        "  (\n"
    )

    # --------------------------------------------------------
    # Generated output paths
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # Lecture metadata
    # --------------------------------------------------------

    for key, value in lecture.items():

        if key in ("previous", "next"):
            continue

        write_field(
            file,
            key,
            value,
            indent=4,
        )

    # --------------------------------------------------------
    # Navigation
    # --------------------------------------------------------

    write_navigation(
        file,
        "previous",
        lecture.get("previous"),
    )

    write_navigation(
        file,
        "next",
        lecture.get("next"),
    )

    file.write(
        "  ),\n"
    )


def write_lectures(lectures):
    """Generate generated/lectures.typ."""

    with LECTURES_TYP.open(
        "w",
        encoding="utf-8",
    ) as file:

        write_header(file, "python3 scripts/run.py metadata")

        file.write(
            "#let lectures = (\n"
        )

        for lecture in lectures:
            write_lecture(
                file,
                lecture,
            )

        file.write(
            ")\n"
        )

    print(
        f"Wrote {LECTURES_TYP}"
    )
