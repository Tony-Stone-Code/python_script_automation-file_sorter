# Setup & Installation Guide

This guide helps both new users and technical maintainers install, configure, and run the File Sorter tool (2025). It contains quick-start instructions for beginners and deeper steps for developers.

Notes and assumptions
- Assumes a checkout of this repository (root contains `files_sorter.py`, package directory `file_sorter/`, and `config.example.json`).
- Assumes Windows environment with PowerShell (user shell: PowerShell 5+). Commands below use PowerShell syntax.
- Recommended Python: 3.10+ (3.11 or 3.12 recommended in 2025). If the project requires a different version, adjust accordingly.

## Quick start (for newbies)
If you just want to try the tool locally (recommended):

1. Install Python 3.10+ from https://www.python.org/ if not already installed.
2. Open PowerShell and create an isolated virtual environment, activate it, install dependencies, and run the script:

```powershell
# From the project root
python -m venv .venv
# Activate the venv (PowerShell)
.\.venv\Scripts\Activate.ps1
# Install project dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Run the quick example (script is at project root)
python .\files_sorter.py --help
```

3. Try a basic run (replace source/destination paths with real folders):

```powershell
# Example: sort files from source into categorized folders under destination
python .\files_sorter.py --source "C:\Users\You\Downloads" --dest "C:\Users\You\Sorted"
```

Notes:
- If a console script / entry point is provided by the package (may be added later), you could run `file-sorter` directly after installing via `pip install .`.

## For technical users / developers
This section covers development workflow, local installs, running as a module, and tests.

### Install for development (editable install)
Create and activate a virtual environment, then install the package in editable mode so changes are reflected immediately:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -e .
# or: pip install -r requirements.txt
```

Editable install lets you run code as a package and import modules from `file_sorter`.

### Running as a module
You can run the CLI module directly with Python's `-m` option (useful during development):

```powershell
# Run the CLI module
python -m file_sorter.cli --help
# Run watch mode
python -m file_sorter.watch --help
```

If the top-level `files_sorter.py` script is meant as the primary entrypoint, you can continue using it as shown in Quick start.

### Configuration
This project includes `config.example.json` in the repo root. To configure the tool:

1. Copy the example to a working config file:

```powershell
copy .\config.example.json .\config.json
```

2. Edit `config.json` to set: source directories, destination rules, file type mappings, and any behaviour flags (watch intervals, dry-run toggles, etc.).

3. If the tool reads environment variables, set them in PowerShell like:

```powershell
$env:FILESORTER_CONFIG = "C:\path\to\config.json"
# To persist across sessions, set via System settings or use setx
setx FILESORTER_CONFIG "C:\path\to\config.json"
```

(If this repository uses a different env var name, substitute accordingly.)

### Running tests
This repository includes pytest tests in the `tests/` folder. Run them like this (inside the activated venv):

```powershell
pip install -r requirements.txt
pip install -r requirements-dev.txt --no-deps -r requirements.txt  # if a dev file exists
# Run pytest (showing short summary)
python -m pytest -q
```

# Setup & Installation Guide

This guide helps both new users and technical maintainers install, configure, and run the File Sorter tool (2025). It contains quick-start instructions for beginners and deeper steps for developers.

## Notes and assumptions

- Assumes a checkout of this repository (root contains `files_sorter.py`, package directory `file_sorter/`, and `config.example.json`).
- Assumes Windows environment with PowerShell (user shell: PowerShell 5+). Commands below use PowerShell syntax.
- Recommended Python: 3.10+ (3.11 or 3.12 recommended in 2025). If the project requires a different version, adjust accordingly.

## Quick start (for newbies)

If you just want to try the tool locally (recommended):

1. Install Python 3.10+ from [python.org](https://www.python.org/) if not already installed.

2. Open PowerShell and create an isolated virtual environment, activate it, install dependencies, and run the script:

```powershell
# From the project root
python -m venv .venv
# Activate the venv (PowerShell)
.\.venv\Scripts\Activate.ps1
# Install project dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Run the quick example (script is at project root)
python .\files_sorter.py --help
```

3. Try a basic run (replace source/destination paths with real folders):

```powershell
# Example: sort files from source into categorized folders under destination
python .\files_sorter.py --source "C:\Users\You\Downloads" --dest "C:\Users\You\Sorted"
```

Notes:

- If a console script / entry point is provided by the package (may be added later), you could run `file-sorter` directly after installing via `pip install .`.

## For technical users / developers

This section covers development workflow, local installs, running as a module, and tests.

### Install for development (editable install)

Create and activate a virtual environment, then install the package in editable mode so changes are reflected immediately:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -e .
# or: pip install -r requirements.txt
```

