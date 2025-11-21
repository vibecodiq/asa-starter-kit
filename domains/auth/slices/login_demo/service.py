"""
Login Demo Service
"""
from typing import Optional
from .schemas import LoginRequest, LoginResponse
from .repository import DemoUserRepository
from shared.utils import verify_password, create_access_token
from shared.entities import User


class LoginDemoService:
    """
    Login demo business logic.

    Handles authentication flow:
    1. Validate user exists
    2. Verify password
    3. Generate JWT token
    4. Return response
    """

    def __init__(self):
        self.repository = DemoUserRepository()

    async def authenticate(self, request: LoginRequest) -> Optional[LoginResponse]:
        """
        Authenticate user and return token.

        Args:
            request: Login request with email and password

        Returns:
            LoginResponse if authentication successful, None otherwise

        Raises:
            None - returns None on failure instead of raising exceptions
        """
        # Get user from repository
        user_in_db = await self.repository.get_by_email(request.email)
        if not user_in_db:
            return None

        # Check if user is active
        if not user_in_db.is_active:
            return None

        # Verify password
        if not verify_password(request.password, user_in_db.password_hash):
            return None

        # Create access token
        access_token = create_access_token(data={"sub": user_in_db.email})

        # Create user response (without password hash)
        user = User(
            id=user_in_db.id,
            email=user_in_db.email,
            name=user_in_db.name,
            is_active=user_in_db.is_active,
            created_at=user_in_db.created_at
        )

        # Return response
        return LoginResponse(
            access_token=access_token,
            token_type="bearer",
            user=user
        )

    def get_demo_users(self) -> list[str]:
        """
        Get list of demo user emails (for documentation).

        Returns:
            List of email addresses
        """
        return self.repository.list_demo_users()
