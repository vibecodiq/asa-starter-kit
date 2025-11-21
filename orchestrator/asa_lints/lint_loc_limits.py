"""ASA Linter: LOC Limits Checker"""
import json
from pathlib import Path
from typing import List, Tuple, Dict, Optional

DEFAULT_LOC_PER_FILE = 350
DEFAULT_LOC_TOTAL = 600

FILES_TO_CHECK = ["handler.py", "service.py", "repository.py", "schemas.py"]

def count_loc(file_path: Path) -> int:
    """Count lines of code (excluding empty lines and comments)."""
    if not file_path.exists():
        return 0

    loc = 0
    with open(file_path, "r") as f:
        for line in f:
            stripped = line.strip()
            # Skip empty lines and comments
            if stripped and not stripped.startswith("#"):
                loc += 1
    return loc

def get_custom_limits(slice_path: Path) -> Optional[Dict]:
    """Get custom LOC limits from contract.json if specified."""
    contract_path = slice_path / "slice.contract.json"
    if not contract_path.exists():
        return None

    try:
        with open(contract_path, "r") as f:
            contract = json.load(f)
        return contract.get("loc_limits")
    except:
        return None

def lint_loc_limits(slice_path: Path) -> Tuple[bool, List[str]]:
    """Check LOC limits for slice files."""
    errors = []
    warnings = []

    # Get custom limits if any
    custom_limits = get_custom_limits(slice_path)

    if custom_limits:
        max_per_file = custom_limits.get("per_file", DEFAULT_LOC_PER_FILE)
        max_total = custom_limits.get("total", DEFAULT_LOC_TOTAL)
        justification = custom_limits.get("justification", "")
        has_override = True
    else:
        max_per_file = DEFAULT_LOC_PER_FILE
        max_total = DEFAULT_LOC_TOTAL
        justification = ""
        has_override = False

    # Check each file
    total_loc = 0
    for filename in FILES_TO_CHECK:
        file_path = slice_path / filename
        if file_path.exists():
            loc = count_loc(file_path)
            total_loc += loc

            if loc > max_per_file:
                if has_override:
                    warnings.append(
                        f"⚠️ {filename}: {loc} LOC (max {max_per_file}) - "
                        f"Override specified: {justification}"
                    )
                else:
                    errors.append(
                        f"❌ {filename}: {loc} LOC exceeds limit of {max_per_file}"
                    )

    # Check total LOC
    if total_loc > max_total:
        if has_override:
            warnings.append(
                f"⚠️ Total: {total_loc} LOC (max {max_total}) - "
                f"Override specified: {justification}"
            )
        else:
            errors.append(
                f"❌ Total: {total_loc} LOC exceeds limit of {max_total}"
            )

    # Print warnings
    for warning in warnings:
        print(warning)

    return len(errors) == 0, errors
