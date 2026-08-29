#!/usr/bin/env bash

set -euo pipefail

export TYPST_FEATURES=html

# ============================================================
# Output colors / print helpers
# ============================================================

if [[ -t 1 ]]; then
    C_RESET=$'\033[0m'
    C_GREEN=$'\033[32m'
    C_YELLOW=$'\033[33m'
    C_RED=$'\033[31m'
    C_BLUE=$'\033[34m'
    C_CYAN=$'\033[36m'
    C_BOLD=$'\033[1m'
else
    C_RESET=""
    C_GREEN=""
    C_YELLOW=""
    C_RED=""
    C_BLUE=""
    C_CYAN=""
    C_BOLD=""
fi


print_step() {
    printf '\n%s%s%s\n' \
        "$C_BOLD$C_BLUE" "$1" "$C_RESET"
}


print_ok() {
    printf '    %s✅ %s %s\n' \
        "$C_GREEN" "$C_RESET" "$1"
}


print_skip() {
    printf '    %s⏭️  %s %s\n' \
        "$C_YELLOW" "$C_RESET" "$1"
}


print_warn() {
    printf '    %s⚠️  %s %s\n' \
        "$C_YELLOW" "$C_RESET" "$1"
}


print_fail() {
    printf '    %s❌ %s %s\n' \
        "$C_RED" "$C_RESET" "$1"
}


print_info() {
    printf '    %sℹ️  %s %s\n' \
        "$C_CYAN" "$C_RESET" "$1"
}


# ============================================================
# Effective Open Graph setting
# ============================================================
#
# Let scripts/config.py determine whether OG generation is
# enabled. This respects:
#
#   TYPST_OG_BUILD
#   TYPST_OG_GITBUILD
#
# and therefore keeps build.sh and Python configuration
# synchronized.
# ============================================================

TYPST_OG=$(python3 -c \
    'from scripts.config import TYPST_OG; print(str(TYPST_OG).lower())')

export TYPST_OG

printf '%sTYPST_OG=%s%s\n' \
    "$C_CYAN" "$TYPST_OG" "$C_RESET"


# ============================================================
# Build target
#
# Usage:
#
#     ./build.sh
#     ./build.sh <target>
#
# The default target is "all".
#
# Common targets:
#
#     all
#     config
#     metadata
#     refmap
#     fix-refs
#     fix-equations
#     og-generate
#     og-build
#     og-publish
#     og-refresh
#     metadata-check
#     generated
#     imports
#     og-check
#     links
#     prepare-dist
#     prepare-diagnostics
#     html
#     sitemap
#     robots
#     pdf
#     categories
#     book
#     pages-pdf
#     allpdf
#     report
# ============================================================

TARGET="${1:-all}"


# ============================================================
# Help
# ============================================================