Editable install lets you run code as a package and import modules from `file_sorter`.

### Running as a module

You can run the CLI module directly with Python's `-m` option (useful during development):

```powershell
# Run the CLI module
python -m file_sorter.cli --help
# Run watch mode
python -m file_sorter.watch --help
```

If the top-level `files_sorter.py` script is meant as the primary entrypoint, you can continue using it as shown in Quick start.

### Configuration

This project includes `config.example.json` in the repo root. To configure the tool:

1. Copy the example to a working config file:

```powershell
copy .\config.example.json .\config.json
```

2. Edit `config.json` to set source directories, destination rules, file type mappings, and any behaviour flags (watch intervals, dry-run toggles, etc.).

3. If the tool reads environment variables, set them in PowerShell like:

```powershell
$env:FILESORTER_CONFIG = "C:\path\to\config.json"
# To persist across sessions, set via System settings or use setx
setx FILESORTER_CONFIG "C:\path\to\config.json"
```

(If this repository uses a different env var name, substitute accordingly.)

### Running tests

This repository includes pytest tests in the `tests/` folder. Run them like this (inside the activated venv):

```powershell
pip install -r requirements.txt
# If a dev requirements file exists, install it (adjust filename as needed)
# pip install -r requirements-dev.txt
# Run pytest (showing short summary)
python -m pytest -q
```

If there is no separate `requirements-dev.txt`, install `pytest` manually:

```powershell
pip install pytest
python -m pytest -q
```

### Linting and type checks (optional)

If the project includes linters and type checking (e.g., flake8, black, mypy), run them locally according to the repo conventions. Example:

```powershell
pip install black flake8 mypy
black .
flake8
mypy file_sorter
```

## Watch mode (file system monitoring)

If the project provides a watch mode (likely `file_sorter/watch.py` or `file_sorter/watch` module), run:

```powershell
python -m file_sorter.watch --source "C:\Users\You\Downloads" --dest "C:\Users\You\Sorted"
```

Watch mode typically keeps running and responds to new files according to the configured rules. Use a `--dry-run` or `--verbose` flag if available to validate behaviour before changing filesystem state.

## Packaging and distribution

To build a wheel locally:

```powershell
pip install build
python -m build
# Dist artifacts will be in ./dist
```

To publish to PyPI, follow standard packaging and publishing steps (set up PyPI account, use twine):

```powershell
pip install twine
python -m twine upload dist/*
```

If you plan to produce a console script entry point (recommended for end users), add a `console_scripts` entry in `setup.py` or `pyproject.toml` and test after `pip install .`.

## Troubleshooting & common issues

- "Module not found" or import errors: ensure the virtual environment is active and you installed the package (`pip install -e .`) or run using `python .\files_sorter.py`.
- Permissions errors when moving files: run PowerShell as a user with appropriate filesystem permissions, or adjust the destination folder ACLs.
- File locking on Windows: Some files may be locked by other apps; use `--retry` or close the locking program.
- Tests failing locally: ensure the venv is active and dependencies are installed; check Python version compatibility.

## Quick reference (commands)

PowerShell commands (copy-paste):

```powershell
# Setup venv, activate, install deps
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Run script
python .\files_sorter.py --source "C:\Downloads" --dest "C:\Sorted"

# Run tests
pip install pytest
python -m pytest -q
```

## Next steps and how to contribute

- If you'd like a packaged console entrypoint (so users can run `file-sorter`), we can add `console_scripts` and CI packaging.
- Improve README with examples and sample `config.json` content.
- Add more tests for edge cases (large files, long paths, Unicode filenames).