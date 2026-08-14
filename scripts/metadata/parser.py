#!/usr/bin/env python3

import re


# ============================================================
# Lecture metadata
# ============================================================

LECTURE_START_RE = re.compile(
    r"#let\s+lecture\s*=\s*\(",
    re.MULTILINE,
)


# ============================================================
# Balanced structure handling
# ============================================================

def find_matching_parenthesis(text, opening):
    """
    Find the closing ')' matching the '(' at `opening`.

    Parentheses inside strings are ignored.

    Nested (), [], and {} structures are supported.
    """

    pairs = {
        "(": ")",
        "[": "]",
        "{": "}",
    }

    stack = []

    in_string = False
    escaped = False

    for index in range(
        opening,
        len(text),
    ):

        char = text[index]

        # ----------------------------------------------------
        # Inside string
        # ----------------------------------------------------

        if in_string:

            if escaped:
                escaped = False
                continue

            if char == "\\":
                escaped = True
                continue

            if char == '"':
                in_string = False

            continue

        # ----------------------------------------------------
        # Start string
        # ----------------------------------------------------

        if char == '"':
            in_string = True
            continue

        # ----------------------------------------------------
        # Opening delimiter
        # ----------------------------------------------------

        if char in pairs:

            stack.append(char)
            continue

        # ----------------------------------------------------
        # Closing delimiter
        # ----------------------------------------------------

        if char in pairs.values():

            if not stack:
                return None

            expected = pairs[stack[-1]]

            if char != expected:
                return None

            stack.pop()

            if not stack:
                return index

    return None


# ============================================================
# Top-level splitting
# ============================================================

def split_top_level(text, delimiter=","):
    """
    Split text at top-level commas.

    Commas inside:

        (...)
        [...]
        {...}
        "..."

    are ignored.
    """

    parts = []

    start = 0

    stack = []

    pairs = {
        "(": ")",
        "[": "]",
        "{": "}",
    }

    reverse_pairs = {
        ")": "(",
        "]": "[",
        "}": "{",
    }

    in_string = False
    escaped = False

    for index, char in enumerate(text):

        # ----------------------------------------------------
        # String
        # ----------------------------------------------------

        if in_string:

            if escaped:
                escaped = False
                continue

            if char == "\\":
                escaped = True
                continue

            if char == '"':
                in_string = False

            continue

        if char == '"':
            in_string = True
            continue

        # ----------------------------------------------------
        # Nested structures
        # ----------------------------------------------------

        if char in pairs:

            stack.append(char)
            continue

        if char in reverse_pairs:

            if stack and stack[-1] == reverse_pairs[char]:
                stack.pop()

            continue

        # ----------------------------------------------------
        # Top-level delimiter
        # ----------------------------------------------------

        if (
            char == delimiter
            and not stack
        ):

            part = text[
                start:index
            ].strip()

            if part:
                parts.append(part)

            start = index + 1

    # --------------------------------------------------------
    # Final part
    # --------------------------------------------------------

    final = text[start:].strip()

    if final:
        parts.append(final)

    return parts


# ============================================================
# Key/value splitting
# ============================================================

def split_key_value(text):
    """
    Split:

        tags: ["linear-map", "matrices"]

    into:

        tags
        ["linear-map", "matrices"]

    Only a colon at the top level is considered.
    """

    stack = []

    pairs = {
        "(": ")",
        "[": "]",
        "{": "}",
    }

    reverse_pairs = {
        ")": "(",
        "]": "[",
        "}": "{",
    }

    in_string = False
    escaped = False

    for index, char in enumerate(text):

        # ----------------------------------------------------
        # String
        # ----------------------------------------------------

        if in_string:

            if escaped:
                escaped = False
                continue

            if char == "\\":
                escaped = True
                continue

            if char == '"':
                in_string = False

            continue

        if char == '"':
            in_string = True
            continue

        # ----------------------------------------------------
        # Nested structures
        # ----------------------------------------------------

        if char in pairs:

            stack.append(char)
            continue

        if char in reverse_pairs:

            if stack and stack[-1] == reverse_pairs[char]:
                stack.pop()

            continue

        # ----------------------------------------------------
        # Top-level colon
        # ----------------------------------------------------

        if char == ":" and not stack:

            key = text[:index].strip()
            value = text[index + 1:].strip()

            return key, value

    return None, None


# ============================================================
# Value parser
# ============================================================

def parse_value(value):
    """
    Convert a Typst metadata value to Python.

    Supported:

        "text"
        123
        true
        false
        none
        ("a", "b")
        ["a", "b"]

    Unknown Typst expressions are preserved as strings.

    Examples:

        datetime(year: 2026, month: 8, day: 1)

    remains:

        datetime(year: 2026, month: 8, day: 1)
    """

    value = value.strip()

    # --------------------------------------------------------
    # String
    # --------------------------------------------------------

    if (
        len(value) >= 2
        and value.startswith('"')
        and value.endswith('"')
    ):
        return value[1:-1]

    # --------------------------------------------------------
    # none
    # --------------------------------------------------------

    if value == "none":
        return None

    # --------------------------------------------------------
    # Boolean
    # --------------------------------------------------------

    if value == "true":
        return True

    if value == "false":
        return False

    # --------------------------------------------------------
    # Integer
    # --------------------------------------------------------

    try:
        return int(value)

    except ValueError:
        pass

    # --------------------------------------------------------
    # Tuple
    # --------------------------------------------------------

    if (
        value.startswith("(")
        and value.endswith(")")
    ):

        closing = find_matching_parenthesis(
            value,
            0,
        )

        if closing == len(value) - 1:

            inner = value[1:-1].strip()

            if not inner:
                return ()

            return tuple(
                parse_value(item)
                for item in split_top_level(inner)
            )

    # --------------------------------------------------------
    # Array
    # --------------------------------------------------------

    if (
        value.startswith("[")
        and value.endswith("]")
    ):

        closing = find_matching_parenthesis(
            value,
            0,
        )

        if closing == len(value) - 1:

            inner = value[1:-1].strip()

            if not inner:
                return []

            return [
                parse_value(item)
                for item in split_top_level(inner)
            ]

    # --------------------------------------------------------
    # Fallback
    # --------------------------------------------------------

    return value


# ============================================================
# Lecture block
# ============================================================

def find_lecture_block(text):
    """
    Extract the complete outer:

        #let lecture = (...)

    record.

    Nested parentheses, arrays, strings, etc. are handled
    correctly.
    """

    match = LECTURE_START_RE.search(text)

    if match is None:
        return None

    opening = (
        match.end() - 1
    )

    closing = find_matching_parenthesis(
        text,
        opening,
    )

    if closing is None:
        return None

    return text[
        opening + 1 : closing
    ]


# ============================================================
# Main parser
# ============================================================

def parse_lecture(text):
    """
    Extract lecture metadata.

    Returns:

        dict

    or:

        None
    """

    body = find_lecture_block(text)

    if body is None:
        return None

    lecture = {}

    fields = split_top_level(body)

    for field in fields:

        field = field.strip()

        if not field:
            continue

        # ----------------------------------------------------
        # Ignore comments
        # ----------------------------------------------------

        if field.startswith("//"):
            continue

        key, value = split_key_value(field)

        if key is None:
            continue

        lecture[key] = parse_value(value)

    return lecture