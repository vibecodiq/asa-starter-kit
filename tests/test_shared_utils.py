"""
Tests for shared utilities
"""
import pytest
from shared.utils import (
    hash_password,
    verify_password,
    generate_random_password,
    create_access_token,
    decode_access_token,
    verify_token,
    get_token_subject,
)


class TestPasswordHasher:
    """Tests for password hashing utilities"""

    def test_hash_password(self):
        """Test password hashing"""
        password = "test_password_123"
        hashed = hash_password(password)

        assert hashed is not None
        assert len(hashed) == 64  # SHA256 produces 64 hex characters
        assert hashed != password  # Hash should be different from plain text

    def test_hash_password_consistency(self):
        """Test that same password produces same hash"""
        password = "consistent_password"
        hash1 = hash_password(password)
        hash2 = hash_password(password)

        assert hash1 == hash2

    def test_hash_password_empty(self):
        """Test that empty password raises error"""
        with pytest.raises(ValueError):
            hash_password("")

    def test_verify_password_correct(self):
        """Test password verification with correct password"""
        password = "correct_password"
        hashed = hash_password(password)

        assert verify_password(password, hashed) is True

    def test_verify_password_incorrect(self):
        """Test password verification with incorrect password"""
        password = "correct_password"
        hashed = hash_password(password)

        assert verify_password("wrong_password", hashed) is False

    def test_verify_password_empty(self):
        """Test password verification with empty inputs"""
        assert verify_password("", "hash") is False
        assert verify_password("password", "") is False

    def test_generate_random_password(self):
        """Test random password generation"""
        password = generate_random_password(16)

        assert len(password) == 16
        assert password.isascii()

    def test_generate_random_password_different(self):
        """Test that generated passwords are different"""
        pwd1 = generate_random_password(12)
        pwd2 = generate_random_password(12)

        assert pwd1 != pwd2

    def test_generate_random_password_min_length(self):
        """Test minimum password length validation"""
        with pytest.raises(ValueError):
            generate_random_password(4)  # Too short


class TestJWTService:
    """Tests for JWT token service"""

    def test_create_access_token(self):
        """Test token creation"""
        token = create_access_token({"sub": "test@example.com"})

        assert token is not None
        assert token.startswith("mock_jwt_token_")
        assert "test@example.com" in token

    def test_create_access_token_no_subject(self):
        """Test token creation without subject raises error"""
        with pytest.raises(ValueError):
            create_access_token({})

    def test_decode_access_token(self):
        """Test token decoding"""
        email = "user@example.com"
        token = create_access_token({"sub": email})
        payload = decode_access_token(token)

        assert payload["sub"] == email
        assert payload["valid"] is True
        assert "exp" in payload
        assert "expires_in" in payload

    def test_decode_invalid_token(self):
        """Test decoding invalid token raises error"""
        with pytest.raises(ValueError):
            decode_access_token("invalid_token")

    def test_verify_token_valid(self):
        """Test token verification with valid token"""
        token = create_access_token({"sub": "user@example.com"})
        assert verify_token(token) is True

    def test_verify_token_invalid(self):
        """Test token verification with invalid token"""
        assert verify_token("invalid_token") is False

    def test_get_token_subject(self):
        """Test extracting subject from token"""
        email = "user@example.com"
        token = create_access_token({"sub": email})
        subject = get_token_subject(token)

        assert subject == email

    def test_get_token_subject_invalid(self):
        """Test extracting subject from invalid token"""
        subject = get_token_subject("invalid_token")
        assert subject is None
