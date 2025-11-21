# Changelog

All notable changes to the ASA Starter Kit will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [0.9.0] - 2025-11-21

### Added

#### Core Features
- **ASA Architecture Implementation** - Complete AI-Sliced Architecture pattern
- **Demo Authentication Slice** - `domains/auth/slices/login_demo/` with full implementation
- **Shared Modules** - Reusable entities, utilities, and value objects
- **FastAPI Main Server** - Production-ready server on port 8000

#### ASA Linter Engine
- **Structure Linter** - Validates required files in slices
- **Contract Linter** - Validates `slice.contract.json` format
- **LOC Limits Linter** - Enforces line-of-code limits per file
- **Import Linter** - Validates import rules and dependencies
- **Linter Orchestrator** - Runs all linters and aggregates results

#### CLI Tool
- **`asa` command** - Main CLI entry point
- **`asa list-slices`** - List all slices in the project
- **`asa lint <path>`** - Lint specific slice
- **`asa lint-all`** - Lint all slices
- **`asa generate-slice`** - Generate new slice from specification
- **`asa mcp-server start`** - Start MCP server

#### MCP Server
- **MCP FastAPI Server** - Slice generation server on port 8001
- **Generate Spec Endpoint** - `/mcp/generate-spec` for `slice.spec.md`
- **Generate Contract Endpoint** - `/mcp/generate-contract` for `slice.contract.json`
- **Generate Skeleton Endpoint** - `/mcp/generate-skeleton` for complete slice
- **7 Jinja2 Templates** - For generating all slice files

#### Testing
- **42 Tests** - Comprehensive test suite
- **67% Coverage** - Good test coverage
- **Test Suites:**
  - ASA Linters (8 tests)
  - CLI Tool (13 tests)
  - MCP Server (4 tests)
  - Shared Utils (17 tests)

#### Documentation
- **README.md** - Main project documentation
- **GETTING_STARTED.md** - Comprehensive getting started guide
- **PROJECT_STRUCTURE.md** - Complete project structure overview
- **CONTRIBUTING.md** - Contributing guidelines
- **SECURITY.md** - Security policy
- **CHANGELOG.md** - This file
- **LICENSE** - MIT License

#### Development Tools
- **Devbox Support** - Nix-based development environment
- **Virtual Environment** - Standard Python venv support
- **Test Scripts** - Automated testing for both Devbox and venv
- **Cleanup Scripts** - Environment cleanup utilities

### Technical Details

#### Dependencies
- FastAPI >= 0.104.0
- Uvicorn >= 0.24.0
- Pydantic >= 2.5.0
- Click >= 8.1.0
- Jinja2 >= 3.1.0
- httpx >= 0.25.0

#### Development Dependencies
- pytest >= 7.4.0
- pytest-asyncio >= 0.21.0
- pytest-cov >= 4.1.0
- ruff >= 0.1.0
- mypy >= 1.7.0

#### Requirements
- Python 3.11+
- 4GB RAM minimum
- 500MB disk space

### Notes

#### MVP Limitations
- Mock JWT implementation (use python-jose in production)
- SHA256 password hashing (use bcrypt in production)
- No database (add PostgreSQL/MongoDB in production)
- No rate limiting (implement before production)

#### Known Issues
- None reported

---

## [Unreleased]

No unreleased changes yet.

---

## How to Update This Changelog

When making changes:

1. Add entry under `[Unreleased]` section
2. Use categories: Added, Changed, Deprecated, Removed, Fixed, Security
3. Include brief description and PR/issue number if applicable
4. When releasing, move `[Unreleased]` items to new version section

### Example

```markdown
## [Unreleased]

### Added
- New feature X (#123)

### Fixed
- Bug in feature Y (#124)
```

---

## Version History

- **v0.9.0** (2025-11-21) - Initial MVP release

---

**ASA Starter Kit**  
Copyright © 2025 Jan Voldán, VibeCodiq  
Licensed under the MIT License
