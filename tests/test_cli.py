"""Tests for ASA CLI"""
import pytest
from click.testing import CliRunner
from orchestrator.cli import main
from pathlib import Path


@pytest.fixture
def cli_runner():
    """Create CLI runner."""
    return CliRunner()


def test_cli_help(cli_runner):
    """Test asa --help."""
    result = cli_runner.invoke(main, ["--help"])
    assert result.exit_code == 0
    assert "ASA CLI Tool" in result.output
    assert "list-slices" in result.output
    assert "lint" in result.output
    assert "lint-all" in result.output
    assert "generate-slice" in result.output
    assert "mcp-server" in result.output


def test_cli_version(cli_runner):
    """Test asa --version."""
    result = cli_runner.invoke(main, ["--version"])
    assert result.exit_code == 0
    assert "0.9.0" in result.output


def test_list_slices(cli_runner):
    """Test asa list-slices."""
    result = cli_runner.invoke(main, ["list-slices"])
    assert result.exit_code == 0
    assert "Found" in result.output
    assert "auth/login_demo" in result.output


def test_list_slices_with_domain_filter(cli_runner):
    """Test asa list-slices --domain auth."""
    result = cli_runner.invoke(main, ["list-slices", "--domain", "auth"])
    assert result.exit_code == 0
    assert "auth/login_demo" in result.output


def test_list_slices_with_invalid_domain(cli_runner):
    """Test asa list-slices --domain nonexistent."""
    result = cli_runner.invoke(main, ["list-slices", "--domain", "nonexistent"])
    assert result.exit_code == 0
    assert "No slices found" in result.output


def test_lint_success(cli_runner):
    """Test asa lint on valid slice."""
    result = cli_runner.invoke(main, ["lint", "domains/auth/slices/login_demo"])
    assert result.exit_code == 0
    assert "Structure: OK" in result.output
    assert "Contract: OK" in result.output
    assert "Loc Limits: OK" in result.output
    assert "Imports: OK" in result.output
    assert "PASSED" in result.output


def test_lint_nonexistent_path(cli_runner):
    """Test asa lint on nonexistent path."""
    result = cli_runner.invoke(main, ["lint", "domains/nonexistent/slice"])
    assert result.exit_code != 0


def test_lint_all_success(cli_runner):
    """Test asa lint-all."""
    result = cli_runner.invoke(main, ["lint-all"])
    assert result.exit_code == 0
    assert "Linting" in result.output
    assert "Summary:" in result.output
    assert "Total:" in result.output
    assert "Passed:" in result.output


def test_lint_all_with_domain_filter(cli_runner):
    """Test asa lint-all --domain auth."""
    result = cli_runner.invoke(main, ["lint-all", "--domain", "auth"])
    assert result.exit_code == 0
    assert "Linting" in result.output


def test_lint_help(cli_runner):
    """Test asa lint --help."""
    result = cli_runner.invoke(main, ["lint", "--help"])
    assert result.exit_code == 0
    assert "Lint a specific slice" in result.output
    assert "Structure check" in result.output
    assert "Contract validation" in result.output


def test_generate_slice_help(cli_runner):
    """Test asa generate-slice --help."""
    result = cli_runner.invoke(main, ["generate-slice", "--help"])
    assert result.exit_code == 0
    assert "Generate a new slice" in result.output
    assert "--func-spec" in result.output
    assert "--domain" in result.output
    assert "--slice-name" in result.output


def test_mcp_server_help(cli_runner):
    """Test asa mcp-server --help."""
    result = cli_runner.invoke(main, ["mcp-server", "--help"])
    assert result.exit_code == 0
    assert "MCP server management" in result.output


def test_mcp_server_start_help(cli_runner):
    """Test asa mcp-server start --help."""
    result = cli_runner.invoke(main, ["mcp-server", "start", "--help"])
    assert result.exit_code == 0
    assert "Start the MCP server" in result.output
    assert "--port" in result.output


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
