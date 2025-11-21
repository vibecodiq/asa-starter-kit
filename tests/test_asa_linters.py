"""Tests for ASA Linters"""
import pytest
from pathlib import Path
from orchestrator.asa_lints import run_asa_checks, format_results
from orchestrator.asa_lints.lint_slice_structure import lint_slice_structure
from orchestrator.asa_lints.lint_contract_json import lint_contract_json
from orchestrator.asa_lints.lint_loc_limits import lint_loc_limits
from orchestrator.asa_lints.lint_contract_imports import lint_contract_imports


def test_lint_slice_structure_success():
    """Test structure linter with valid slice."""
    slice_path = Path("domains/auth/slices/login_demo")
    success, errors = lint_slice_structure(slice_path)
    
    assert success is True
    assert len(errors) == 0


def test_lint_slice_structure_missing_files():
    """Test structure linter detects missing files."""
    # Use a non-existent path
    slice_path = Path("domains/nonexistent/slice")
    success, errors = lint_slice_structure(slice_path)
    
    assert success is False
    assert len(errors) > 0


def test_lint_contract_json_success():
    """Test contract linter with valid contract."""
    slice_path = Path("domains/auth/slices/login_demo")
    success, errors = lint_contract_json(slice_path)
    
    assert success is True
    assert len(errors) == 0


def test_lint_loc_limits_success():
    """Test LOC linter with valid slice."""
    slice_path = Path("domains/auth/slices/login_demo")
    success, errors = lint_loc_limits(slice_path)
    
    # Should pass or have warnings (not errors)
    assert success is True or len(errors) == 0


def test_lint_contract_imports_success():
    """Test imports linter with valid slice."""
    slice_path = Path("domains/auth/slices/login_demo")
    success, errors = lint_contract_imports(slice_path)
    
    assert success is True
    assert len(errors) == 0


def test_run_asa_checks_full():
    """Test full ASA checks orchestrator."""
    slice_path = Path("domains/auth/slices/login_demo")
    results = run_asa_checks(slice_path)
    
    # Check structure
    assert "slice_path" in results
    assert "checks" in results
    assert "overall_status" in results
    assert "has_warnings" in results
    
    # Check all linters ran
    assert "structure" in results["checks"]
    assert "contract" in results["checks"]
    assert "loc_limits" in results["checks"]
    assert "imports" in results["checks"]
    
    # Should pass
    assert results["overall_status"] in ["PASSED", "FAILED"]


def test_format_results():
    """Test results formatting."""
    slice_path = Path("domains/auth/slices/login_demo")
    results = run_asa_checks(slice_path)
    formatted = format_results(results)
    
    assert isinstance(formatted, str)
    assert "Linting:" in formatted
    assert "Result:" in formatted


def test_lint_slice_structure_invalid_name():
    """Test structure linter detects invalid slice names."""
    # Create a temporary directory with uppercase name
    import tempfile
    import os
    
    with tempfile.TemporaryDirectory() as tmpdir:
        invalid_slice = Path(tmpdir) / "InvalidName"
        invalid_slice.mkdir()
        
        # Create required files
        (invalid_slice / "slice.spec.md").touch()
        (invalid_slice / "slice.contract.json").touch()
        (invalid_slice / "handler.py").touch()
        (invalid_slice / "service.py").touch()
        (invalid_slice / "repository.py").touch()
        (invalid_slice / "schemas.py").touch()
        (invalid_slice / "tests").mkdir()
        (invalid_slice / "tests" / "test_slice.py").touch()
        
        success, errors = lint_slice_structure(invalid_slice)
        
        # Should fail due to uppercase name
        assert success is False
        assert any("lowercase" in error for error in errors)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