print_help() {
    cat <<'EOF'

Build the Typst mathematics lecture website and PDFs.

Usage:
    ./build.sh [TARGET]

If TARGET is omitted, "all" is used.


Targets:
    ┌──────────────────────┬─────────────────────────────────────┬──────────────────────────────────────────────┐
    │ Target               │ Example                             │ Description                                  │
    ├──────────────────────┼─────────────────────────────────────┼──────────────────────────────────────────────┤
    │ all                  │ ./build.sh                          │ Complete website + committed OG PNGs +       │
    │                      │                                     │ OG check + all PDFs + link check + report.   │
    │                      │                                     │ Does not generate OG .asy or PNG files.      │
    │                      │                                     │ Use og-refresh to regenerate OG assets.      │
    ├──────────────────────┼─────────────────────────────────────┼──────────────────────────────────────────────┤
    │ config               │ ./build.sh config                   │ Audit centralized configuration              │
    │ metadata             │ ./build.sh metadata                 │ Generate metadata                            │
    │ refmap               │ ./build.sh refmap                   │ Build site-wide reference map from HTML      │
    │ fix-refs             │ ./build.sh fix-refs                 │ Fix/canonicalize internal HTML references    │
    │ fix-equations        │ ./build.sh fix-equations            │ Fix/canonicalize internal HTML equations     │
    ├──────────────────────┼─────────────────────────────────────┼──────────────────────────────────────────────┤
    │ og-generate          │ ./build.sh og-generate              │ Generate Open Graph .asy sources             │
    │ og-build             │ ./build.sh og-build                 │ Build Open Graph PNG images                  │
    │ og-publish           │ ./build.sh og-publish               │ Publish OG PNG images into dist/assets/og/   │
    │ og-refresh           │ ./build.sh og-refresh               │ Force generate, build, and publish OG        │
    ├──────────────────────┼─────────────────────────────────────┼──────────────────────────────────────────────┤
    │ metadata-check       │ ./build.sh metadata-check           │ Validate source metadata                     │
    │ generated            │ ./build.sh generated                │ Validate generated files                     │
    │ imports              │ ./build.sh imports                  │ Validate Typst imports                       │
    │ links                │ ./build.sh links                    │ Check generated website links                │
    │ og-check             │ ./build.sh og-check                 │ Validate Open Graph images in HTML           │
    ├──────────────────────┼─────────────────────────────────────┼──────────────────────────────────────────────┤
    │ prepare-dist         │ ./build.sh prepare-dist             │ Prepare dist/ and copy static assets         │
    │ prepare-diagnostics  │ ./build.sh prepare-diagnostics      │ Prepare diagnostics/                         │
    ├──────────────────────┼─────────────────────────────────────┼──────────────────────────────────────────────┤
    │ html                 │ ./build.sh html                     │ Build HTML pages                             │
    │ sitemap              │ ./build.sh sitemap                  │ Generate sitemap.xml                         │
    │ robots               │ ./build.sh robots                   │ Generate robots.txt                          │
    ├──────────────────────┼─────────────────────────────────────┼──────────────────────────────────────────────┤
    │ pdf                  │ ./build.sh pdf                      │ Build individual page PDFs                   │
    │ categories           │ ./build.sh categories               │ Build category PDFs                          │
    │ book                 │ ./build.sh book                     │ Build complete course/book PDF               │
    │ pages-pdf            │ ./build.sh pages-pdf                │ Build combined pages PDF                     │
    │ allpdf               │ ./build.sh allpdf                   │ Build all PDF outputs                        │
    ├──────────────────────┼─────────────────────────────────────┼──────────────────────────────────────────────┤
    │ report               │ ./build.sh report                   │ Generate diagnostics/build report            │
    └──────────────────────┴─────────────────────────────────────┴──────────────────────────────────────────────┘

Open Graph configuration:

    Effective TYPST_OG:

        ┌───────────────────┬──────────────────────────┬──────────────────────────────┐
        │ Environment       │ Setting                  │ Effective TYPST_OG           │
        ├───────────────────┼──────────────────────────┼──────────────────────────────┤
        │ Local             │ no override              │ config: TYPST_OG_BUILD       │
        │ Local             │ TYPST_OG_BUILD=true      │ true                         │
        │ Local             │ TYPST_OG_BUILD=false     │ false                        │
        │ GitHub Actions    │ any local override       │ config: TYPST_OG_GITBUILD    │
        └───────────────────┴──────────────────────────┴──────────────────────────────┘

    Usage:

        ┌────────────────────────────────────┬──────────────────────────────────────────────┐
        │ Command                            │ Effect                                       │
        ├────────────────────────────────────┼──────────────────────────────────────────────┤
        │ ./build.sh                         │ Normal local build                           │
        │ TYPST_OG_BUILD=true ./build.sh     │ Enable OG generation locally                 │
        │ TYPST_OG_BUILD=false ./build.sh    │ Disable OG generation locally                │
        │ ./build.sh og-generate             │ Generate OG .asy sources                     │
        │ ./build.sh og-build                │ Build OG .asy sources into PNGs              │
        │ ./build.sh og-publish              │ Publish generated OG PNGs                    │
        │ ./build.sh og-refresh              │ Force generate + build + publish OG images   │
        └────────────────────────────────────┴──────────────────────────────────────────────┘

    GitHub:

        ┌───────────────────────────┬──────────────────────────────────────────────┐
        │ TYPST_OG_GITBUILD         │ GitHub deployment                            │
        ├───────────────────────────┼──────────────────────────────────────────────┤
        │ False                     │ Reuse committed OG PNGs                      │
        │ True                      │ Generate OG PNGs during deployment           │
        └───────────────────────────┴──────────────────────────────────────────────┘

    When GitHub OG generation is enabled, the workflow installs:
        Asymptote + TeX Live + ImageMagick

Options:

    -h, --help
        Show this help message.

EOF
}


