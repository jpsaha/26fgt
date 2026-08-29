#!/usr/bin/env python3

"""
Audit project configuration usage.

This script checks Python files under scripts/ for configuration-like
values that may have been defined locally instead of being centralized
in scripts/config.py.

The script does NOT modify any files.

Report:
    diagnostics/config_report.txt

Checks:
    1. Constants defined in scripts/config.py.
    2. Configuration-like constants defined outside config.py.
    3. Implementation constants defined outside config.py.
    4. Path(...) constructions outside config.py.
    5. ROOT / ... path constructions.
    6. Hard-coded project directory names.
    7. Hard-coded project/site-specific strings.
    8. Configuration-like numeric constants.
    9. Imports from scripts.config.
   10. Local redefinitions of names imported from config.py.

Important:
    Not every uppercase constant belongs in config.py.

For example:

    REQUIRED_FIELDS
    LECTURE_START_RE
    IMPORT_RE
    COMMANDS

are implementation details of individual scripts.

By contrast:

    WIDTH
    HEIGHT
    DENSITY
    DIST_DIR
    SITE_URL
    CONTENT_DIR

are examples of values that may represent project configuration.

This script therefore separates uppercase constants into:

    Configuration constants
    Implementation constants

The report is an audit aid, not a strict linter.
"""


from pathlib import Path
import ast
import re


from scripts.config import (
    ROOT,
    CONTENT_DIR,
    DIST_DIR,
    DIAGNOSTICS_DIR,
    GENERATED_DIR,
    SCRIPTS_DIR,
    TEMPLATES_DIR,
    CONFIG_FILE,
    CONFIG_REPORT,
    PAGES_DIR,
    PDF_DIR,
    ASSETS_DIR,
)

from scripts.site_config import (
    GITHUB_USERNAME,
    REPO_NAME,
)


# ============================================================
# Audit files
# ============================================================
#
# This script audits project configuration usage.
#
# There are two intentional configuration modules:
#
#     scripts/config.py
#     scripts/site_config.py
#
# Neither should be reported as defining configuration
# "outside" the configuration modules.
#
# ============================================================

SITE_CONFIG_FILE = (
    SCRIPTS_DIR / "site_config.py"
)

AUDIT_FILE = Path(__file__).resolve()

CONFIG_MODULES = {
    CONFIG_FILE,
    SITE_CONFIG_FILE,
}


# ============================================================
# Configuration-like patterns
# ============================================================
#
# Project directory names are used by the text-based audit to
# detect hard-coded project paths in scripts.
#
# The directory names are derived from the centralized path
# constants in config.py rather than repeated as string literals.
#
# This includes both project-root directories and directories
# nested under dist/, such as:
#
#     dist/assets/
#     dist/pages/
#     dist/pdf/
#
# ============================================================

PROJECT_DIRECTORIES = {
    CONTENT_DIR.name,
    GENERATED_DIR.name,
    DIAGNOSTICS_DIR.name,
    DIST_DIR.name,
    SCRIPTS_DIR.name,
    TEMPLATES_DIR.name,
    PAGES_DIR.name,
    PDF_DIR.name,
    ASSETS_DIR.name,
}


# ============================================================
# Project-specific strings
# ============================================================
#
# These values identify this particular GitHub repository/site.
#
# They come from site_config.py so that the audit does not
# duplicate the actual project identity.
#
# ============================================================

PROJECT_STRINGS = {
    GITHUB_USERNAME,
    REPO_NAME,
}

# ------------------------------------------------------------
# Configuration-like numbers
# ------------------------------------------------------------
#
# These are currently known OG-image settings.
#
# They are included as an audit aid. If a script contains one
# of these numbers, the report asks us to review whether the
# value should instead come from config.py.
# ============================================================

CONFIG_LIKE_NUMBERS = {
    1200,
    630,
    300,
}


# ============================================================
# Constant classification
# ============================================================
#
# An uppercase name does NOT automatically mean that it belongs
# in config.py.
#
# The following names/patterns are normally implementation
# details rather than project configuration.
# ============================================================

IMPLEMENTATION_CONSTANT_NAMES = {
    # Validation / metadata
    "REQUIRED_FIELDS",

    # Command dispatch
    "COMMANDS",
    "COMMAND_GROUPS",
    "COMPOSITE_COMMANDS",

    # Import checking
    "TYPST_DIRS",
    "TYPST_FILES",

    # Regular expressions
    "IMPORT_RE",
    "FILE_FIELD_RE",
    "CONTENT_INCLUDE_RE",
    "LECTURE_START_RE",
    "LECTURE_METADATA_PATTERN",


    "EQUATION_STYLESHEET",

    # Metadata-specific generated paths/configuration
    # are intentionally NOT listed here if they represent
    # actual project paths. Those should come from config.py.
}


