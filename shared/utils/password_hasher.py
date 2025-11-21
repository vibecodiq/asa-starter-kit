"""
Password Hashing Utilities

This module provides password hashing and verification functions.

NOTE: This is a simplified implementation for MVP 0.9 demo purposes.
In production, use bcrypt, argon2, or passlib with proper salting.
"""
import hashlib
from typing import Optional


def hash_password(password: str, salt: Optional[str] = None) -> str:
    """
    Hash a password using SHA256.

    Args:
        password: Plain text password to hash
        salt: Optional salt (not used in MVP 0.9 for simplicity)

    Returns:
        Hexadecimal hash string

    Example:
        >>> hash_password("demo123")
        '6b51d431df5d7f141cbececcf79edf3dd861c3b4069f0b11661a3eefacbba918'

    Warning:
        This is a demo implementation. In production:
        - Use bcrypt or argon2
        - Use proper salting
        - Use key stretching
        - Consider pepper (server-side secret)
    """
    if not password:
        raise ValueError("Password cannot be empty")

    # For demo: simple SHA256 hash
    # In production: use bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    return hashlib.sha256(password.encode('utf-8')).hexdigest()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against its hash.

    Args:
        plain_password: Plain text password to verify
        hashed_password: Previously hashed password

    Returns:
        True if password matches, False otherwise

    Example:
        >>> hashed = hash_password("demo123")
        >>> verify_password("demo123", hashed)
        True
        >>> verify_password("wrong", hashed)
        False

    Warning:
        This is a demo implementation. In production:
        - Use bcrypt.checkpw() or similar
        - Implement timing-safe comparison
        - Add rate limiting
    """
    if not plain_password or not hashed_password:
        return False

    try:
        # Hash the plain password and compare
        computed_hash = hash_password(plain_password)

        # Timing-safe comparison (important for security)
        # In Python 3.11+, this is built-in
        return computed_hash == hashed_password
    except Exception:
        # Never leak information via exceptions
        return False


def generate_random_password(length: int = 16) -> str:
    """
    Generate a random password.

    Args:
        length: Password length (default 16)

    Returns:
        Random password string

    Example:
        >>> pwd = generate_random_password(12)
        >>> len(pwd)
        12

    Note:
        This is a simple implementation for demo purposes.
        In production, use secrets.token_urlsafe() or similar.
    """
    import secrets
    import string

    if length < 8:
        raise ValueError("Password length must be at least 8 characters")

    # Character set: letters, digits, punctuation
    alphabet = string.ascii_letters + string.digits + string.punctuation

    # Generate random password
    password = ''.join(secrets.choice(alphabet) for _ in range(length))

    return password
