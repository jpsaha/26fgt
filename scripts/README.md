# Scripts

Build and validation machinery.

This directory contains the Python tools used to generate, build, validate, and
diagnose the project.

## Structure

### `build/`

Build and publication commands.

These scripts handle:

- generating metadata
- preparing the distribution directory
- building HTML pages
- building individual PDFs
- building category PDFs
- building the complete book
- building the complete pages PDF
- generating build reports

### `metadata/`

Metadata processing.

These scripts handle:

- discovering source files
- parsing metadata
- generating navigation information
- generating Typst files
- generating homepage data
- generating metadata reports

### `lint/`

Validation and consistency checks.

These scripts check:

- source metadata
- generated files
- Typst imports
- HTML links

The `lint/generated/` and `lint/imports/` directories contain supporting modules
for these checks.

### `utils/`

Shared Python utilities used by the build system.

### `config.py`

Central project configuration and filesystem paths.

Paths used throughout the build system should be defined here rather than
duplicated across individual scripts.

### `run.py`

Command dispatcher for the Python build system.

It provides a single interface for commands such as:

```text
python3 scripts/run.py metadata
python3 scripts/run.py html
python3 scripts/run.py pdf
python3 scripts/run.py categories
python3 scripts/run.py book
python3 scripts/run.py pages-pdf
python3 scripts/run.py metadata-check
python3 scripts/run.py generated
python3 scripts/run.py imports
python3 scripts/run.py links
python3 scripts/run.py prepare-dist
python3 scripts/run.py report
```