# ============================================================
# Handle command-line help
# ============================================================

case "$TARGET" in
    -h|--help)
        print_help
        exit 0
        ;;
esac


# ============================================================
# Validate command-line target
# ============================================================

case "$TARGET" in

    # --------------------------------------------------------
    # Complete build
    # --------------------------------------------------------

    all)
        ;;

    # --------------------------------------------------------
    # Configuration and metadata generation
    # --------------------------------------------------------

    config|metadata)
        ;;

    # --------------------------------------------------------
    # Open Graph generation
    #
    # These targets are valid regardless of TYPST_OG.
    #
    # The build logic decides whether they actually run:
    #
    #     TYPST_OG=true   → generate/build/publish OG images
    #     TYPST_OG=false  → skip generated OG operations
    #
    # og-refresh is different:
    #
    #     og-refresh      → explicitly forces a local OG refresh
    #
    # og-check remains independent and can always be run.
    # --------------------------------------------------------

    og-generate|og-build|og-publish|og-refresh)
        ;;

    # --------------------------------------------------------
    # Validation
    # --------------------------------------------------------

    metadata-check|generated|imports|links|og-check)
        ;;

    # --------------------------------------------------------
    # Build preparation
    # --------------------------------------------------------

    prepare-dist|prepare-diagnostics)
        ;;

    # --------------------------------------------------------
    # Website output
    # --------------------------------------------------------

    html|refmap|fix-refs|fix-equations|sitemap|robots)
        ;;

    # --------------------------------------------------------
    # PDF output
    # --------------------------------------------------------

    pdf|categories|book|pages-pdf|allpdf)
        ;;

    # --------------------------------------------------------
    # Diagnostics
    # --------------------------------------------------------

    report)
        ;;

    # --------------------------------------------------------
    # Invalid target
    # --------------------------------------------------------

    *)

        print_fail "Unknown build target: $TARGET"
        echo
        echo "Run './build.sh --help' for usage information."
        exit 1
        ;;

esac

# ============================================================
# Build timing
#
# Record the time at which the build starts.
# The final summary will report the total build time.
# ============================================================

BUILD_START=$(date +%s)


# ============================================================
# Stage timings
#
# Each major build stage stores its elapsed time so that the
# final summary can show where the build time was spent.
# ============================================================


# ------------------------------------------------------------
# Configuration and generation
# ------------------------------------------------------------

TIME_CONFIG="0"
TIME_METADATA="0"
TIME_REFMAP="0"
TIME_FIX_REFS="0"
TIME_FIX_EQUATIONS="0"
TIME_OG_GENERATE="0"
TIME_OG_BUILD="0"
TIME_OG_PUBLISH="0"


# ------------------------------------------------------------
# Validation
# ------------------------------------------------------------

TIME_METADATA_CHECK="0"
TIME_GENERATED_CHECK="0"
TIME_IMPORT_CHECK="0"
TIME_LINKS="0"
TIME_OG_CHECK="0"


# ------------------------------------------------------------
# Build preparation
# ------------------------------------------------------------

TIME_PREPARE_DIST="0"
TIME_PREPARE_DIAGNOSTICS="0"


# ------------------------------------------------------------
# Website output
# ------------------------------------------------------------

TIME_HTML="0"
TIME_SITEMAP="0"
TIME_ROBOTS="0"


# ------------------------------------------------------------
# PDF output
# ------------------------------------------------------------

TIME_PDF="0"
TIME_CATEGORIES="0"
TIME_BOOK="0"
TIME_PAGES="0"


# ------------------------------------------------------------
# Diagnostics
# ------------------------------------------------------------

TIME_REPORT="0"


# ============================================================
# Helpers
# ============================================================

die() {
    print_fail "Build failed: $1"
    exit 1
}


