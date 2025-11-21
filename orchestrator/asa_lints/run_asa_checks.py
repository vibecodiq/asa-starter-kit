"""ASA Linter Orchestrator"""
from pathlib import Path
from typing import Dict, List
from .lint_slice_structure import lint_slice_structure
from .lint_contract_json import lint_contract_json
from .lint_loc_limits import lint_loc_limits
from .lint_contract_imports import lint_contract_imports

def run_asa_checks(slice_path: Path) -> Dict:
    """Run all ASA linters on a slice."""
    results = {
        "slice_path": str(slice_path),
        "checks": {},
        "overall_status": "PASSED",
        "has_warnings": False
    }

    # Run structure check
    success, errors = lint_slice_structure(slice_path)
    results["checks"]["structure"] = {
        "status": "OK" if success else "FAILED",
        "errors": errors
    }
    if not success:
        results["overall_status"] = "FAILED"

    # Run contract check
    success, errors = lint_contract_json(slice_path)
    results["checks"]["contract"] = {
        "status": "OK" if success else "FAILED",
        "errors": errors
    }
    if not success:
        results["overall_status"] = "FAILED"

    # Run LOC check
    success, errors = lint_loc_limits(slice_path)
    results["checks"]["loc_limits"] = {
        "status": "OK" if success else "WARNING",
        "errors": errors
    }
    if not success:
        results["has_warnings"] = True

    # Run imports check
    success, errors = lint_contract_imports(slice_path)
    results["checks"]["imports"] = {
        "status": "OK" if success else "FAILED",
        "errors": errors
    }
    if not success:
        results["overall_status"] = "FAILED"

    return results

def format_results(results: Dict) -> str:
    """Format linter results for CLI output."""
    output = []
    output.append(f"\nLinting: {results['slice_path']}\n")

    # Print each check
    for check_name, check_data in results["checks"].items():
        status = check_data["status"]
        icon = "✅" if status == "OK" else ("⚠️" if status == "WARNING" else "❌")
        output.append(f"{icon} {check_name.replace('_', ' ').title()}: {status}")

        if check_data["errors"]:
            for error in check_data["errors"]:
                output.append(f"  {error}")

    # Overall result
    output.append(f"\nResult: {results['overall_status']}")
    if results["has_warnings"]:
        output.append("(with warnings)")

    return "\n".join(output)
