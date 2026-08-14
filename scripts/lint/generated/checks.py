import re
from scripts.config import (
    CONTENT_DIR,
    LECTURES_TYP,
    PAGES_TYP,
    PAGES_META_TYP,
    GENERATED_DIR,
)
from .config import (
    FILE_FIELD_RE,
    CONTENT_INCLUDE_RE,
)

# ============================================================
# Path helpers
# ============================================================

def safe_filename(name):
    """
    Convert a category name to the same filename form used
    by write_book.py.
    """

    name = name.lower().strip()

    name = re.sub(
        r"[^a-z0-9]+",
        "_",
        name,
    )

    return name.strip("_")


# ============================================================
# Generated identifiers
# ============================================================

def generated_file_ids(path):
    """
    Extract file identifiers from a generated metadata file.

    Returns a set of identifiers.
    """

    if not path.exists():

        return set()

    text = path.read_text(
        encoding="utf-8"
    )

    return set(
        FILE_FIELD_RE.findall(text)
    )


def generated_content_sources(path):
    """
    Extract content source filenames from a generated page file.
    """

    if not path.exists():

        return set()

    text = path.read_text(
        encoding="utf-8"
    )

    return set(
        CONTENT_INCLUDE_RE.findall(text)
    )


# ============================================================
# Generated file checks
# ============================================================

def check_required_file(
    path,
    errors,
):
    """Check that a generated file exists."""

    if not path.is_file():

        errors.append(
            (
                path,
                "generated file is missing",
            )
        )

        return False

    return True


def check_lectures(
    lectures,
    errors,
):
    """Check generated/lectures.typ against source lectures."""

    if not check_required_file(
        LECTURES_TYP,
        errors,
    ):

        return

    generated = generated_file_ids(
        LECTURES_TYP
    )

    expected = {
        data.get("file")
        for _, data in lectures
        if isinstance(
            data.get("file"),
            str,
        )
    }

    # --------------------------------------------------------
    # Missing lectures
    # --------------------------------------------------------

    for file_name in sorted(
        expected - generated
    ):

        errors.append(
            (
                LECTURES_TYP,
                (
                    f"source lecture '{file_name}' "
                    "is missing from generated lectures"
                ),
            )
        )

    # --------------------------------------------------------
    # Stale lectures
    # --------------------------------------------------------

    for file_name in sorted(
        generated - expected
    ):

        errors.append(
            (
                LECTURES_TYP,
                (
                    f"generated lecture '{file_name}' "
                    "has no source metadata"
                ),
            )
        )


# ============================================================
# Page checks
# ============================================================

def expected_page_sources(pages):
    """
    Return expected generated page content filenames.

    The source path is relative to content/.

    Example:

        content/courses/fun.typ

    becomes:

        courses/fun_content.typ
    """

    sources = set()

    for path, _ in pages:

        source = path.relative_to(
            CONTENT_DIR
        ).as_posix()

        if source.endswith(".typ"):

            source = source[:-4]

        sources.add(
            f"{source}_content.typ"
        )

    return sources


def check_pages(
    pages,
    errors,
):
    """Check generated page files against source pages."""

    expected_files = {
        data.get("file")
        for _, data in pages
        if isinstance(
            data.get("file"),
            str,
        )
    }

    # ========================================================
    # pages.typ
    # ========================================================

    if check_required_file(
        PAGES_TYP,
        errors,
    ):

        generated_sources = (
            generated_content_sources(
                PAGES_TYP
            )
        )

        expected_sources = (
            expected_page_sources(
                pages
            )
        )

        # ----------------------------------------------------
        # Missing pages
        # ----------------------------------------------------

        for source in sorted(
            expected_sources - generated_sources
        ):

            errors.append(
                (
                    PAGES_TYP,
                    (
                        f"source page content '{source}' "
                        "is missing from generated pages"
                    ),
                )
            )

        # ----------------------------------------------------
        # Stale pages
        # ----------------------------------------------------

        for source in sorted(
            generated_sources - expected_sources
        ):

            errors.append(
                (
                    PAGES_TYP,
                    (
                        f"generated page content '{source}' "
                        "has no source page metadata"
                    ),
                )
            )

    # ========================================================
    # pages_meta.typ
    # ========================================================

    if check_required_file(
        PAGES_META_TYP,
        errors,
    ):

        generated = generated_file_ids(
            PAGES_META_TYP
        )

        # ----------------------------------------------------
        # Missing page metadata
        # ----------------------------------------------------

        for file_name in sorted(
            expected_files - generated
        ):

            errors.append(
                (
                    PAGES_META_TYP,
                    (
                        f"source page '{file_name}' "
                        "is missing from generated page metadata"
                    ),
                )
            )

        # ----------------------------------------------------
        # Stale page metadata
        # ----------------------------------------------------

        for file_name in sorted(
            generated - expected_files
        ):

            errors.append(
                (
                    PAGES_META_TYP,
                    (
                        f"generated page '{file_name}' "
                        "has no source page metadata"
                    ),
                )
            )


# ============================================================
# Category books
# ============================================================

def expected_categories(content):
    """
    Return the set of category-generated filenames required
    by the current metadata-bearing content.
    """

    categories = set()

    for _, data in content:

        category = data.get(
            "category",
            "Uncategorized",
        )

        if not isinstance(category, str):
            continue

        filename = safe_filename(
            category
        )

        categories.add(
            f"category_{filename}.typ"
        )

    return categories


def check_category_books(
    content,
    errors,
):
    """Check generated category books."""

    if not GENERATED_DIR.exists():

        errors.append(
            (
                GENERATED_DIR,
                "generated directory does not exist",
            )
        )

        return

    expected = expected_categories(
        content
    )

    actual = {
        path.name
        for path in GENERATED_DIR.glob(
            "category_*.typ"
        )
    }

    # --------------------------------------------------------
    # Missing category books
    # --------------------------------------------------------

    for filename in sorted(
        expected - actual
    ):

        errors.append(
            (
                GENERATED_DIR / filename,
                "generated category book is missing",
            )
        )

    # --------------------------------------------------------
    # Stale category books
    # --------------------------------------------------------

    for filename in sorted(
        actual - expected
    ):

        errors.append(
            (
                GENERATED_DIR / filename,
                "stale category book exists",
            )
        )
