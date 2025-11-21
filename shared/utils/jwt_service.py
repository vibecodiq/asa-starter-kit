"""
JWT Token Service

This module provides JWT token creation and validation.

NOTE: This is a mock implementation for MVP 0.9 demo purposes.
In production, use python-jose or PyJWT with proper signing.
"""
from datetime import datetime, timedelta
from typing import Dict, Any, Optional


# Mock secret key (in production, use environment variable)
SECRET_KEY = "mock_secret_key_for_demo_only_do_not_use_in_production"
ALGORITHM = "HS256"  # Not actually used in mock implementation
ACCESS_TOKEN_EXPIRE_HOURS = 24


def create_access_token(
    data: Dict[str, Any],
    expires_delta: Optional[timedelta] = None
) -> str:
    """
    Create a JWT access token.

    Args:
        data: Dictionary with token payload (must include 'sub' for subject/user)
        expires_delta: Optional expiration time delta

    Returns:
        JWT token string

    Example:
        >>> token = create_access_token({"sub": "user@example.com"})
        >>> "mock_jwt_token" in token
        True

    Warning:
        This is a MOCK implementation for demo purposes.
        In production:
        - Use python-jose: jose.jwt.encode()
        - Use proper signing with RS256 or HS256
        - Store secret in environment variables
        - Implement token refresh mechanism
    """
    if not data or "sub" not in data:
        raise ValueError("Token data must include 'sub' (subject)")

    # Calculate expiration
    if expires_delta is None:
        expires_delta = timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)

    expire = datetime.utcnow() + expires_delta
    expire_timestamp = int(expire.timestamp())

    # Extract subject (user identifier)
    subject = data.get("sub", "unknown")

    # Mock token format: "mock_jwt_token_{subject}_{timestamp}"
    # In production, this would be: jose.jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    token = f"mock_jwt_token_{subject}_{expire_timestamp}"

    return token


def decode_access_token(token: str) -> Dict[str, Any]:
    """
    Decode and validate a JWT token.

    Args:
        token: JWT token string

    Returns:
        Dictionary with token payload

    Raises:
        ValueError: If token is invalid or expired

    Example:
        >>> token = create_access_token({"sub": "user@example.com"})
        >>> payload = decode_access_token(token)
        >>> payload["sub"]
        'user@example.com'
        >>> payload["valid"]
        True

    Warning:
        This is a MOCK implementation for demo purposes.
        In production:
        - Use python-jose: jose.jwt.decode()
        - Verify signature
        - Check expiration
        - Validate issuer/audience
    """
    if not token or not token.startswith("mock_jwt_token_"):
        raise ValueError("Invalid token format")

    try:
        # Parse mock token: "mock_jwt_token_{subject}_{timestamp}"
        parts = token.split("_")

        if len(parts) < 4:
            raise ValueError("Invalid token structure")

        # Extract subject (skip "mock", "jwt", "token" parts)
        subject = "_".join(parts[3:-1])  # Handle emails with underscores
        expire_timestamp = int(parts[-1])

        # Check expiration
        current_timestamp = int(datetime.utcnow().timestamp())
        is_expired = current_timestamp > expire_timestamp

        if is_expired:
            raise ValueError("Token has expired")

        # Return payload
        return {
            "sub": subject,
            "exp": expire_timestamp,
            "valid": True,
            "expires_in": expire_timestamp - current_timestamp
        }

    except (ValueError, IndexError) as e:
        raise ValueError(f"Token validation failed: {str(e)}")


def verify_token(token: str) -> bool:
    """
    Quick token validation check.

    Args:
        token: JWT token string

    Returns:
        True if token is valid, False otherwise

    Example:
        >>> token = create_access_token({"sub": "user@example.com"})
        >>> verify_token(token)
        True
        >>> verify_token("invalid_token")
        False
    """
    try:
        payload = decode_access_token(token)
        return payload.get("valid", False)
    except Exception:
        return False


def get_token_subject(token: str) -> Optional[str]:
    """
    Extract subject (user identifier) from token.

    Args:
        token: JWT token string

    Returns:
        Subject string or None if invalid

    Example:
        >>> token = create_access_token({"sub": "user@example.com"})
        >>> get_token_subject(token)
        'user@example.com'
    """
    try:
        payload = decode_access_token(token)
        return payload.get("sub")
    except Exception:
        return None
