from scripts.config import CONTENT_DIR
from .parser import parse_lecture


def discover_content():

    lectures = []
    pages = []

    for path in sorted(CONTENT_DIR.rglob("*.typ")):

        # Ignore content files; only process wrapper files.
        if path.stem.endswith("_content"):
            continue

        text = path.read_text(
            encoding="utf-8"
        )

        data = parse_lecture(text)

        if data is None:
            print(
                f"Skipping {path}: "
                "no metadata."
            )
            continue

        # ----------------------------------------------------
        # Derive source automatically from the actual location
        # ----------------------------------------------------

        data["source"] = (
            path
            .relative_to(CONTENT_DIR)
            .as_posix()
        )

        # ----------------------------------------------------
        # Classify
        # ----------------------------------------------------

        if data.get("number") is None:

            pages.append(data)

            print(
                f"Page:    {data['file']}"
            )

        else:

            lectures.append(data)

            print(
                f"Lecture: {data['file']}"
            )

    return lectures, pages