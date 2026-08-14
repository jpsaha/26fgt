from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]

from scripts.config import ROOT, DIAGNOSTICS_DIR, IMPORTS_DOT

# ============================================================
# Path formatting
# ============================================================

def display_path(path):
    """
    Return a readable path.

    Paths inside the repository are displayed relative to ROOT.
    Paths outside the repository are displayed as absolute paths.
    """

    try:
        return path.relative_to(ROOT).as_posix()

    except ValueError:
        return path.as_posix()


# ============================================================
# Dependency tree
# ============================================================

def print_tree(
    node,
    graph,
    prefix="",
    seen=None,
):
    """Print the dependency tree rooted at node."""

    if seen is None:
        seen = set()

    print(
        prefix + display_path(node)
    )

    if node in seen:

        print(
            prefix + "  ↺"
        )

        return

    seen = seen | {node}

    for child in graph[node]:

        print_tree(
            child,
            graph,
            prefix + "    ",
            seen,
        )


def print_dependency_tree(
    roots,
    graph,
):
    """Print dependency trees."""

    print(
        "\n=============================="
    )
    print(
        "Dependency Tree"
    )
    print(
        "==============================\n"
    )

    for root in sorted(roots):

        print_tree(
            root,
            graph,
        )

        print()


def print_cycles(cycles):
    """Print circular imports."""

    print(
        "=============================="
    )
    print(
        "Cycle Detection"
    )
    print(
        "==============================\n"
    )

    if not cycles:

        print(
            "No circular imports.\n"
        )

        return

    for cycle in cycles:

        print(
            "Circular import:"
        )

        for path in cycle:

            print(
                "   ",
                display_path(path),
            )

        print()

# ============================================================
# Missing imports
# ============================================================

def print_missing(missing):
    """Print missing imports."""

    print(
        "=============================="
    )
    print(
        "Missing Imports"
    )
    print(
        "==============================\n"
    )

    if not missing:

        print(
            "No missing imports.\n"
        )

        return

    for source, target in missing:

        print(
            display_path(source)
        )

        print(
            f"   -> {display_path(target)}"
        )

        print(
            "      [NOT FOUND]\n"
        )


# ============================================================
# Unreadable files
# ============================================================

def print_unreadable(unreadable):
    """Print Typst files that could not be read."""

    print(
        "=============================="
    )
    print(
        "Unreadable Files"
    )
    print(
        "==============================\n"
    )

    if not unreadable:

        print(
            "No unreadable files.\n"
        )

        return

    for path, error in unreadable:

        print(
            display_path(path)
        )

        print(
            f"   -> {error}\n"
        )


# ============================================================
# Top-level files
# ============================================================

def print_roots(
    roots,
):
    """Print files that are not imported by another file."""

    print(
        "=============================="
    )
    print(
        "Top-level files"
    )
    print(
        "==============================\n"
    )

    for path in sorted(roots):

        print(
            display_path(path)
        )

    print()


# ============================================================
# Leaves
# ============================================================

def print_leaves(
    files,
    graph,
):
    """Print files that import nothing."""

    print(
        "=============================="
    )
    print(
        "Leaf modules"
    )
    print(
        "==============================\n"
    )

    for path in sorted(files):

        if not graph[path]:

            print(
                display_path(path)
            )

    print()


# ============================================================
# Graphviz
# ============================================================

def write_graphviz(
    files,
    graph,
):
    """Write the import graph as Graphviz IMPORTS_DOT."""

    DIAGNOSTICS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    with IMPORTS_DOT.open(
        "w",
        encoding="utf-8",
    ) as file:

        file.write(
            "digraph Imports {\n"
        )

        file.write(
            "rankdir=LR;\n\n"
        )

        for source in sorted(files):

            source_name = display_path(source)

            if not graph[source]:

                file.write(
                    f'"{source_name}";\n'
                )

            for target in graph[source]:

                target_name = display_path(target)

                file.write(
                    f'"{source_name}" '
                    f'-> '
                    f'"{target_name}";\n'
                )

        file.write(
            "}\n"
        )

    print(
        "=============================="
    )

    print(
        "Graphviz"
    )

    print(
        "==============================\n"
    )

    print(
        f"Wrote {IMPORTS_DOT.relative_to(ROOT)}"
    )
