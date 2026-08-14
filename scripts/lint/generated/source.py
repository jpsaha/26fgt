from scripts.config import CONTENT_DIR
from scripts.metadata.parser import parse_lecture

# ============================================================
# Source metadata
# ============================================================

def discover_source_metadata():
    """
    Discover source wrapper metadata.

    Returns:

        wrappers
        lectures
        pages
        errors
    """

    wrappers = []

    lectures = []

    pages = []

    errors = []

    if not CONTENT_DIR.exists():

        errors.append(
            (
                CONTENT_DIR,
                "content directory does not exist",
            )
        )

        return (
            wrappers,
            lectures,
            pages,
            errors,
        )

    for path in sorted(
        path
        for path in CONTENT_DIR.rglob("*.typ")
        if "motypprog" not in path.parts
    ):

        # ----------------------------------------------------
        # Ignore generated content files
        # ----------------------------------------------------

        if path.stem.endswith("_content"):
            continue

        # ----------------------------------------------------
        # Read source
        # ----------------------------------------------------

        try:

            text = path.read_text(
                encoding="utf-8"
            )

        except (OSError, UnicodeError) as error:

            errors.append(
                (
                    path,
                    f"could not read file: {error}",
                )
            )

            continue

        # ----------------------------------------------------
        # Parse metadata
        # ----------------------------------------------------

        data = parse_lecture(text)

        if data is None:

            errors.append(
                (
                    path,
                    "no metadata block found",
                )
            )

            continue

        wrappers.append(
            (path, data)
        )

        # ----------------------------------------------------
        # Classify
        #
        # number == None  -> page
        # number != None  -> lecture
        # ----------------------------------------------------

        if data.get("number") is None:

            pages.append(
                (path, data)
            )

        else:

            lectures.append(
                (path, data)
            )

    return (
        wrappers,
        lectures,
        pages,
        errors,
    )

