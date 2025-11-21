"""
ASA CLI Tool

Command-line interface for ASA operations.
"""
import click
from pathlib import Path
from .asa_lints import run_asa_checks, format_results


@click.group()
@click.version_option(version="0.9.0", prog_name="asa")
def main():
    """
    ASA CLI Tool - AI-Sliced Architecture utilities.

    Use 'asa COMMAND --help' for more information on a command.
    """
    pass


@main.command()
@click.option(
    "--domain",
    "-d",
    help="Filter by domain (e.g., auth, users)",
    default=None
)
def list_slices(domain):
    """
    List all slices in the project.

    Example:
        asa list-slices
        asa list-slices --domain auth
    """
    domains_path = Path("domains")

    if not domains_path.exists():
        click.echo("❌ No domains/ directory found", err=True)
        return

    slices = []

    # Find all slices
    for domain_dir in domains_path.iterdir():
        if not domain_dir.is_dir():
            continue

        # Filter by domain if specified
        if domain and domain_dir.name != domain:
            continue

        slices_dir = domain_dir / "slices"
        if slices_dir.exists():
            for slice_dir in slices_dir.iterdir():
                if (slice_dir.is_dir() and 
                    not slice_dir.name.startswith(".") and 
                    not slice_dir.name.startswith("__")):
                    slices.append(f"{domain_dir.name}/{slice_dir.name}")

    if not slices:
        click.echo("No slices found")
        return

    click.echo(f"\nFound {len(slices)} slice(s):\n")
    for slice_name in sorted(slices):
        click.echo(f"  • {slice_name}")
    click.echo()


@main.command()
@click.argument("slice_path", type=click.Path(exists=True))
def lint(slice_path):
    """
    Lint a specific slice.

    Runs all ASA linters on the specified slice:
    - Structure check (required files)
    - Contract validation (slice.contract.json)
    - LOC limits check
    - Import validation

    Example:
        asa lint domains/auth/slices/login_demo
    """
    slice_path = Path(slice_path)

    if not slice_path.is_dir():
        click.echo(f"❌ Not a directory: {slice_path}", err=True)
        return 1

    # Run linters
    results = run_asa_checks(slice_path)

    # Format and print results
    output = format_results(results)
    click.echo(output)

    # Exit with appropriate code
    if results["overall_status"] == "FAILED":
        return 1
    return 0


@main.command()
@click.option(
    "--domain",
    "-d",
    help="Filter by domain",
    default=None
)
@click.option(
    "--fail-fast",
    "-f",
    is_flag=True,
    help="Stop on first failure"
)
def lint_all(domain, fail_fast):
    """
    Lint all slices in the project.

    Example:
        asa lint-all
        asa lint-all --domain auth
        asa lint-all --fail-fast
    """
    domains_path = Path("domains")

    if not domains_path.exists():
        click.echo("❌ No domains/ directory found", err=True)
        return 1

    # Find all slices
    slices = []
    for domain_dir in domains_path.iterdir():
        if not domain_dir.is_dir():
            continue

        if domain and domain_dir.name != domain:
            continue

        slices_dir = domain_dir / "slices"
        if slices_dir.exists():
            for slice_dir in slices_dir.iterdir():
                if (slice_dir.is_dir() and 
                    not slice_dir.name.startswith(".") and 
                    not slice_dir.name.startswith("__")):
                    slices.append(slice_dir)

    if not slices:
        click.echo("No slices found")
        return 0

    click.echo(f"\n{'='*60}")
    click.echo(f"Linting {len(slices)} slice(s)")
    click.echo(f"{'='*60}\n")

    failed_slices = []
    warning_slices = []

    for slice_path in slices:
        results = run_asa_checks(slice_path)
        output = format_results(results)
        click.echo(output)
        click.echo()

        if results["overall_status"] == "FAILED":
            failed_slices.append(str(slice_path))
            if fail_fast:
                click.echo("❌ Stopping due to --fail-fast")
                return 1
        elif results["has_warnings"]:
            warning_slices.append(str(slice_path))

    # Summary
    click.echo(f"{'='*60}")
    click.echo("Summary:")
    click.echo(f"  Total: {len(slices)}")
    click.echo(f"  Passed: {len(slices) - len(failed_slices)}")
    click.echo(f"  Failed: {len(failed_slices)}")
    click.echo(f"  Warnings: {len(warning_slices)}")
    click.echo(f"{'='*60}\n")

    if failed_slices:
        click.echo("❌ Failed slices:")
        for slice_path in failed_slices:
            click.echo(f"  • {slice_path}")
        return 1

    if warning_slices:
        click.echo("⚠️ Slices with warnings:")
        for slice_path in warning_slices:
            click.echo(f"  • {slice_path}")

    click.echo("✅ All slices passed!")
    return 0


