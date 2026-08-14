#!/usr/bin/env python3

"""
Analyze Typst import dependencies.

Checks:

1. Scans project Typst source files.
2. Builds an import dependency graph.
3. Detects missing imports.
4. Detects circular imports.
5. Reports top-level files.
6. Reports leaf modules.
7. Writes a Graphviz dependency graph.
8. Reports unreadable Typst files.

Usage:

    python3 scripts/lint/check_imports.py

Exit status:

    0   no problems
    1   missing imports, unreadable files, or circular imports
"""

import sys

# ============================================================
# Paths
# ============================================================

from scripts.config import (
    CONTENT_DIR,
    GENERATED_DIR,
    TEMPLATES_DIR,
    BOOK_SOURCE,
    PAGES_SOURCE,
    PDFLAYOUT,
)

from scripts.lint.imports.graph import build_graph, find_cycles
from scripts.lint.imports.report import (
    print_dependency_tree,
    print_missing,
    print_unreadable,
    print_cycles,
    print_roots,
    print_leaves,
    write_graphviz,
)

# ============================================================
# Configuration
# ============================================================

TYPST_DIRS = (
    CONTENT_DIR,
    TEMPLATES_DIR,
    GENERATED_DIR,
)

TYPST_FILES = (
    BOOK_SOURCE,
    PAGES_SOURCE,
    PDFLAYOUT,
)

# ============================================================
# Discover Typst files
# ============================================================

def discover_typst_files():
    """Return all Typst files that belong to the project."""

    files = set()

    for directory in TYPST_DIRS:

        if not directory.exists():
            continue

        files.update(
            path.resolve()
            for path in directory.rglob("*.typ")
        )

    for path in TYPST_FILES:

        if path.exists() and path.is_file():
            files.add(path.resolve())

    return files

# ============================================================
# Main
# ============================================================

def main():

    files = discover_typst_files()

    if not files:

        print(
            "ERROR: no Typst files found."
        )

        return 1

    (
        graph,
        reverse,
        missing,
        unreadable,
    ) = build_graph(
        files
    )

    # --------------------------------------------------------
    # Top-level files
    # --------------------------------------------------------

    roots = [
        path
        for path in files
        if not reverse[path]
    ]

    # --------------------------------------------------------
    # Dependency tree
    # --------------------------------------------------------

    print_dependency_tree(
        roots,
        graph,
    )

    # --------------------------------------------------------
    # Missing imports
    # --------------------------------------------------------

    print_missing(
        missing
    )

    # --------------------------------------------------------
    # Unreadable files
    # --------------------------------------------------------

    print_unreadable(
        unreadable
    )

    # --------------------------------------------------------
    # Cycles
    # --------------------------------------------------------

    cycles = find_cycles(
        files,
        graph,
    )

    print_cycles(
        cycles
    )

    # --------------------------------------------------------
    # Roots
    # --------------------------------------------------------

    print_roots(
        roots
    )

    # --------------------------------------------------------
    # Leaves
    # --------------------------------------------------------

    print_leaves(
        files,
        graph,
    )

    # --------------------------------------------------------
    # Graphviz
    # --------------------------------------------------------

    write_graphviz(
        files,
        graph,
    )

    # --------------------------------------------------------
    # Summary
    # --------------------------------------------------------

    print()
    print(
        "=============================="
    )
    print(
        "Import Check"
    )
    print(
        "==============================\n"
    )

    import_count = sum(
        len(targets)
        for targets in graph.values()
    )

    print(
        f"Typst files : {len(files)}"
    )

    print(
        f"Imports     : {import_count}"
    )

    print(
        f"Missing     : {len(missing)}"
    )

    print(
        f"Unreadable  : {len(unreadable)}"
    )

    print(
        f"Cycles      : {len(cycles)}"
    )

    if missing or unreadable or cycles:

        print()
        print(
            "❌ Import check failed."
        )

        return 1

    print()
    print(
        "✅ Import check passed."
    )

    return 0


if __name__ == "__main__":
    sys.exit(main())