# ============================================================
# Timing helpers
#
# macOS does not support date +%s.%N reliably.
# Use whole-second timestamps for portable shell timing.
# ============================================================

stage_start() {
    STAGE_START=$(date +%s)
}


stage_end() {
    local variable="$1"
    local elapsed

    elapsed=$(( $(date +%s) - STAGE_START ))

    printf -v "$variable" '%s' "$elapsed"
}


# ============================================================
# Cleanup
#
# Remove Python bytecode generated during the build.
# Preserve the original exit status of the build.
# ============================================================

cleanup() {

    local status=$?

    if find scripts \
        -type d \
        -name "__pycache__" \
        -print -quit |
        grep -q .
    then
        print_step "🧹 Cleaning Python bytecode..."

        find scripts \
            -type d \
            -name "__pycache__" \
            -prune \
            -exec rm -rf {} +

        print_ok "Python bytecode removed."
    fi

    return "$status"
}


trap cleanup EXIT

# ============================================================
# 1. Generation
# ============================================================

# ============================================================
# 1a. Generate metadata
# ============================================================

generate_metadata() {

    print_step "📋 Generating metadata..."

    stage_start

    if ! python3 scripts/run.py metadata; then
        die "metadata generation failed."
    fi

    stage_end TIME_METADATA

    print_ok "Metadata generated."
}


# ============================================================
# 1b. Generate Open Graph Asymptote sources
# ============================================================

generate_og() {

    print_step "🖼️  Generating Open Graph sources..."

    if [[ "$TYPST_OG" != "true" ]]; then
        print_skip "Open Graph generation disabled (TYPST_OG=false)"
        return 0
    fi

    stage_start

    if ! python3 scripts/run.py og-generate; then
        die "Open Graph source generation failed."
    fi

    stage_end TIME_OG_GENERATE

    print_ok "Open Graph sources generated."
}


# ============================================================
# 1c. Build Open Graph PNG images
# ============================================================

build_og() {

    print_step "🖼️  Building Open Graph PNGs..."

    if [[ "$TYPST_OG" != "true" ]]; then
        print_skip "Open Graph build disabled (TYPST_OG=false)"
        return 0
    fi

    stage_start

    if ! python3 scripts/run.py og-build; then
        die "Open Graph image build failed."
    fi

    stage_end TIME_OG_BUILD

    print_ok "Open Graph PNGs built."
}


# ============================================================
# 1d. Publish Open Graph PNG images
# ============================================================
#
# Copy generated OG PNG images from:
#
#     generated/og/
#
# to:
#
#     dist/assets/og/
#
# This must run AFTER prepare_dist(), because prepare_dist()
# removes and recreates dist/.
#
# TYPST_OG=false:
#
#     Do not publish generated OG images.
#     prepare_dist() restores the committed OG images instead.
#
# TYPST_OG=true:
#
#     Publish the freshly generated OG PNGs.
# ============================================================

publish_og() {

    print_step "📦 Publishing Open Graph PNGs..."

    if [[ "$TYPST_OG" != "true" ]]; then
        print_skip "Open Graph publishing disabled (TYPST_OG=false)"
        return 0
    fi

    stage_start

    if ! python3 scripts/run.py og-publish; then
        die "Open Graph image publishing failed."
    fi

    stage_end TIME_OG_PUBLISH

    print_ok "Open Graph PNGs published."
}

# ============================================================
# 1e. Refresh Open Graph images
#
# Force a complete local OG refresh regardless of TYPST_OG.
#
# This target:
#
#   1. Removes the existing generated OG working directory
#   2. Generates all OG Asymptote sources
#   3. Builds all OG PNG images
#   4. Publishes the PNG images into dist/assets/og/
#
# It does NOT rebuild the website.
#
# Unlike the normal build pipeline, this command intentionally
# ignores TYPST_OG so that:
#
#     ./build.sh og-refresh
#
# always performs the requested refresh.
# ============================================================

