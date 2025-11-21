# Shared Modules Changelog

All notable changes to shared modules will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.1.0] - 2025-11-21

### Added
- `User` entity with email validation
- `UserInDB` entity with password hash
- `UserCreate` and `UserUpdate` schemas
- `hash_password()` utility function
- `verify_password()` utility function
- `generate_random_password()` utility function
- `create_access_token()` JWT utility
- `decode_access_token()` JWT utility
- `verify_token()` JWT utility
- `get_token_subject()` JWT utility
- Comprehensive unit tests for all utilities

### Notes
- Password hashing uses SHA256 (demo only, use bcrypt in production)
- JWT tokens are mock implementation (use python-jose in production)
- All utilities have docstrings and examples

## [1.0.0] - 2025-11-21

### Added
- Project initialization
- Basic directory structure
- CHANGELOG.md file

---

## How to Update This Changelog

When modifying shared modules:

1. **Document the change** in `slice.spec.md`
2. **Get review approval** (manual in MVP 0.9)
3. **Update this CHANGELOG**:
   ```markdown
   ## [X.Y.Z] - YYYY-MM-DD
   ### Added/Changed/Deprecated/Removed/Fixed/Security
   - Description of change
   - Added by: domain/slice_name
   ```
4. **Run tests** on affected slices

---

## Change Categories

- **Added**: New features
- **Changed**: Changes in existing functionality
- **Deprecated**: Soon-to-be removed features
- **Removed**: Removed features
- **Fixed**: Bug fixes
- **Security**: Security fixes

---

**ASA Starter Kit v0.9.0**  
Copyright © 2025 Jan Voldán, VibeCodiq  
Licensed under the MIT License