# ------------------------------------------------------------
# Implementation-name patterns
# ------------------------------------------------------------
#
# These patterns identify common implementation constants.
#
# They are deliberately conservative. A constant is only
# classified as implementation when there is a strong signal.
# ============================================================

IMPLEMENTATION_NAME_PATTERNS = (
    r".*_RE$",          # Regular expressions
    r".*_REGEX$",
    r".*_PATTERN$",
    r".*_FIELDS$",
    r".*_NAMES$",
    r".*_MAP$",
    r".*_MAPPING$",
)


# ============================================================
# Utilities
# ============================================================

def relative(path):
    """Return a project-relative path."""

    try:
        return path.relative_to(ROOT)

    except ValueError:
        return path


def source_line(source, lineno):
    """Return a source line, if available."""

    lines = source.splitlines()

    if 1 <= lineno <= len(lines):
        return lines[lineno - 1].strip()

    return ""


def add_finding(findings, category, path, lineno, text):
    """Add one finding to the report."""

    findings[category].append(
        (
            str(relative(path)),
            lineno,
            text,
        )
    )


# ============================================================
# AST helpers
# ============================================================

def imported_config_names(tree):
    """
    Return names imported from scripts.config.

    Handles:

        from scripts.config import ROOT

        from scripts.config import ROOT, DIST_DIR

        from scripts.config import ROOT as PROJECT_ROOT
    """

    names = {}

    for node in ast.walk(tree):

        if not isinstance(node, ast.ImportFrom):
            continue

        if node.module != "scripts.config":
            continue

        for alias in node.names:

            if alias.name == "*":
                continue

            local_name = alias.asname or alias.name

            names[local_name] = alias.name

    return names


def assigned_names(tree):
    """
    Return names assigned anywhere in the module.
    """

    names = set()

    for node in ast.walk(tree):

        if isinstance(node, ast.Name):

            if isinstance(node.ctx, ast.Store):
                names.add(node.id)

        elif isinstance(node, ast.arg):

            names.add(node.arg)

    return names


def uppercase_assignments(tree):
    """
    Return uppercase module-level assignments.

    Each result is:

        (name, line_number, AST_node)

    Only assignments directly in the module body are considered.
    Constants created inside functions are not treated as module
    configuration.
    """

    results = []

    for node in tree.body:

        targets = []

        if isinstance(node, ast.Assign):
            targets = node.targets

        elif isinstance(node, ast.AnnAssign):
            targets = [node.target]

        for target in targets:

            if not isinstance(target, ast.Name):
                continue

            name = target.id

            if re.fullmatch(
                r"[A-Z][A-Z0-9_]*",
                name,
            ):
                results.append(
                    (
                        name,
                        target.lineno,
                        node,
                    )
                )

    return results


# ============================================================
# Constant classification helpers
# ============================================================

def looks_like_implementation_constant(name, node):
    """
    Return True if an uppercase constant looks like an
    implementation detail rather than project configuration.

    This classification is intentionally conservative.

    Examples:

        IMPORT_RE
        LECTURE_START_RE
        REQUIRED_FIELDS
        COMMANDS

    are implementation constants.

    Examples such as:

        OG_WIDTH
        OG_HEIGHT
        DIST_DIR
        SITE_URL

    are not classified as implementation constants here.
    """

    # --------------------------------------------------------
    # Explicit implementation constants
    # --------------------------------------------------------

    if name in IMPLEMENTATION_CONSTANT_NAMES:
        return True

    # --------------------------------------------------------
    # Regex / pattern constants
    # --------------------------------------------------------

    for pattern in IMPLEMENTATION_NAME_PATTERNS:

        if re.fullmatch(pattern, name):
            return True

    # --------------------------------------------------------
    # AST-based implementation detection
    # --------------------------------------------------------
    #
    # Regular expressions often contain calls such as:
    #
    #     re.compile(...)
    #
    # Detect these even if the constant name is unusual.
    # --------------------------------------------------------

    if isinstance(node, ast.Assign):

        value = node.value

        if isinstance(value, ast.Call):

            function = value.func

            if (
                isinstance(function, ast.Attribute)
                and isinstance(function.value, ast.Name)
                and function.value.id == "re"
                and function.attr == "compile"
            ):
                return True

    return False


