"""
Demo User Repository (Mock Data)
"""
from typing import Optional
from shared.entities import UserInDB
from shared.utils import hash_password


class DemoUserRepository:
    """
    Mock user repository with hardcoded demo users.

    In production, this would query a real database (SQLAlchemy, etc.).
    For MVP 0.9, we use hardcoded data for simplicity.
    """

    # Hardcoded demo users
    _users = {
        "demo@vibecodiq.com": UserInDB(
            id=1,
            email="demo@vibecodiq.com",
            name="Demo User",
            is_active=True,
            password_hash=hash_password("demo123")
        ),
        "test@vibecodiq.com": UserInDB(
            id=2,
            email="test@vibecodiq.com",
            name="Test User",
            is_active=True,
            password_hash=hash_password("test456")
        ),
        "admin@vibecodiq.com": UserInDB(
            id=3,
            email="admin@vibecodiq.com",
            name="Admin User",
            is_active=True,
            password_hash=hash_password("admin789")
        ),
    }

    async def get_by_email(self, email: str) -> Optional[UserInDB]:
        """
        Get user by email address.

        Args:
            email: User email address

        Returns:
            UserInDB if found, None otherwise
        """
        return self._users.get(email.lower())

    async def get_by_id(self, user_id: int) -> Optional[UserInDB]:
        """
        Get user by ID.

        Args:
            user_id: User ID

        Returns:
            UserInDB if found, None otherwise
        """
        for user in self._users.values():
            if user.id == user_id:
                return user
        return None

    def list_demo_users(self) -> list[str]:
        """
        List all demo user emails (for documentation/testing).

        Returns:
            List of email addresses
        """
        return list(self._users.keys())
