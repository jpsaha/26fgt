#!/usr/bin/env python3

"""
Fix equation-number rendering in generated HTML.

Typst's HTML output currently produces labelled equations like:

    <math id="eqn-ab" display="block">...</math>

but does not render the equation number visually.

This script:

1. Processes dist/pages/*.html.
2. Finds block equations with an id.
3. Inserts a visible equation number.
4. Preserves the equation id so internal references continue to work.
5. Wraps the equation and number in .html-equation.
6. Injects the equation-only stylesheet.

Example:

    Before:

        <math id="eqn-ab" display="block">...</math>

    After:

        <div class="html-equation">
          <math id="eqn-ab" display="block">...</math>
          <span class="html-equation-number">(1)</span>
        </div>

The numbering is determined from the order of labelled block
equations in each lecture page.

This is deliberately an HTML post-processing step. PDF equation
numbering remains entirely under Typst's control.
"""

from pathlib import Path
import re
import sys


# ============================================================
# Project root
# ============================================================

from scripts.config import (
    PAGES_DIR,
    ROOT,
)


# ============================================================
# Equation-only stylesheet
# ============================================================

EQUATION_STYLESHEET = (
    '<link rel="stylesheet" '
    'href="../assets/css/html-equations.css">\n'
)


# ============================================================
# Equation pattern
# ============================================================

EQUATION_RE = re.compile(
    r'(?P<equation>'
    r'<math\b'
    r'(?P<attrs>[^>]*\bid="(?P<id>[^"]+)"[^>]*)'
    r'\bdisplay="block"'
    r'[^>]*>'
    r'.*?'
    r'</math>'
    r')',
    re.IGNORECASE | re.DOTALL,
)


# ============================================================
# Equation number
# ============================================================

def equation_number(index):
    """
    Return the visible HTML equation number.

    Example:

        1 -> (1)
        2 -> (2)
    """

    return f"({index})"


# ============================================================
# Build replacement
# ============================================================

def make_equation_html(
    equation,
    number,
):
    """
    Wrap one block equation in the HTML equation container.
    """

    return (
        '<div class="html-equation">'
        + equation
        + '<span class="html-equation-number">'
        + number
        + '</span>'
        + '</div>'
    )


# ============================================================
# Inject equation stylesheet
# ============================================================

def inject_equation_stylesheet(html):
    """
    Inject the equation-only stylesheet into <head>.

    The operation is idempotent.
    """

    # --------------------------------------------------------
    # Already present.
    # --------------------------------------------------------

    if "html-equations.css" in html:
        return html

    # --------------------------------------------------------
    # Every lecture HTML page should have </head>.
    # --------------------------------------------------------

    if "</head>" not in html:

        raise RuntimeError(
            "Generated HTML has no </head>"
        )

    return html.replace(
        "</head>",
        f"    {EQUATION_STYLESHEET}</head>",
        1,
    )


# ============================================================
# Fix one HTML file
# ============================================================

def fix_file(html_path):
    """
    Fix labelled block equations in one HTML file.

    Returns:

        (number_of_equations, number_of_changes)
    """

    html = html_path.read_text(
        encoding="utf-8"
    )

    equation_count = 0
    changes = 0

    # --------------------------------------------------------
    # Equation replacement
    # --------------------------------------------------------

    def replace(match):

        nonlocal equation_count
        nonlocal changes

        equation = match.group("equation")
        anchor = match.group("id")

        # ----------------------------------------------------
        # Do not process equations already inside our wrapper.
        #
        # Find the most recent wrapper and the most recent
        # closing div before this equation. If the wrapper is
        # more recent, the equation is already wrapped.
        #
        # This makes the transformation idempotent and avoids
        # relying on a fixed number of preceding characters.
        # ----------------------------------------------------

        start = match.start()

        preceding = html[:start]

        last_wrapper = preceding.rfind(
            '<div class="html-equation"'
        )

        last_close = preceding.rfind(
            '</div>'
        )

        if last_wrapper > last_close:
            return equation

        # ----------------------------------------------------
        # This is a new labelled block equation.
        # ----------------------------------------------------

        equation_count += 1

        number = equation_number(
            equation_count
        )

        changes += 1

        print(
            f"  ✓ #{equation_count:<4}"
            f"{anchor:<30}"
            f" → {number}"
        )

        return make_equation_html(
            equation,
            number,
        )

    # --------------------------------------------------------
    # Transform equations.
    # --------------------------------------------------------

    updated = EQUATION_RE.sub(
        replace,
        html,
    )

    # --------------------------------------------------------
    # Inject equation-only CSS.
    #
    # This is intentionally done here rather than in
    # build_html.py so that the normal lecture-page styling
    # remains untouched.
    # --------------------------------------------------------

    updated = inject_equation_stylesheet(
        updated
    )

    # --------------------------------------------------------
    # Write only if changed.
    # --------------------------------------------------------

    if updated != html:

        html_path.write_text(
            updated,
            encoding="utf-8",
        )

    return equation_count, changes


# ============================================================
# Main
# ============================================================

def main():

    print()
    print("🔢 Fixing HTML equation numbers")
    print("================================")

    html_files = sorted(
        PAGES_DIR.glob("*.html")
    )

    if not html_files:

        print(
            f"ERROR: no HTML files found in {PAGES_DIR}"
        )

        return 1

    total_equations = 0
    total_changes = 0

    for html_path in html_files:

        print()
        print(
            f"📖 {html_path.name}"
        )

        equations, changes = fix_file(
            html_path
        )

        total_equations += equations
        total_changes += changes

    print()
    print(
        f"✓ HTML pages        : {len(html_files)}"
    )

    print(
        f"✓ Equations found   : {total_equations}"
    )

    print(
        f"✓ Equations changed : {total_changes}"
    )

    print()

    return 0


# ============================================================
# Entry point
# ============================================================

if __name__ == "__main__":

    raise SystemExit(
        main()
    )