def classify_constant(name, node):
    """
    Classify an uppercase constant.

    Returns either:

        "configuration"

    or:

        "implementation"
    """

    if looks_like_implementation_constant(name, node):
        return "implementation"

    return "configuration"


# ============================================================
# Main audit
# ============================================================

def main():

    if not CONFIG_FILE.exists():

        raise FileNotFoundError(
            f"Configuration file not found: {CONFIG_FILE}"
        )

    DIAGNOSTICS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    python_files = sorted(
        SCRIPTS_DIR.rglob("*.py")
    )


    # ========================================================
    # Report sections
    # ========================================================

    findings = {
        "configuration_constants": [],
        "implementation_constants": [],
        "local_paths": [],
        "root_paths": [],
        "project_directories": [],
        "project_strings": [],
        "config_numbers": [],
        "config_imports": [],
        "redefinitions": [],
    }


    config_constants = set()


    # ========================================================
    # Parse config.py
    # ========================================================

    config_source = CONFIG_FILE.read_text(
        encoding="utf-8"
    )

    config_tree = ast.parse(
        config_source,
        filename=str(CONFIG_FILE),
    )

    for name, lineno, node in uppercase_assignments(
        config_tree
    ):
        config_constants.add(name)


    # ========================================================
    # Audit every Python script
    # ========================================================

    for path in python_files:

        source = path.read_text(
            encoding="utf-8"
        )

        try:

            tree = ast.parse(
                source,
                filename=str(path),
            )

        except SyntaxError as exc:

            print(
                f"⚠️  Could not parse {relative(path)}: "
                f"{exc}"
            )

            continue


        # ====================================================
        # Skip config.py for duplicate-definition checks
        # ====================================================

        if path not in CONFIG_MODULES and path != AUDIT_FILE:

            # ------------------------------------------------
            # 1. Uppercase constants
            # ------------------------------------------------

            for name, lineno, node in uppercase_assignments(
                tree
            ):

                classification = classify_constant(
                    name,
                    node,
                )

                if classification == "configuration":

                    add_finding(
                        findings,
                        "configuration_constants",
                        path,
                        lineno,
                        name,
                    )

                else:

                    add_finding(
                        findings,
                        "implementation_constants",
                        path,
                        lineno,
                        name,
                    )


            # ------------------------------------------------
            # 2. Imported config names
            # ------------------------------------------------

            imported = imported_config_names(tree)

            for local_name, config_name in imported.items():

                findings["config_imports"].append(
                    (
                        str(relative(path)),
                        0,
                        f"{local_name} ← config.{config_name}",
                    )
                )


            # ------------------------------------------------
            # 3. Local redefinitions
            # ------------------------------------------------

            assignments = assigned_names(tree)

            for local_name, config_name in imported.items():

                if local_name not in assignments:
                    continue

                # Ignore the import itself.
                #
                # We only report actual Store nodes that occur
                # as assignments elsewhere in the module.
                # ------------------------------------------------

                for node in ast.walk(tree):

                    if not isinstance(node, ast.Name):
                        continue

                    if node.id != local_name:
                        continue

                    if not isinstance(node.ctx, ast.Store):
                        continue

                    # The import itself is an ImportFrom node,
                    # not an ast.Name Store node, so every match
                    # here represents an actual assignment.
                    # ------------------------------------------------

                    findings["redefinitions"].append(
                        (
                            str(relative(path)),
                            node.lineno,
                            (
                                f"{local_name} "
                                f"(imported from config "
                                f"as {config_name})"
                            ),
                        )
                    )


        # ====================================================
        # AST/path checks
        # ====================================================

        for node in ast.walk(tree):

            # ------------------------------------------------
            # 4. Path(...)
            # ------------------------------------------------
            #
            # Path(source) is not necessarily configuration.
            # It is still useful to report because it can reveal
            # scripts constructing project paths locally.
            # ------------------------------------------------

            if (
                isinstance(node, ast.Call)
                and isinstance(node.func, ast.Name)
                and node.func.id == "Path"
            ):

                add_finding(
                    findings,
                    "local_paths",
                    path,
                    node.lineno,
                    source_line(source, node.lineno),
                )


            # ------------------------------------------------
            # 5. ROOT / ...
            # ------------------------------------------------
            #
            # Only report actual division expressions involving
            # ROOT. This is intended to find locally reconstructed
            # project paths such as:
            #
            #     ROOT / "generated"
            #
            # ------------------------------------------------

            if (
                isinstance(node, ast.BinOp)
                and isinstance(node.op, ast.Div)
            ):

                text = source_line(
                    source,
                    node.lineno,
                )

                if "ROOT" in text:

                    add_finding(
                        findings,
                        "root_paths",
                        path,
                        node.lineno,
                        text,
                    )


            # ------------------------------------------------
            # 6. Numeric constants
            # ------------------------------------------------

            if isinstance(node, ast.Constant):

                if (
                    isinstance(node.value, int)
                    and node.value in CONFIG_LIKE_NUMBERS
                ):

                    add_finding(
                        findings,
                        "config_numbers",
                        path,
                        node.lineno,
                        str(node.value),
                    )


    # ========================================================
    # Text-based checks
    # ========================================================

    for path in python_files:

        if path == CONFIG_FILE:
            continue

        source = path.read_text(
            encoding="utf-8"
        )

        lines = source.splitlines()

        for lineno, line in enumerate(
            lines,
            start=1,
        ):

            # ------------------------------------------------
            # 7. Project directory names
            # ------------------------------------------------

            for directory in PROJECT_DIRECTORIES:

                pattern = (
                    rf'["\']{re.escape(directory)}'
                    rf'(?:/|["\'])'
                )

                if re.search(
                    pattern,
                    line,
                ):

                    add_finding(
                        findings,
                        "project_directories",
                        path,
                        lineno,
                        line.strip(),
                    )

                    break


            # ------------------------------------------------
            # 8. Project-specific strings
            # ------------------------------------------------

            for value in PROJECT_STRINGS:

                if value in line:

                    add_finding(
                        findings,
                        "project_strings",
                        path,
                        lineno,
                        line.strip(),
                    )

                    break


    # ========================================================
    # Remove duplicate findings
    # ========================================================

    for category in findings:

        findings[category] = sorted(
            set(findings[category]),
            key=lambda item: (
                item[0],
                item[1],
                item[2],
            ),
        )


    # ========================================================
    # Build report
    # ========================================================

    lines = []

    lines.append("=" * 70)
    lines.append("Configuration Audit Report")
    lines.append("=" * 70)
    lines.append("")

    lines.append(
        f"Project root : {ROOT}"
    )

    lines.append(
        f"Config file  : {relative(CONFIG_FILE)}"
    )

    lines.append(
        f"Python files : {len(python_files)}"
    )

    lines.append("")


    # ========================================================
    # Central configuration
    # ========================================================

    lines.append("CENTRAL CONFIGURATION")
    lines.append("-" * 70)

    for name in sorted(config_constants):

        lines.append(
            f"  {name}"
        )

    lines.append(
        f"\nTotal: {len(config_constants)}"
    )

    lines.append("")


    # ========================================================
    # Configuration constants outside config.py
    # ========================================================

    lines.append(
        "1. CONFIGURATION-LIKE CONSTANTS DEFINED "
        "OUTSIDE CONFIGURATION MODULES"
    )

    lines.append("-" * 70)

    if findings["configuration_constants"]:

        for path, lineno, text in findings[
            "configuration_constants"
        ]:

            lines.append(
                f"  {path}:{lineno}: {text}"
            )

    else:

        lines.append(
            "  ✓ None found."
        )

    lines.append("")


    # ========================================================
    # Implementation constants
    # ========================================================

    lines.append(
        "2. IMPLEMENTATION CONSTANTS DEFINED "
        "OUTSIDE CONFIGURATION MODULES"
    )

    lines.append("-" * 70)

    if findings["implementation_constants"]:

        for path, lineno, text in findings[
            "implementation_constants"
        ]:

            lines.append(
                f"  {path}:{lineno}: {text}"
            )

    else:

        lines.append(
            "  ✓ None found."
        )

    lines.append("")


    # ========================================================
    # Local paths
    # ========================================================

    lines.append(
        "3. LOCAL PATH CONSTRUCTION CANDIDATES"
    )

    lines.append("-" * 70)

    lines.append(
        "  NOTE: Path(...) calls are reported as audit candidates."
    )

    lines.append(
        "  They are not necessarily configuration and often represent"
    )

    lines.append(
        "  normal runtime conversion of strings to Path objects."
    )

    lines.append("")

    if findings["local_paths"]:

        for path, lineno, text in findings[
            "local_paths"
        ]:

            lines.append(
                f"  {path}:{lineno}: {text}"
            )

    else:

        lines.append(
            "  ✓ None found."
        )

    lines.append("")


    # ========================================================
    # ROOT path constructions
    # ========================================================

    lines.append(
        "4. PROJECT PATH CONSTRUCTIONS OUTSIDE CONFIGURATION MODULES"
    )

    lines.append("-" * 70)

    if findings["root_paths"]:

        for path, lineno, text in findings[
            "root_paths"
        ]:

            lines.append(
                f"  {path}:{lineno}: {text}"
            )

    else:

        lines.append(
            "  ✓ None found."
        )

    lines.append("")


    # ========================================================
    # Project directories
    # ========================================================

    lines.append(
        "5. HARDCODED PROJECT DIRECTORY NAMES"
    )

    lines.append("-" * 70)

    if findings["project_directories"]:

        for path, lineno, text in findings[
            "project_directories"
        ]:

            lines.append(
                f"  {path}:{lineno}: {text}"
            )

    else:

        lines.append(
            "  ✓ None found."
        )

    lines.append("")


    # ========================================================
    # Project strings
    # ========================================================

    lines.append(
        "6. HARDCODED PROJECT / WEBSITE STRINGS"
    )

    lines.append("-" * 70)

    if findings["project_strings"]:

        for path, lineno, text in findings[
            "project_strings"
        ]:

            lines.append(
                f"  {path}:{lineno}: {text}"
            )

    else:

        lines.append(
            "  ✓ None found."
        )

    lines.append("")


    # ========================================================
    # Numeric configuration
    # ========================================================

    lines.append(
        "7. CONFIGURATION-LIKE NUMERIC VALUES"
    )

    lines.append("-" * 70)

    if findings["config_numbers"]:

        for path, lineno, text in findings[
            "config_numbers"
        ]:

            lines.append(
                f"  {path}:{lineno}: {text}"
            )

    else:

        lines.append(
            "  ✓ None found."
        )

    lines.append("")


    # ========================================================
    # Config imports
    # ========================================================

    lines.append(
        "8. IMPORTS FROM scripts.config"
    )

    lines.append("-" * 70)

    if findings["config_imports"]:

        for path, lineno, text in findings[
            "config_imports"
        ]:

            lines.append(
                f"  {path}: {text}"
            )

    else:

        lines.append(
            "  ⚠️  No config imports found."
        )

    lines.append("")


    # ========================================================
    # Redefinitions
    # ========================================================

    lines.append(
        "9. NAMES IMPORTED FROM config.py AND REDEFINED"
    )

    lines.append("-" * 70)

    if findings["redefinitions"]:

        for path, lineno, text in findings[
            "redefinitions"
        ]:

            lines.append(
                f"  {path}:{lineno}: {text}"
            )

    else:

        lines.append(
            "  ✓ None found."
        )

    lines.append("")


    # ========================================================
    # Summary
    # ========================================================

    lines.append("SUMMARY")
    lines.append("-" * 70)

    lines.append(
        f"Config constants              : "
        f"{len(config_constants)}"
    )

    lines.append(
        f"Configuration constants "
        f"outside configuration modules : "
        f"{len(findings['configuration_constants'])}"
    )

    lines.append(
        f"Implementation constants      : "
        f"{len(findings['implementation_constants'])}"
    )

    lines.append(
        f"Local Path(...) constructions  : "
        f"{len(findings['local_paths'])}"
    )

    lines.append(
        f"ROOT / ... constructions       : "
        f"{len(findings['root_paths'])}"
    )

    lines.append(
        f"Hardcoded directories          : "
        f"{len(findings['project_directories'])}"
    )

    lines.append(
        f"Hardcoded project strings      : "
        f"{len(findings['project_strings'])}"
    )

    lines.append(
        f"Configuration-like numbers     : "
        f"{len(findings['config_numbers'])}"
    )

    lines.append(
        f"Config imports                 : "
        f"{len(findings['config_imports'])}"
    )

    lines.append(
        f"Config-name redefinitions      : "
        f"{len(findings['redefinitions'])}"
    )

    lines.append("")

    lines.append(
        "NOTE: Findings are candidates for review, not "
        "automatic errors."
    )

    lines.append(
        "Configuration constants should normally be centralized "
        "in config.py."
    )

    lines.append(
        "Implementation constants may legitimately remain "
        "inside the scripts that use them."
    )


    # ========================================================
    # Write report
    # ========================================================

    report = "\n".join(lines) + "\n"

    CONFIG_REPORT.write_text(
        report,
        encoding="utf-8",
    )


    # ========================================================
    # Print report
    # ========================================================

    print(report)

    print(
        f"📄 Report written to "
        f"{relative(CONFIG_REPORT)}"
    )


# ============================================================
# Entry point
# ============================================================

if __name__ == "__main__":
    main()