@main.command()
@click.option(
    "--func-spec",
    "-f",
    required=True,
    help="Functional specification (plain text)"
)
@click.option(
    "--domain",
    "-d",
    required=True,
    help="Domain name (e.g., auth, users)"
)
@click.option(
    "--slice-name",
    "-s",
    required=True,
    help="Slice name (e.g., login, register)"
)
@click.option(
    "--output",
    "-o",
    help="Output directory (default: domains/<domain>/slices/<slice-name>)",
    default=None
)
def generate_slice(func_spec, domain, slice_name, output):
    """
    Generate a new slice from functional specification.

    This command calls the MCP server to generate:
    - slice.spec.md
    - slice.contract.json
    - Skeleton files (handler, service, repository, schemas, tests)

    Example:
        asa generate-slice \\
          --func-spec "User registration with email verification" \\
          --domain auth \\
          --slice-name register
    """
    import httpx

    # Default output path
    if output is None:
        output = f"domains/{domain}/slices/{slice_name}"

    output_path = Path(output)

    # Check if slice already exists
    if output_path.exists():
        if not click.confirm(f"⚠️ Slice already exists at {output}. Overwrite?"):
            click.echo("Cancelled")
            return

    click.echo(f"\n🔨 Generating slice: {domain}/{slice_name}\n")

    # Call MCP server
    try:
        # Note: MCP server must be running (Task 6)
        response = httpx.post(
            "http://localhost:8001/mcp/generate-skeleton",
            json={
                "func_spec": func_spec,
                "domain": domain,
                "slice_name": slice_name,
                "output_path": str(output_path)
            },
            timeout=30.0
        )

        if response.status_code == 200:
            data = response.json()
            click.echo("✅ Slice generated successfully!\n")
            click.echo("Created files:")
            for file in data.get("created_files", []):
                click.echo(f"  • {file}")

            # Run linter
            click.echo(f"\n🔍 Running linter...\n")
            results = run_asa_checks(output_path)
            output_text = format_results(results)
            click.echo(output_text)

            if results["overall_status"] == "PASSED":
                click.echo("\n✅ Slice is ready to use!")
                click.echo(f"\nNext steps:")
                click.echo(f"  1. Review generated files in {output}")
                click.echo(f"  2. Implement business logic in service.py")
                click.echo(f"  3. Run tests: pytest {output}/tests/")
                click.echo(f"  4. Register router in main.py")
            else:
                click.echo("\n⚠️ Linter found issues. Please fix before using.")
        else:
            click.echo(f"❌ MCP server error: {response.status_code}", err=True)
            click.echo(response.text, err=True)
            return 1

    except httpx.ConnectError:
        click.echo("❌ Cannot connect to MCP server", err=True)
        click.echo("Make sure MCP server is running: asa mcp-server start", err=True)
        return 1
    except Exception as e:
        click.echo(f"❌ Error: {str(e)}", err=True)
        return 1


@main.group()
def mcp_server():
    """MCP server management commands."""
    pass


@mcp_server.command()
@click.option(
    "--port",
    "-p",
    default=8001,
    help="Port to run MCP server on (default: 8001)"
)
def start(port):
    """
    Start the MCP server.

    Example:
        asa mcp-server start
        asa mcp-server start --port 8002
    """
    import subprocess

    click.echo(f"🚀 Starting MCP server on port {port}...")

    try:
        subprocess.run(
            ["python", "-m", "mcp_server.main", "--port", str(port)],
            check=True
        )
    except KeyboardInterrupt:
        click.echo("\n👋 MCP server stopped")
    except Exception as e:
        click.echo(f"❌ Error starting MCP server: {str(e)}", err=True)
        return 1


if __name__ == "__main__":
    main()
