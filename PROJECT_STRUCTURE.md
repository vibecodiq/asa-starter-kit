# ASA Starter Kit - Project Structure

**Generated:** 2025-11-21  
**Version:** v0.9.0  
**Author:** Jan Voldán, VibeCodiq

## 📁 Complete Directory Structure

```
asa_starter_kit/
│
├── 📄 Configuration Files
│   ├── pyproject.toml              # Project metadata & dependencies
│   ├── requirements.txt            # Python dependencies
│   ├── devbox.json                 # Devbox environment config
│   ├── .gitignore                  # Git ignore rules
│   └── .gitattributes              # Git attributes
│
├── 📚 Documentation
│   ├── README.md                   # Main project documentation
│   ├── GETTING_STARTED.md          # Quick start guide
│   ├── PROJECT_STRUCTURE.md        # This file
│   ├── CONTRIBUTING.md             # Contributing guidelines
│   ├── SECURITY.md                 # Security policy
│   ├── CHANGELOG.md                # Project changelog
│   └── LICENSE                     # MIT License
│
├── 🚀 Main Application
│   └── main.py                     # FastAPI main server (port 8000)
│
├── 🌐 Domains (Business Logic)
│   ├── __init__.py
│   └── auth/                       # Authentication domain
│       ├── __init__.py
│       └── slices/
│           ├── __init__.py
│           ├── .gitkeep
│           └── login_demo/         # Demo login slice
│               ├── __init__.py
│               ├── handler.py      # FastAPI route handler
│               ├── service.py      # Business logic
│               ├── repository.py   # Data access layer
│               ├── schemas.py      # Pydantic models
│               ├── slice.spec.md   # Functional specification
│               ├── slice.contract.json  # API contract
│               └── tests/
│                   ├── __init__.py
│                   └── test_slice.py    # Slice tests
│
├── 🔧 Shared Modules
│   ├── __init__.py
│   ├── CHANGELOG.md
│   ├── entities/                   # Domain entities
│   │   ├── __init__.py
│   │   └── user.py                 # User entity
│   ├── utils/                      # Utility functions
│   │   ├── __init__.py
│   │   ├── jwt_service.py          # JWT token handling
│   │   └── password_hasher.py      # Password hashing
│   └── value_objects/              # Value objects
│       └── __init__.py
│
├── 🎯 Orchestrator (CLI & Linters)
│   ├── __init__.py
│   ├── cli.py                      # CLI tool (asa command)
│   └── asa_lints/                  # ASA Linter Engine
│       ├── __init__.py
│       ├── lint_slice_structure.py # Structure validator
│       ├── lint_contract_json.py   # Contract validator
│       ├── lint_loc_limits.py      # LOC limits checker
│       ├── lint_contract_imports.py # Import validator
│       └── run_asa_checks.py       # Linter orchestrator
│
├── 🤖 MCP Server (Slice Generator)
│   ├── __init__.py
│   ├── main.py                     # MCP FastAPI server (port 8001)
│   ├── handlers/                   # Generation handlers
│   │   ├── __init__.py
│   │   ├── generate_spec.py        # Generate slice.spec.md
│   │   ├── generate_contract.py    # Generate slice.contract.json
│   │   └── generate_skeleton.py    # Generate complete slice
│   └── templates/                  # Jinja2 templates
│       ├── .gitkeep
│       ├── slice.spec.md.j2        # Spec template
│       ├── slice.contract.json.j2  # Contract template
│       ├── handler.py.j2           # Handler template
│       ├── service.py.j2           # Service template
│       ├── repository.py.j2        # Repository template
│       ├── schemas.py.j2           # Schemas template
│       └── test_slice.py.j2        # Test template
│
├── 🧪 Tests
│   ├── __init__.py
│   ├── test_asa_linters.py         # Linter tests (8 tests)
│   ├── test_cli.py                 # CLI tests (13 tests)
│   ├── test_mcp_server.py          # MCP server tests (4 tests)
│   └── test_shared_utils.py        # Shared utils tests (17 tests)
│
└── 📦 Build Artifacts
    └── asa_starter_kit.egg-info/   # Package metadata
        ├── PKG-INFO
        ├── SOURCES.txt
        ├── dependency_links.txt
        ├── entry_points.txt
        ├── requires.txt
        └── top_level.txt
```

---

## 📊 Project Statistics

### Files by Type
- **Python files:** ~30 files
- **Templates:** 7 Jinja2 templates
- **Tests:** 42 tests total
- **Documentation:** 5 markdown files
- **Configuration:** 3 config files

