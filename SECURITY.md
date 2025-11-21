# Security Policy

## Supported Versions

We release patches for security vulnerabilities for the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 0.9.x   | :white_check_mark: |
| < 0.9   | :x:                |

---

## Reporting a Vulnerability

We take the security of the ASA Starter Kit seriously. If you discover a security vulnerability, please follow these steps:

### 1. **Do Not** Open a Public Issue

Please do not report security vulnerabilities through public GitHub issues, discussions, or pull requests.

### 2. Report Privately

Send an email to:

**jan@vibecodiq.com**

Include:
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

### 3. Response Timeline

- **Initial Response**: Within 48 hours
- **Status Update**: Within 7 days
- **Fix Timeline**: Depends on severity
  - Critical: Within 7 days
  - High: Within 14 days
  - Medium: Within 30 days
  - Low: Next release cycle

### 4. Disclosure Policy

- We will acknowledge receipt of your report
- We will investigate and validate the issue
- We will develop and test a fix
- We will release the fix and credit you (if desired)
- We will publicly disclose the vulnerability after the fix is released

---

## Security Best Practices

When using the ASA Starter Kit in production:

### 1. Authentication & Authorization

- **Never use demo credentials** in production
- Implement proper JWT token validation
- Use secure password hashing (bcrypt, argon2)
- Enable HTTPS/TLS for all endpoints

### 2. Dependencies

- Regularly update dependencies
- Run `pip audit` to check for vulnerabilities
- Use `dependabot` or similar tools

### 3. Environment Variables

- Never commit `.env` files
- Use environment-specific configurations
- Rotate secrets regularly

### 4. Database Security

- Use parameterized queries (prevent SQL injection)
- Implement proper access controls
- Enable database encryption at rest
- Regular backups

### 5. API Security

- Implement rate limiting
- Validate all input data
- Use CORS properly
- Enable API authentication

### 6. Code Security

- Run static analysis tools (ruff, mypy)
- Review dependencies for known vulnerabilities
- Follow OWASP Top 10 guidelines
- Regular security audits

---

## Known Limitations (MVP 0.9)

The current version is an MVP and has the following security limitations:

### ⚠️ Not Production-Ready

- **Mock JWT tokens**: Replace with `python-jose` or similar
- **SHA256 password hashing**: Replace with `bcrypt` or `argon2`
- **No rate limiting**: Implement before production
- **No input sanitization**: Add comprehensive validation
- **No HTTPS enforcement**: Configure in production
- **Mock database**: Replace with real database

### 🔒 Before Production Deployment

1. Replace all mock implementations
2. Add proper authentication/authorization
3. Implement rate limiting
4. Enable HTTPS/TLS
5. Add input validation and sanitization
6. Set up monitoring and logging
7. Conduct security audit
8. Implement backup strategy

---

## Security Updates

Security updates will be announced:

- GitHub Security Advisories
- Release notes
- Email to security@vibecodiq.com subscribers

To subscribe to security updates, email: jan@vibecodiq.com

---

## Acknowledgments

We appreciate the security research community and will acknowledge researchers who responsibly disclose vulnerabilities (with their permission).

---

## Contact

For security concerns:
- **Email**: jan@vibecodiq.com
- **Subject**: [SECURITY] Brief description

For general questions:
- **GitHub Issues**: [asa-starter-kit/issues](https://github.com/vibecodiq/asa-starter-kit/issues)

---

**ASA Starter Kit v0.9.0**  
Copyright © 2025 Jan Voldán, VibeCodiq  
Licensed under the MIT License

Thank you for helping keep ASA Starter Kit secure! 🔒
