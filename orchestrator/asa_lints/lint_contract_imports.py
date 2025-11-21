"""ASA Linter: Contract Imports Validator"""
import ast
from pathlib import Path
from typing import List, Tuple, Set
import fnmatch

def extract_imports(file_path: Path) -> Set[str]:
    """Extract all imports from a Python file using AST."""
    if not file_path.exists():
        return set()

    imports = set()

    try:
        with open(file_path, "r") as f:
            tree = ast.parse(f.read())

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.add(alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.add(node.module)
    except:
        pass

    return imports

def is_allowed_import(import_name: str, allowed_patterns: List[str]) -> bool:
    """Check if import matches any allowed pattern (glob-style)."""
    for pattern in allowed_patterns:
        # Convert glob pattern to match
        if fnmatch.fnmatch(import_name, pattern):
            return True
        # Also check if import starts with pattern (for submodules)
        if import_name.startswith(pattern.replace(".*", "")):
            return True
    return False

def lint_contract_imports(slice_path: Path) -> Tuple[bool, List[str]]:
    """Validate imports against allowed_imports in contract."""
    errors = []

    # Load contract
    contract_path = slice_path / "slice.contract.json"
    if not contract_path.exists():
        return False, ["slice.contract.json not found"]

    try:
        import json
        with open(contract_path, "r") as f:
            contract = json.load(f)
        allowed_imports = contract.get("allowed_imports", [])
    except:
        return False, ["Failed to load contract.json"]

    # Check Python files
    python_files = ["handler.py", "service.py", "repository.py", "schemas.py"]

    for filename in python_files:
        file_path = slice_path / filename
        if file_path.exists():
            imports = extract_imports(file_path)

            # Filter internal imports (domains.*, shared.*)
            internal_imports = {
                imp for imp in imports
                if imp.startswith("domains.") or imp.startswith("shared.")
            }

            # Check each internal import
            for imp in internal_imports:
                if not is_allowed_import(imp, allowed_imports):
                    errors.append(
                        f"{filename}: Unauthorized import '{imp}' "
                        f"(not in allowed_imports)"
                    )

    return len(errors) == 0, errors