og_refresh() {

    print_step "🔄 Refreshing Open Graph images..."

    # --------------------------------------------------------
    # Force a clean OG generation
    # --------------------------------------------------------
    #
    # This makes "refresh" genuinely destructive for the
    # generated OG working tree. Existing generated .asy/.png
    # files cannot cause generation/build steps to be skipped.
    # --------------------------------------------------------

    if [[ -d "generated/og" ]]; then

        print_info "Removing existing generated OG files..."

        rm -rf "generated/og"

    fi

    # --------------------------------------------------------
    # Generate OG sources
    # --------------------------------------------------------

    stage_start

    if ! python3 scripts/run.py og-generate; then
        die "Open Graph source generation failed."
    fi

    stage_end TIME_OG_GENERATE

    print_ok "Open Graph sources generated."

    # --------------------------------------------------------
    # Build OG PNGs
    # --------------------------------------------------------

    stage_start

    if ! python3 scripts/run.py og-build; then
        die "Open Graph image build failed."
    fi

    stage_end TIME_OG_BUILD

    print_ok "Open Graph PNGs built."

    # --------------------------------------------------------
    # Publish OG PNGs
    # --------------------------------------------------------

    stage_start

    if ! python3 scripts/run.py og-publish; then
        die "Open Graph image publishing failed."
    fi

    stage_end TIME_OG_PUBLISH

    print_ok "Open Graph PNGs published."

    echo
    print_ok "Open Graph images refreshed."
}

# ============================================================
# 2. Validation
# ============================================================
#
# Validation operates on the generated project state.
#
# Reference-map generation and HTML reference fixing are NOT
# validation steps. They are generation/transformation steps
# and therefore run before this section.
#
# The normal order is:
#
#     metadata
#     refmap
#     html
#     fix-html-refs
#     ...
#     validation
#
# ============================================================


# ============================================================
# 2a. Check configuration
#
# Audit configuration usage across the Python codebase.
#
# The configuration audit is informational rather than a strict
# validation check. It reports:
#
#   - configuration constants outside config.py
#   - implementation constants
#   - Path(...) constructions
#   - hardcoded project directories
#   - hardcoded project/website strings
#   - configuration-like numeric values
#   - imports from scripts.config
#   - redefinitions of config names
#
# Findings are candidates for review and are not automatically
# considered build errors.
#
# The detailed report is written to:
#
#     diagnostics/config_report.txt
#
# Therefore, a non-zero exit status from the audit does not
# abort the build.
# ============================================================

validate_config() {

    print_step "⚙️  Checking configuration..."

    stage_start

    if ! python3 scripts/run.py config; then
        print_warn "Configuration audit reported findings."
        print_info "See diagnostics/config_report.txt for details."
    else
        print_ok "Configuration audit passed."
    fi

    stage_end TIME_CONFIG

    print_ok "Configuration audit completed."
}


# ============================================================
# 2b. Check source metadata
# ============================================================

validate_metadata() {

    print_step "📋 Validating source metadata..."

    stage_start

    if ! python3 scripts/run.py metadata-check; then
        die "metadata validation failed."
    fi

    stage_end TIME_METADATA_CHECK

    print_ok "Source metadata validated."
}


# ============================================================
# 2c. Check generated files
# ============================================================

validate_generated() {

    print_step "🔍 Validating generated files..."

    stage_start

    if ! python3 scripts/run.py generated; then
        die "generated consistency check failed."
    fi

    stage_end TIME_GENERATED_CHECK

    print_ok "Generated files validated."
}


# ============================================================
# 2d. Check Typst imports
#
# Verify that all imported Typst files exist and that there
# are no circular import dependencies.
#
# The detailed dependency graph is written to:
#
#     diagnostics/imports.dot
#
# ============================================================

validate_imports() {

    print_step "🔍 Validating Typst imports..."

    stage_start

    if ! python3 scripts/run.py imports; then
        die "Typst import validation failed."
    fi

    stage_end TIME_IMPORT_CHECK

    print_ok "Typst imports validated."
}


# ============================================================
# 2e. Check Open Graph images
#
# Validate the final Open Graph output in dist/.
#
# This check is intentionally independent of how the OG images
# were produced:
#
#     TYPST_OG=true
#         generated/og/*.png → dist/assets/og/
#
#     TYPST_OG=false
#         committed OG images → dist/assets/og/
#
# Therefore this validation checks the deployed output rather
# than the OG generation mechanism.
#
# It verifies that:
#
#   - generated HTML pages contain expected OG metadata
#   - og:image references are valid
#   - referenced OG images are under dist/assets/og/
#   - referenced OG image files actually exist
#
# This must run after HTML generation and after prepare_dist().
# ============================================================