### Lines of Code
- **Total:** ~1,014 statements
- **Test Coverage:** 67%
- **Domains:** 1 domain (auth)
- **Slices:** 1 slice (login_demo)

---

## 🎯 Key Components

### 1. Main Server (`main.py`)
- FastAPI application
- Port: 8000
- Routes: `/health`, `/docs`, `/api/v1/auth/login-demo`

### 2. MCP Server (`mcp_server/main.py`)
- FastAPI application
- Port: 8001
- Endpoints:
  - `POST /mcp/generate-spec`
  - `POST /mcp/generate-contract`
  - `POST /mcp/generate-skeleton`

### 3. CLI Tool (`orchestrator/cli.py`)
- Command: `asa`
- Subcommands:
  - `list-slices` - List all slices
  - `lint <path>` - Lint specific slice
  - `lint-all` - Lint all slices
  - `generate-slice` - Generate new slice
  - `mcp-server start` - Start MCP server

### 4. ASA Linters (`orchestrator/asa_lints/`)
- **Structure Linter:** Validates required files
- **Contract Linter:** Validates slice.contract.json
- **LOC Linter:** Checks line count limits
- **Imports Linter:** Validates import rules

### 5. Shared Modules (`shared/`)
- **Entities:** User entity
- **Utils:** JWT service, Password hasher
- **Value Objects:** (placeholder)

---

## 🔄 Typical Workflow

```bash
# 1. Start main server
python main.py

# 2. Start MCP server (in another terminal)
asa mcp-server start

# 3. List existing slices
asa list-slices

# 4. Generate new slice
asa generate-slice \
  --func-spec "User registration" \
  --domain auth \
  --slice-name register

# 5. Lint the new slice
asa lint domains/auth/slices/register

# 6. Run all tests
pytest -v
```

---

## 📝 File Naming Conventions

### Slices
- **Directory:** `domains/{domain}/slices/{slice_name}/`
- **Files:**
  - `slice.spec.md` - Functional specification
  - `slice.contract.json` - API contract
  - `handler.py` - FastAPI route handler
  - `service.py` - Business logic
  - `repository.py` - Data access
  - `schemas.py` - Pydantic models
  - `tests/test_slice.py` - Tests

### Python Classes
- **Handler:** `{SliceName}Handler` (CamelCase)
- **Service:** `{SliceName}Service` (CamelCase)
- **Repository:** `{SliceName}Repository` (CamelCase)
- **Request:** `{SliceName}Request` (CamelCase)
- **Response:** `{SliceName}Response` (CamelCase)

### Example
For slice `update_profile`:
- Class: `UpdateProfileHandler`
- Class: `UpdateProfileService`
- Class: `UpdateProfileRepository`
- Schema: `UpdateProfileRequest`
- Schema: `UpdateProfileResponse`

---

## 🚀 Technologies Used

- **Framework:** FastAPI 0.121.3
- **Server:** Uvicorn 0.38.0
- **Validation:** Pydantic 2.12.4
- **Templates:** Jinja2 3.1.6
- **CLI:** Click 8.3.1
- **HTTP Client:** httpx 0.28.1
- **Testing:** pytest 9.0.1
- **Linting:** ruff 0.14.5
- **Type Checking:** mypy 1.18.2

---

## 📦 Dependencies

### Core
- fastapi>=0.104.0
- uvicorn[standard]>=0.24.0
- pydantic>=2.5.0
- pydantic-settings>=2.1.0
- email-validator>=2.0.0
- python-multipart>=0.0.6
- httpx>=0.25.0
- click>=8.1.0
- jinja2>=3.1.0

### Development
- pytest>=7.4.0
- pytest-asyncio>=0.21.0
- pytest-cov>=4.1.0
- ruff>=0.1.0
- mypy>=1.7.0

---

## 🎯 ASA Architecture Principles

1. **Slice Independence:** Each slice is self-contained
2. **Contract-First:** API contracts define slice boundaries
3. **Layered Architecture:** Handler → Service → Repository
4. **Test Coverage:** Each slice has its own tests
5. **Linter Validation:** Automated checks for ASA compliance

---

---

## License & Credits

**ASA Starter Kit v0.9.0**  
Copyright © 2025 Jan Voldán, VibeCodiq  
Licensed under the MIT License - see [LICENSE](LICENSE) for details.

**Generated:** 2025-11-21  
**Status:** ✅ Complete & Functional

Built with ❤️ for AI-first development
