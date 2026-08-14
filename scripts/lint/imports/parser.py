
"""
Parsing helpers for Typst source files.

This module is responsible only for understanding the contents
of Typst files. It does not know about the project dependency
graph or reporting.
"""

import re

IMPORT_RE = re.compile(
    r'#import\s+"([^"]+)"'
)


def remove_comments(text):
    """
    Remove Typst comments while preserving strings.

    Supports:

        // line comments

        /*
           block comments
        */

    Comment markers appearing inside quoted strings are preserved.
    """

    result = []

    i = 0
    length = len(text)

    in_string = False
    in_line_comment = False
    in_block_comment = False
    escaped = False

    while i < length:

        char = text[i]

        # ----------------------------------------------------
        # Line comment
        # ----------------------------------------------------

        if in_line_comment:

            if char == "\n":

                in_line_comment = False
                result.append(char)

            i += 1
            continue

        # ----------------------------------------------------
        # Block comment
        # ----------------------------------------------------

        if in_block_comment:

            if (
                char == "*"
                and i + 1 < length
                and text[i + 1] == "/"
            ):

                in_block_comment = False
                i += 2
                continue

            # Preserve newlines so that the resulting text
            # retains approximately the original structure.
            if char == "\n":
                result.append("\n")

            i += 1
            continue

        # ----------------------------------------------------
        # Quoted string
        # ----------------------------------------------------

        if in_string:

            result.append(char)

            if escaped:

                escaped = False

            elif char == "\\":

                escaped = True

            elif char == '"':

                in_string = False

            i += 1
            continue

        # ----------------------------------------------------
        # Start quoted string
        # ----------------------------------------------------

        if char == '"':

            in_string = True
            result.append(char)
            i += 1
            continue

        # ----------------------------------------------------
        # Start line comment
        # ----------------------------------------------------

        if (
            char == "/"
            and i + 1 < length
            and text[i + 1] == "/"
        ):

            in_line_comment = True
            i += 2
            continue

        # ----------------------------------------------------
        # Start block comment
        # ----------------------------------------------------

        if (
            char == "/"
            and i + 1 < length
            and text[i + 1] == "*"
        ):

            in_block_comment = True
            i += 2
            continue

        # ----------------------------------------------------
        # Normal character
        # ----------------------------------------------------

        result.append(char)
        i += 1

    return "".join(result)

def find_imports(text):
    """
    Return local Typst import paths found in source text.

    Comments must already have been removed before calling this
    function.
    """

    return [
        match.group(1)
        for match in IMPORT_RE.finditer(text)
        if not match.group(1).startswith("@")
    ]