validate_og() {

    print_step "🖼️  Checking Open Graph images..."

    stage_start

    if ! python3 scripts/run.py og-check; then
        die "Open Graph image check failed."
    fi

    stage_end TIME_OG_CHECK

    print_ok "Open Graph images validated."
}


# ============================================================
# 2f. Check links
#
# Validate links in the final generated website.
#
# This should normally run after:
#
#     - HTML generation
#     - sitemap/robots generation
#     - PDF generation
#
# so that all referenced output files exist.
# ============================================================

validate_links() {

    print_step "🔗 Checking links..."

    stage_start

    if ! python3 scripts/run.py links; then
        die "broken links detected."
    fi

    stage_end TIME_LINKS

    print_ok "Links validated."
}

# ============================================================
# 3. Build preparation
# ============================================================


# ============================================================
# 3a. Prepare dist
#
# Delegate dist preparation to the Python build layer.
#
# prepare_dist() is responsible for:
#
#   - removing the previous dist/
#   - recreating the required dist/ directory structure
#   - copying static assets
#   - copying project-supplied PNG images
#   - when TYPST_OG=true:
#         copying generated/og/*.png → dist/assets/og/
#   - when TYPST_OG=false:
#         preserving/restoring committed OG PNGs
#
# IMPORTANT:
#
# This is the OG publishing mechanism used by the normal
# full build.
#
# Do NOT call:
#
#     python3 scripts/run.py og-publish
#
# here.
#
# og-publish is an explicit operation used by:
#
#     ./build.sh og-refresh
#
# ============================================================

prepare_dist() {

    print_step "📁 Preparing dist..."

    stage_start

    if ! python3 scripts/run.py prepare-dist; then
        die "dist preparation failed."
    fi

    stage_end TIME_PREPARE_DIST

    print_ok "dist prepared."
}


# ============================================================
# 3b. Prepare diagnostics
# ============================================================

prepare_diagnostics() {

    print_step "🧹 Preparing diagnostics..."

    stage_start

    if ! python3 scripts/run.py prepare-diagnostics; then
        die "diagnostics preparation failed."
    fi

    stage_end TIME_PREPARE_DIAGNOSTICS

    print_ok "Diagnostics directory prepared."
}


# ============================================================
# 4. Website output
# ============================================================


# ============================================================
# 4a. Build HTML pages
# ============================================================

build_html() {

    print_step "🌐 Building course pages..."

    stage_start

    if ! python3 scripts/run.py html; then
        die "HTML build failed."
    fi

    stage_end TIME_HTML

    print_ok "Course HTML pages built."
}


# ============================================================
# 4b. Build reference map
# ============================================================

build_refmap() {

    print_step "🔖 Building reference map..."

    stage_start

    if ! python3 scripts/run.py refmap; then
        die "reference map generation failed."
    fi

    stage_end TIME_REFMAP

    print_ok "Reference map built."
}


# ============================================================
# 4c. Fix HTML references
# ============================================================

fix_html_refs() {

    print_step "🔗 Fixing HTML references..."

    stage_start

    if ! python3 scripts/run.py fix-refs; then
        die "HTML reference fixing failed."
    fi

    stage_end TIME_FIX_REFS

    print_ok "HTML references fixed."
}


# ============================================================
# 4d. Fix HTML equations
# ============================================================

fix_html_equations() {

    print_step "🔢 Fixing HTML equation numbers..."

    stage_start

    if ! python3 scripts/run.py fix-equations; then
        die "HTML equation fixing failed."
    fi

    stage_end TIME_FIX_EQUATIONS

    print_ok "HTML equation numbers fixed."
}


# ============================================================
# 4e. Generate sitemap
# ============================================================

