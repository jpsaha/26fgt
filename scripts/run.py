#!/usr/bin/env python3

import subprocess
import sys


# ============================================================
# Command registry
#
# Each command maps to a Python module that can be executed
# with:
#
#     python3 -m <module>
#
# This file provides a single entry point for build.sh and
# keeps the shell script independent of the individual Python
# module names.
# 
# python3 scripts/run.py metadata
# python3 scripts/run.py metadata-check
# python3 scripts/run.py generated
# python3 scripts/run.py imports

# python3 scripts/run.py prepare-dist
# python3 scripts/run.py prepare-diagnostics

# python3 scripts/run.py html
# python3 scripts/run.py pdf
# python3 scripts/run.py categories
# python3 scripts/run.py book
# python3 scripts/run.py pages-pdf

# python3 scripts/run.py links
# python3 scripts/run.py report
# ============================================================

COMMANDS = {

    # --------------------------------------------------------
    # Generation
    # --------------------------------------------------------

    "metadata": "scripts.build.generate_metadata",

    # --------------------------------------------------------
    # Output
    # --------------------------------------------------------

    "html": "scripts.build.build_html",
    "pdf": "scripts.build.build_pdfs",
    "categories": "scripts.build.build_categories",
    "book": "scripts.build.build_book",
    "pages-pdf": "scripts.build.build_pages_pdf",

    # --------------------------------------------------------
    # Validation
    # --------------------------------------------------------

    "metadata-check": "scripts.lint.check_metadata",
    "generated": "scripts.lint.check_generated",
    "imports": "scripts.lint.check_imports",
    "links": "scripts.lint.check_links",

    # --------------------------------------------------------
    # Build infrastructure
    # --------------------------------------------------------

    "prepare-dist": "scripts.build.prepare_dist",
    "report": "scripts.build.build_report",

    # --------------------------------------------------------
    # Prepare diagnostics
    # --------------------------------------------------------
    
    "prepare-diagnostics": "scripts.build.prepare_diagnostics",
}


# ============================================================
# Main
# ============================================================

def main():

    # --------------------------------------------------------
    # Validate command
    # --------------------------------------------------------

    if len(sys.argv) != 2 or sys.argv[1] not in COMMANDS:

        print("Usage: python3 scripts/run.py <command>")
        print()
        print("Commands:")

        for command in COMMANDS:
            print(f"  {command}")

        return 1

    # --------------------------------------------------------
    # Resolve module
    # --------------------------------------------------------

    module = COMMANDS[sys.argv[1]]

    # --------------------------------------------------------
    # Execute module
    #
    # Use the same Python interpreter that invoked run.py.
    # This avoids accidentally using a different Python
    # installation or virtual environment.
    # --------------------------------------------------------

    result = subprocess.run(
        [sys.executable, "-m", module]
    )

    return result.returncode


# ============================================================
# Entry point
# ============================================================

if __name__ == "__main__":
    sys.exit(main())