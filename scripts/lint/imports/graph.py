from collections import defaultdict
from .parser import remove_comments, find_imports

# ============================================================
# Build dependency graph
# ============================================================

def build_graph(files):
    """
    Build the Typst import graph.

    Returns:

        graph:
            source -> imported files

        reverse:
            imported file -> importing files

        missing:
            (source, target) pairs for missing imports

        unreadable:
            files that could not be read
    """

    graph = defaultdict(list)
    reverse = defaultdict(list)

    missing = []
    unreadable = []

    for path in sorted(files):

        try:

            text = path.read_text(
                encoding="utf-8"
            )

        except (OSError, UnicodeError) as error:

            unreadable.append(
                (path, error)
            )

            continue

        # --------------------------------------------------------
        # Ignore commented-out imports.
        #
        # This prevents lines such as:
        #
        #     // #import "main.typ": *
        #
        # and imports inside:
        #
        #     /*
        #     #import "main.typ": *
        #     */
        #
        # from being treated as real dependencies.
        #
        # Comment removal and import extraction are handled by
        # the parser module.
        # --------------------------------------------------------

        text = remove_comments(text)

        for import_path in find_imports(text):

            # ----------------------------------------------------
            # Ignore Typst package imports.
            #
            # Examples:
            #
            #     @preview/cetz:0.3.4
            #     @preview/gentle-clues:1.2.0
            #     @preview/theorion:0.6.0
            #
            # These are handled by Typst's package system and are
            # not local project files.
            # ----------------------------------------------------

            if import_path.startswith("@"):
                continue

            target = (
                path.parent / import_path
            ).resolve()

            graph[path].append(target)
            reverse[target].append(path)

            if not target.is_file():

                missing.append(
                    (path, target)
                )

    return (
        graph,
        reverse,
        missing,
        unreadable,
    )

# ============================================================
# Cycle detection
# ============================================================

def find_cycles(
    nodes,
    graph,
):
    """Return circular import paths."""

    cycles = []

    visited = set()
    stack = []

    def dfs(node):

        if node in stack:

            index = stack.index(node)

            cycles.append(
                stack[index:] + [node]
            )

            return

        if node in visited:
            return

        visited.add(node)
        stack.append(node)

        for child in graph[node]:

            # Missing imports cannot participate
            # in a meaningful cycle.
            if child.is_file():

                dfs(child)

        stack.pop()

    for node in sorted(nodes):
        dfs(node)

    return cycles