build_sitemap() {

    print_step "🗺️  Generating sitemap..."

    stage_start

    if ! python3 scripts/run.py sitemap; then
        die "sitemap generation failed."
    fi

    stage_end TIME_SITEMAP

    print_ok "Sitemap generated."
}


# ============================================================
# 4f. Generate robots.txt
# ============================================================

build_robots() {

    print_step "🤖 Generating robots.txt..."

    stage_start

    if ! python3 scripts/run.py robots; then
        die "robots.txt generation failed."
    fi

    stage_end TIME_ROBOTS

    print_ok "robots.txt generated."
}


# ============================================================
# 5. PDF output
# ============================================================


# ============================================================
# 5a. Build individual page PDFs
# ============================================================

build_pdf() {

    print_step "📄 Building individual page PDFs..."

    stage_start

    if ! python3 scripts/run.py pdf; then
        die "individual PDF build failed."
    fi

    stage_end TIME_PDF

    print_ok "Individual page PDFs built."
}


# ============================================================
# 5b. Build category books
# ============================================================

build_categories() {

    print_step "📚 Building category books..."

    stage_start

    if ! python3 scripts/run.py categories; then
        die "category PDF build failed."
    fi

    stage_end TIME_CATEGORIES

    print_ok "Category books built."
}


# ============================================================
# 5c. Build complete course PDF
# ============================================================

build_book() {

    print_step "📚 Building complete course book..."

    stage_start

    if ! python3 scripts/run.py book; then
        die "complete course book build failed."
    fi

    stage_end TIME_BOOK

    print_ok "Complete course book built."
}


# ============================================================
# 5d. Build complete pages PDF
# ============================================================

build_pages_pdf() {

    print_step "📚 Building complete pages.pdf..."

    stage_start

    if ! python3 scripts/run.py pages-pdf; then
        die "complete pages PDF build failed."
    fi

    stage_end TIME_PAGES

    print_ok "Complete pages.pdf built."
}


# ============================================================
# 5e. Composite PDF build
#
# Build all PDF outputs:
#
#   1. Individual page PDFs
#   2. Category PDFs
#   3. Complete course book
#   4. Complete pages PDF
#
# This is a composite operation, so its constituent stages
# provide the individual timings.
# ============================================================

build_allpdf() {

    build_pdf
    build_categories
    build_book
    build_pages_pdf
}


# ============================================================
# 6. Diagnostics
# ============================================================


# ============================================================
# 6a. Build diagnostics summary
#
# Delegate report generation to the Python build layer.
#
# The report receives timing information from the shell
# pipeline through environment variables.
#
# Open Graph timing is split into:
#
#     TIME_OG_GENERATE
#         OG Asymptote source generation
#
#     TIME_OG_BUILD
#         OG PNG generation
#
#     TIME_OG_PUBLISH
#         Explicit OG publishing performed by:
#
#             ./build.sh og-refresh
#
# TIME_OG_PUBLISH records OG publishing performed during
# the normal "all" build and by the explicit "og-refresh"
# target.
# ============================================================

print_summary() {

    BUILD_END=$(date +%s)
    BUILD_TIME=$((BUILD_END - BUILD_START))

    BUILD_TIME="$BUILD_TIME" \
    TIME_CONFIG="$TIME_CONFIG" \
    TIME_METADATA="$TIME_METADATA" \
    TIME_REFMAP="$TIME_REFMAP" \
    TIME_FIX_REFS="$TIME_FIX_REFS" \
    TIME_FIX_EQUATIONS="$TIME_FIX_EQUATIONS" \
    TIME_OG_GENERATE="$TIME_OG_GENERATE" \
    TIME_OG_BUILD="$TIME_OG_BUILD" \
    TIME_OG_PUBLISH="$TIME_OG_PUBLISH" \
    TIME_METADATA_CHECK="$TIME_METADATA_CHECK" \
    TIME_GENERATED_CHECK="$TIME_GENERATED_CHECK" \
    TIME_IMPORT_CHECK="$TIME_IMPORT_CHECK" \
    TIME_OG_CHECK="$TIME_OG_CHECK" \
    TIME_LINKS="$TIME_LINKS" \
    TIME_PREPARE_DIST="$TIME_PREPARE_DIST" \
    TIME_PREPARE_DIAGNOSTICS="$TIME_PREPARE_DIAGNOSTICS" \
    TIME_HTML="$TIME_HTML" \
    TIME_SITEMAP="$TIME_SITEMAP" \
    TIME_ROBOTS="$TIME_ROBOTS" \
    TIME_PDF="$TIME_PDF" \
    TIME_CATEGORIES="$TIME_CATEGORIES" \
    TIME_BOOK="$TIME_BOOK" \
    TIME_PAGES="$TIME_PAGES" \
    TIME_REPORT="$TIME_REPORT" \
        python3 scripts/run.py report
}

