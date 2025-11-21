# Getting Started with the ASA Starter Kit

This guide will walk you through setting up and using the ASA Starter Kit v0.9.0.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [First Steps](#first-steps)
4. [Understanding ASA](#understanding-asa)
5. [Using the CLI](#using-the-cli)
6. [Creating Your First Slice](#creating-your-first-slice)
7. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required

- **Python 3.11 or higher**
  ```bash
  python --version  # Should show 3.11.x or higher
  ```
- **Git** - For cloning the repository
- **4GB RAM minimum** - For running the development server
- **500MB disk space** - For dependencies and virtual environment

### Optional but Recommended

- **Devbox** - For easier environment management
  ```bash
  curl -fsSL https://get.jetpack.io/devbox | bash
  ```
- **curl** or **httpie** - For testing API endpoints
- **VS Code** or **PyCharm** - Recommended IDEs

---

## Installation

### Step 1: Clone Repository

```bash
git clone https://github.com/vibecodiq/asa-starter-kit.git
cd asa_starter_kit
```

### Step 2: Setup Environment

#### Option A: With Devbox (Recommended)

```bash
devbox shell
```

This will:
- Install Python 3.11
- Create virtual environment
- Install all dependencies
- Set up environment variables

#### Option B: Without Devbox

```bash
# Create virtual environment
python3.11 -m venv .venv

# Activate virtual environment
source .venv/bin/activate  # Linux/macOS
# OR
.venv\Scripts\activate     # Windows

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Verify Installation

```bash
# Check Python version
python --version

# Check installed packages
pip list

# Verify ASA CLI
asa --help
```

---

## First Steps

### Start the Main Server

```bash
python main.py
```

You should see:

```
============================================================
ASA Starter Kit v0.9.0
============================================================
Starting server...
API Documentation: http://localhost:8000/docs
Health Check: http://localhost:8000/health
============================================================
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Start the MCP Server (Optional)

The MCP server is needed for generating new slices with `asa generate-slice`.

**In a new terminal:**

```bash
# Activate environment first (if using venv)
source .venv/bin/activate

# Start MCP server
asa mcp-server start
```

You should see:

```
🚀 Starting MCP server on port 8001...
Starting MCP Server on port 8001...
INFO:     Uvicorn running on http://0.0.0.0:8001
```

**Note:** You only need the MCP server running when generating new slices. For normal development and testing, only the main server (port 8000) is required.

### Test the API

Open your browser and visit:

- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

Or use curl:

```bash
# Root endpoint
curl http://localhost:8000

# Health check
curl http://localhost:8000/health
```

### Test Demo Slice (After Task 3)

```bash
curl -X POST http://localhost:8000/api/v1/auth/login-demo \
  -H "Content-Type: application/json" \
  -d '{
    "email": "demo@vibecodiq.com",
    "password": "demo123"
  }'
```

Expected response:

```json
{
  "access_token": "mock_jwt_token_demo@vibecodiq.com_1234567890",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "email": "demo@vibecodiq.com",
    "name": "Demo User",
    "is_active": true
  }
}
```

---

## Understanding ASA

### What is a Slice?

A **slice** is the smallest unit of functionality in ASA. Each slice:

- Has a single purpose
- Is completely isolated
- Has explicit metadata
- Can be implemented by AI

### Slice Structure

```
domains/auth/slices/login_demo/
├── slice.spec.md          # Functional specification
├── slice.contract.json    # API contract & dependencies
├── handler.py             # FastAPI route handler
├── service.py             # Business logic
├── repository.py          # Data access
├── schemas.py             # Pydantic models
└── tests/
    └── test_slice.py      # Tests
```

### Key Files

#### slice.spec.md

Human-readable specification with:
- Goal and user story
- Functional requirements
- API contract
- Acceptance criteria
- Test cases

#### slice.contract.json

Machine-readable contract with:
- Slice name and version
- Allowed imports
- Public API exports
- Dependencies

---

## Using the CLI

### List All Slices

```bash
asa list-slices
```

Output:

```
Found 1 slice(s):
  - auth/login_demo
```

### Lint a Slice

```bash
asa lint domains/auth/slices/login_demo
```

Output:

```
✅ Structure: OK (all required files present)
✅ Contract: OK (all required fields present)
✅ LOC limits: OK (within limits)
✅ Imports: OK (all imports allowed)

Result: PASSED
```

### Lint All Slices

```bash
asa lint-all
```

### Generate New Slice

**Prerequisites:** MCP server must be running (see "Start the MCP Server" above)

```bash
asa generate-slice \
  --func-spec "User registration with email verification" \
  --domain auth \
  --slice-name register
```

This will:
1. Generate `slice.spec.md`
2. Generate `slice.contract.json`
3. Create skeleton files
4. Run linter to verify

**Note:** If you get a connection error, make sure the MCP server is running on port 8001.

---

## Creating Your First Slice

### Step 1: Plan Your Slice

Define:
- **Domain**: Which domain does it belong to? (e.g., `auth`, `users`, `posts`)
- **Slice name**: What is it called? (e.g., `register`, `update_profile`)
- **Purpose**: What does it do? (1-2 sentences)

### Step 2: Start MCP Server

**In a separate terminal:**

```bash
asa mcp-server start
```

Keep this running while generating slices.

### Step 3: Generate Skeleton

```bash
asa generate-slice \
  --func-spec "Your feature description here" \
  --domain your_domain \
  --slice-name your_slice_name
```

### Step 4: Review Generated Files

Check:
- `slice.spec.md` - Is the spec correct?
- `slice.contract.json` - Are dependencies correct?
- Skeleton files - Do they match your needs?

### Step 5: Implement Business Logic

Edit:
- `service.py` - Add your business logic
- `repository.py` - Add data access code
- `schemas.py` - Adjust models if needed

### Step 6: Write Tests

Edit `tests/test_slice.py`:

```python
@pytest.mark.asyncio
async def test_your_feature():
    # Your test here
    pass
```

### Step 7: Run Tests

```bash
pytest domains/your_domain/slices/your_slice_name/tests/
```

### Step 8: Lint Your Slice

```bash
asa lint domains/your_domain/slices/your_slice_name
```

### Step 9: Register in main.py

```python
from domains.your_domain.slices.your_slice_name import router as your_router

app.include_router(your_router)
```

---

## Troubleshooting

### Server Won't Start

**Problem**: `ModuleNotFoundError` or import errors

**Solution**:
```bash
# Ensure you're in the project root
pwd

# Reinstall dependencies
pip install -r requirements.txt

# Check Python version
python --version  # Must be 3.11+
```

### Linter Errors

**Problem**: `asa lint` reports errors

**Solution**:
```bash
# Check which files are missing
ls domains/auth/slices/login_demo/

# Verify contract.json format
cat domains/auth/slices/login_demo/slice.contract.json | python -m json.tool
```

### Tests Failing

**Problem**: `pytest` shows failures

**Solution**:
```bash
# Run tests with verbose output
pytest -v

# Run specific test
pytest domains/auth/slices/login_demo/tests/test_slice.py::test_successful_login

# Check test coverage
pytest --cov
```

### Import Errors

**Problem**: Cannot import shared modules

**Solution**:
```bash
# Ensure PYTHONPATH is set
export PYTHONPATH=.

# Or run from project root
cd /path/to/asa_starter_kit
python main.py
```

---

## Next Steps

1. ✅ Explore the demo slice in `domains/auth/slices/login_demo/`
2. 📖 Read [Project Structure](PROJECT_STRUCTURE.md) for complete overview
3. 🔨 Create your first real slice using `asa generate-slice`
4. 🧪 Write comprehensive tests
5. 🚀 Deploy to production

---

## Getting Help

- **Documentation**: Check documentation files in the repository
- **Examples**: Study `domains/auth/slices/login_demo/`
- **Issues**: [Report bugs on GitHub](https://github.com/vibecodiq/asa-starter-kit/issues)
- **Email**: jan@vibecodiq.com

---

**ASA Starter Kit v0.9.0**  
Copyright © 2025 Jan Voldán, VibeCodiq  
Licensed under the MIT License - see [LICENSE](LICENSE) for details.

Happy coding with ASA! 🚀
