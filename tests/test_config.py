import pathlib
import re
from platform import python_version

from packaging.version import Version

CURRENT_INTERPRETER_VERSION = Version(python_version())

# Regex to match the Python version in PEP 621 style pyproject.toml
PYPROJECT_TOML_VERSION_REGEX = r'requires-python\s*=\s*"([^"]+)"'

# Paths
PROJECT_ROOT = pathlib.Path(__file__).parent.parent.resolve()
PYPROJECT_TOML_PATH = list(PROJECT_ROOT.glob("pyproject.toml"))
MAKEFILE_PATH = list(PROJECT_ROOT.glob("Makefile"))
PRECOMMIT_HOOKS_PATH = list(PROJECT_ROOT.glob(".git/hooks/*"))


def test_file_uniqueness() -> None:
    """Ensure only one pyproject.toml and Makefile exists."""
    if len(PYPROJECT_TOML_PATH) != 1:
        raise ValueError(
            "Found more than one 'pyproject.toml':"
            f" {', '.join(str(p) for p in PYPROJECT_TOML_PATH)}"
        )

    if len(MAKEFILE_PATH) != 1:
        raise ValueError(
            f"Found more than one 'Makefile': {', '.join(str(p) for p in MAKEFILE_PATH)}"
        )


def test_python_version_is_specified() -> None:
    """Check that pyproject.toml specifies a Python version."""
    with open(PYPROJECT_TOML_PATH[0], encoding="utf-8") as f:
        pyproject_toml = f.read()

    toml_versions = re.findall(PYPROJECT_TOML_VERSION_REGEX, pyproject_toml)
    if not toml_versions:
        raise ValueError("No Python version specified in 'pyproject.toml'")


def test_precommit_hooks_is_set() -> None:
    """Verify that pre-commit hooks are installed."""
    if len(PRECOMMIT_HOOKS_PATH) == 0:
        raise ValueError("Pre-commit hooks are not set. Run `make pre-commit`")