# ============================================================
# Build pipeline
# ============================================================

# ------------------------------------------------------------
# Common generation + validation
# ------------------------------------------------------------

run_common_checks() {

    generate_metadata
    validate_metadata
    validate_generated

    generate_og
    build_og

    validate_config
    validate_imports
}


# ============================================================
# Build dispatcher
#
# Composite targets:
#
#   all       Complete site build
#   allpdf    All PDF outputs
#
# Individual targets use the same shell functions as the
# complete build wherever those functions exist. This keeps
# terminal output consistent and ensures timing is recorded
# for stages that participate in the diagnostics system.
# ============================================================

run_build() {

    case "$TARGET" in

        # ----------------------------------------------------
        # Complete build
        # ----------------------------------------------------

        all)

            prepare_diagnostics

            run_common_checks

            prepare_dist
            publish_og

            build_html
            build_refmap
            fix_html_refs
            fix_html_equations

            build_sitemap
            build_robots

            validate_og

            build_allpdf

            validate_links

            ;;

        # ----------------------------------------------------
        # All PDFs
        # ----------------------------------------------------

        allpdf)

            build_allpdf

            ;;

        # ----------------------------------------------------
        # Configuration
        # ----------------------------------------------------

        config)

            validate_config

            ;;

        # ----------------------------------------------------
        # Generation
        # ----------------------------------------------------

        metadata)

            generate_metadata

            ;;

        # ----------------------------------------------------
        # Open Graph
        # ----------------------------------------------------

        og-generate)

            generate_og

            ;;

        og-build)

            build_og

            ;;

        og-publish)

            publish_og

            ;;

        og-refresh)

            og_refresh

            ;;

        # ----------------------------------------------------
        # Validation
        # ----------------------------------------------------

        metadata-check)

            validate_metadata

            ;;

        generated)

            validate_generated

            ;;

        imports)

            validate_imports

            ;;

        og-check)

            validate_og

            ;;

        links)

            validate_links

            ;;

        # ----------------------------------------------------
        # Reference processing
        # ----------------------------------------------------

        refmap)

            build_refmap

            ;;

        fix-refs)

            fix_html_refs

            ;;

        fix-equations)

            fix_html_equations

            ;;

        # ----------------------------------------------------
        # Build preparation
        # ----------------------------------------------------

        prepare-dist)

            prepare_dist

            ;;

        prepare-diagnostics)

            prepare_diagnostics

            ;;

        # ----------------------------------------------------
        # Website output
        # ----------------------------------------------------

        html)

            build_html

            ;;

        sitemap)

            build_sitemap

            ;;

        robots)

            build_robots

            ;;

        # ----------------------------------------------------
        # PDF output
        # ----------------------------------------------------

        pdf)

            build_pdf

            ;;

        categories)

            build_categories

            ;;

        book)

            build_book

            ;;

        pages-pdf)

            build_pages_pdf

            ;;

        # ----------------------------------------------------
        # Diagnostics
        # ----------------------------------------------------

        report)

            print_summary

            ;;

    esac
}


# ============================================================
# Run selected build target
# ============================================================

run_build


# ============================================================
# Print final summary
#
# Only the complete "all" build produces the final diagnostics
# summary.
#
# Individual targets execute only their requested operation.
# This prevents commands such as:
#
#     ./build.sh config
#     ./build.sh metadata
#     ./build.sh html
#     ./build.sh pdf
#
# from unexpectedly generating diagnostics/build_report.txt.
# ============================================================

if [[ "$TARGET" == "all" ]]; then
    print_summary
fi