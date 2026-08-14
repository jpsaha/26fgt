#!/usr/bin/env python3

"""
Validate Typst content metadata.

Checks:

1. Scans content/**/*.typ wrapper files.
2. Ignores *_content.typ files.
3. Verifies that metadata exists.
4. Verifies required metadata fields.
5. Validates metadata field types.
6. Checks duplicate file identifiers.
7. Checks the corresponding _content.typ file exists.
8. Checks that lecture numbers are valid when present.
9. Reports pages and lectures separately.
10. Returns non-zero if metadata is invalid.

The validator uses the same parser and content directory
as the metadata generation pipeline.

Usage:

    python3 scripts/lint/check_metadata.py

Exit status:

    0   metadata is valid
    1   metadata errors were found
"""

from pathlib import Path
import sys

from scripts.config import ROOT
from scripts.config import CONTENT_DIR
from scripts.metadata.parser import parse_lecture

# ============================================================
# Metadata rules
# ============================================================

REQUIRED_FIELDS = (
    "file",
    "title",
)


# ============================================================
# Path helpers
# ============================================================

def display_path(path):
    """Return a path relative to the project root."""

    try:

        return path.relative_to(
            ROOT
        ).as_posix()

    except ValueError:

        return path.as_posix()


def content_source(path):
    """
    Return the expected content file for a wrapper.

    Example:

        lec1.typ
        -> lec1_content.typ
    """

    return path.with_name(
        f"{path.stem}_content.typ"
    )


# ============================================================
# Validation
# ============================================================

def validate_metadata(path, data):
    """
    Validate metadata for one wrapper file.

    Returns:

        list[str]:
            validation error messages
    """

    errors = []

    # --------------------------------------------------------
    # Required fields
    # --------------------------------------------------------

    for key in REQUIRED_FIELDS:

        if key not in data:

            errors.append(
                f"missing required field '{key}'"
            )

            continue

        value = data[key]

        if not isinstance(value, str):

            errors.append(
                f"field '{key}' must be a string"
            )

        elif not value.strip():

            errors.append(
                f"field '{key}' must not be empty"
            )

    # --------------------------------------------------------
    # File identifier
    # --------------------------------------------------------

    file_name = data.get("file")

    if isinstance(file_name, str):

        if "/" in file_name or "\\" in file_name:

            errors.append(
                "field 'file' must be a filename, "
                "not a path"
            )

        if file_name.startswith("."):

            errors.append(
                "field 'file' must not start with '.'"
            )

    # --------------------------------------------------------
    # Title
    # --------------------------------------------------------

    title = data.get("title")

    if isinstance(title, str):

        if not title.strip():

            errors.append(
                "field 'title' must not be empty"
            )

    # --------------------------------------------------------
    # Number
    # --------------------------------------------------------
    #
    # The existing metadata pipeline intentionally allows
    # number to be absent or none for pages.
    #
    # A present number must therefore be an integer or None.
    # --------------------------------------------------------

    if "number" in data:

        number = data["number"]

        if number is not None and not isinstance(
            number,
            int,
        ):

            errors.append(
                "field 'number' must be an integer "
                "or none"
            )

        elif isinstance(number, int) and number < 0:

            errors.append(
                "field 'number' must not be negative"
            )

    # --------------------------------------------------------
    # Category
    # --------------------------------------------------------
    #
    # Category is optional because write_book.py explicitly
    # supports missing categories using "Uncategorized".
    # --------------------------------------------------------

    if "category" in data:

        category = data["category"]

        if not isinstance(category, str):

            errors.append(
                "field 'category' must be a string"
            )

        elif not category.strip():

            errors.append(
                "field 'category' must not be empty"
            )

    return errors


# ============================================================
# Main validation
# ============================================================

def main():

    if not CONTENT_DIR.exists():

        print(
            f"ERROR: {display_path(CONTENT_DIR)} "
            "does not exist."
        )

        return 1

    wrapper_files = sorted(
        path
        for path in CONTENT_DIR.rglob("*.typ")
        if not path.stem.endswith("_content")
        and "motypprog" not in path.relative_to(CONTENT_DIR).parts
    )

    if not wrapper_files:

        print(
            "ERROR: no content wrapper files found."
        )

        return 1

    errors = []

    lectures = []
    pages = []

    files_seen = {}

    metadata_count = 0

    # --------------------------------------------------------
    # Scan wrappers
    # --------------------------------------------------------

    for path in wrapper_files:

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

        data = parse_lecture(text)

        # ----------------------------------------------------
        # Metadata block
        # ----------------------------------------------------

        if data is None:

            errors.append(
                (
                    path,
                    "no '#let lecture = (...)' metadata block",
                )
            )

            continue

        metadata_count += 1

        # ----------------------------------------------------
        # Field validation
        # ----------------------------------------------------

        for message in validate_metadata(
            path,
            data,
        ):

            errors.append(
                (
                    path,
                    message,
                )
            )

        # ----------------------------------------------------
        # File identifier
        # ----------------------------------------------------

        file_name = data.get("file")

        if isinstance(file_name, str):

            if file_name in files_seen:

                errors.append(
                    (
                        path,
                        (
                            f"duplicate file identifier "
                            f"'{file_name}' "
                            f"(already used by "
                            f"{display_path(files_seen[file_name])})"
                        ),
                    )
                )

            else:

                files_seen[file_name] = path

        # ----------------------------------------------------
        # Expected content file
        # ----------------------------------------------------

        content = content_source(path)

        if not content.is_file():

            errors.append(
                (
                    path,
                    (
                        "missing content file: "
                        f"{display_path(content)}"
                    ),
                )
            )

        # ----------------------------------------------------
        # Classify
        # ----------------------------------------------------

        number = data.get("number")

        if number is None:

            pages.append(
                (path, data)
            )

        else:

            lectures.append(
                (path, data)
            )

    # ========================================================
    # Report
    # ========================================================

    print()
    print(
        "=============================="
    )
    print(
        "Metadata Check"
    )
    print(
        "=============================="
    )
    print()

    print(
        f"Wrapper files : {len(wrapper_files)}"
    )

    print(
        f"Metadata      : {metadata_count}"
    )

    print(
        f"Lectures      : {len(lectures)}"
    )

    print(
        f"Pages         : {len(pages)}"
    )

    print(
        f"Errors        : {len(errors)}"
    )

    # --------------------------------------------------------
    # Errors
    # --------------------------------------------------------

    if errors:

        print()
        print(
            "=============================="
        )
        print(
            "Metadata Errors"
        )
        print(
            "=============================="
        )
        print()

        for path, message in errors:

            print(
                display_path(path)
            )

            print(
                f"   -> {message}"
            )

            print()

        print(
            "❌ Metadata check failed."
        )

        return 1

    # --------------------------------------------------------
    # Successful validation
    # --------------------------------------------------------

    print()
    print(
        "No metadata errors found."
    )

    print()
    print(
        "✅ Metadata check passed."
    )

    return 0


# ============================================================
# Entry point
# ============================================================

if __name__ == "__main__":
    sys.exit(main())