#!/usr/bin/env python3

import shutil

from scripts.config import DIAGNOSTICS_DIR


def prepare_diagnostics():
    """Prepare the diagnostics directory for a fresh build."""

    shutil.rmtree(
        DIAGNOSTICS_DIR,
        ignore_errors=True,
    )

    DIAGNOSTICS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )


def main():
    prepare_diagnostics()


if __name__ == "__main__":
    main()