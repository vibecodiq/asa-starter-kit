"""ASA Linter: Slice Structure Checker"""
from pathlib import Path
from typing import List, Tuple

REQUIRED_FILES = [
    "slice.spec.md",
    "slice.contract.json",
    "handler.py",
    "service.py",
    "repository.py",
    "schemas.py",
    "tests/test_slice.py",
]

def lint_slice_structure(slice_path: Path) -> Tuple[bool, List[str]]:
    """Check if slice has all required files."""
    errors = []

    if not slice_path.exists():
        return False, [f"Slice path does not exist: {slice_path}"]

    if not slice_path.is_dir():
        return False, [f"Slice path is not a directory: {slice_path}"]

    # Check required files
    for required_file in REQUIRED_FILES:
        file_path = slice_path / required_file
        if not file_path.exists():
            errors.append(f"Missing required file: {required_file}")

    # Check slice name (lowercase, no spaces)
    slice_name = slice_path.name
    if not slice_name.islower():
        errors.append(f"Slice name must be lowercase: {slice_name}")

    if " " in slice_name:
        errors.append(f"Slice name cannot contain spaces: {slice_name}")

    return len(errors) == 0, errors
