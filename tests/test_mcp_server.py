"""Tests for MCP Server"""
import pytest
from fastapi.testclient import TestClient
from mcp_server.main import app
from pathlib import Path
import shutil

client = TestClient(app)


def test_mcp_root():
    """Test MCP server root endpoint"""
    response = client.get("/")
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["service"] == "ASA MCP Server"
    assert data["version"] == "0.9.0"


def test_generate_spec():
    """Test generate-spec endpoint"""
    response = client.post(
        "/mcp/generate-spec",
        json={
            "func_spec": "User registration feature",
            "domain": "auth",
            "slice_name": "register"
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "spec_md" in data
    assert "auth/register" in data["spec_md"]


def test_generate_contract():
    """Test generate-contract endpoint"""
    response = client.post(
        "/mcp/generate-contract",
        json={
            "spec_md": "# Test spec",
            "domain": "auth",
            "slice_name": "register"
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "contract_json" in data
    # Verify it's valid JSON
    import json
    contract = json.loads(data["contract_json"])
    assert contract["domain"] == "auth"
    assert contract["slice_name"] == "auth/register"


def test_generate_skeleton():
    """Test generate-skeleton endpoint"""
    # Create temp output directory
    output_path = Path("test_generated_slice")
    
    # Clean up if exists
    if output_path.exists():
        shutil.rmtree(output_path)
    
    try:
        response = client.post(
            "/mcp/generate-skeleton",
            json={
                "func_spec": "Test feature",
                "domain": "test",
                "slice_name": "demo",
                "output_path": str(output_path)
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "created_files" in data
        
        # Verify files were created
        created_files = data["created_files"]
        assert len(created_files) > 0
        
        # Check key files exist
        assert (output_path / "slice.spec.md").exists()
        assert (output_path / "slice.contract.json").exists()
        assert (output_path / "handler.py").exists()
        assert (output_path / "service.py").exists()
        assert (output_path / "repository.py").exists()
        assert (output_path / "schemas.py").exists()
        assert (output_path / "tests" / "test_slice.py").exists()
        
    finally:
        # Cleanup
        if output_path.exists():
            shutil.rmtree(output_path)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
