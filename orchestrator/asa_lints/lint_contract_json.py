"""ASA Linter: Contract JSON Validator"""
import json
from pathlib import Path
from typing import List, Tuple, Dict, Any

REQUIRED_FIELDS = [
    "slice_name",
    "version",
    "domain",
    "allowed_imports",
    "public_api",
    "dependencies",
]

def lint_contract_json(slice_path: Path) -> Tuple[bool, List[str]]:
    """Validate slice.contract.json structure."""
    errors = []
    contract_path = slice_path / "slice.contract.json"

    if not contract_path.exists():
        return False, ["slice.contract.json not found"]

    # Load JSON
    try:
        with open(contract_path, "r") as f:
            contract: Dict[str, Any] = json.load(f)
    except json.JSONDecodeError as e:
        return False, [f"Invalid JSON: {str(e)}"]

    # Check required fields
    for field in REQUIRED_FIELDS:
        if field not in contract:
            errors.append(f"Missing required field: {field}")

    # Validate field types
    if "slice_name" in contract and not isinstance(contract["slice_name"], str):
        errors.append("slice_name must be a string")

    if "version" in contract and not isinstance(contract["version"], str):
        errors.append("version must be a string")

    if "domain" in contract and not isinstance(contract["domain"], str):
        errors.append("domain must be a string")

    if "allowed_imports" in contract and not isinstance(contract["allowed_imports"], list):
        errors.append("allowed_imports must be a list")

    if "public_api" in contract and not isinstance(contract["public_api"], dict):
        errors.append("public_api must be an object")

    if "dependencies" in contract and not isinstance(contract["dependencies"], dict):
        errors.append("dependencies must be an object")

    # Validate public_api structure
    if "public_api" in contract and isinstance(contract["public_api"], dict):
        public_api = contract["public_api"]
        if "exports" in public_api and not isinstance(public_api["exports"], list):
            errors.append("public_api.exports must be a list")

    return len(errors) == 0, errors
