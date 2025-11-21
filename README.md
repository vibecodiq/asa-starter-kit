# ASA Starter Kit v0.9.0

🚀 **AI-Sliced Architecture Starter Kit** for AI-first development.

## What is ASA?

ASA (AI-Sliced Architecture) is an architecture pattern designed specifically for AI-first development. It provides:

- ✅ **Small, isolated slices** - Each feature is a self-contained unit
- ✅ **Explicit metadata** - AI-readable specs and contracts
- ✅ **Automatic validation** - Linters ensure architectural rules
- ✅ **AI-friendly structure** - Optimized for AI code generation

## Quick Start

### Option 1: With Devbox (Recommended)

```bash
# Install devbox: https://www.jetpack.io/devbox
curl -fsSL https://get.jetpack.io/devbox | bash

# Clone and start
git clone https://github.com/vibecodiq/asa-starter-kit.git
cd asa_starter_kit
devbox shell
python main.py
```

### Option 2: Without Devbox

```bash
# Clone repository
git clone https://github.com/vibecodiq/asa-starter-kit.git
cd asa_starter_kit

# Create virtual environment
python3.11 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start server
python main.py
```

## Verify Installation

```bash
# Main server should be running on http://localhost:8000
curl http://localhost:8000

# Expected response:
# {
#   "status": "ok",
#   "message": "ASA Starter Kit v0.9.0",
#   "version": "0.9.0"
# }

# To generate new slices, start MCP server (in another terminal):
asa mcp-server start
# MCP server runs on http://localhost:8001
```

## Project Structure

```
asa_starter_kit/
├── domains/              # Domain slices
│   └── auth/
│       └── slices/
│           └── login_demo/  # Demo authentication slice
├── shared/               # Shared modules
│   ├── entities/         # Shared data models
│   ├── value_objects/    # Value objects
│   └── utils/            # Utility functions
├── orchestrator/         # ASA tooling
│   ├── asa_lints/        # Architectural linters
│   └── cli.py            # CLI tool
├── mcp_server/           # MCP server for slice generation
└── main.py               # FastAPI entry point
```

## Next Steps

1. **Explore Demo Slice**: Check out `domains/auth/slices/login_demo/`
2. **Read Documentation**: See [GETTING_STARTED.md](GETTING_STARTED.md)
3. **Try ASA CLI**: Run `asa --help`
4. **Create Your First Slice**: Use `asa generate-slice`

## Documentation

- 📖 [Getting Started Guide](GETTING_STARTED.md)
- 📋 [Project Structure](PROJECT_STRUCTURE.md)
- 📝 [Shared Modules Changelog](shared/CHANGELOG.md)
- 🤝 [Contributing Guidelines](CONTRIBUTING.md)
- 🔒 [Security Policy](SECURITY.md)

## Requirements

- Python 3.11+
- (Optional) Devbox for easier environment management

## Features

### ✅ Implemented (MVP 0.9)

- Demo authentication slice
- ASA linter engine (4 linters)
- CLI tool (`asa` command)
- MCP server for slice generation
- Complete documentation

## Support

- **Documentation**: See documentation files above
- **Issues**: [GitHub Issues](https://github.com/vibecodiq/asa-starter-kit/issues)
- **Email**: jan@vibecodiq.com

## License

MIT License - See [LICENSE](LICENSE) file for details.

---

**ASA Starter Kit v0.9.0**  
Copyright © 2025 Jan Voldán, VibeCodiq  
Licensed under the MIT License

Built with ❤️ for AI-first development
