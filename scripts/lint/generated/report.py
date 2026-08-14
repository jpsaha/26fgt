from scripts.config import ROOT

# ============================================================
# Path formatting
# ============================================================

def display_path(path):
    """Return a path relative to the project root."""

    try:

        return path.relative_to(
            ROOT
        ).as_posix()

    except ValueError:

        return path.as_posix()
