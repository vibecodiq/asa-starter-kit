"""
Login Demo Handler
"""
from fastapi import APIRouter, HTTPException, status
from .schemas import LoginRequest, LoginResponse
from .service import LoginDemoService

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])
service = LoginDemoService()


@router.post("/login-demo", response_model=LoginResponse, status_code=status.HTTP_200_OK)
async def login_demo(request: LoginRequest):
    """
    Demo login endpoint with mock authentication.

    This endpoint demonstrates ASA slice architecture with:
    - Mock user data (no real database)
    - Password verification
    - JWT token generation

    **Test credentials:**
    - Email: `demo@vibecodiq.com`, Password: `demo123`
    - Email: `test@vibecodiq.com`, Password: `test456`
    - Email: `admin@vibecodiq.com`, Password: `admin789`

    **Returns:**
    - 200: Successful authentication with JWT token
    - 401: Invalid credentials
    - 422: Validation error (invalid email format, missing fields)
    """
    result = await service.authenticate(request)

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    return result


@router.get("/demo-users", tags=["auth"])
async def list_demo_users():
    """
    List available demo users (for testing purposes).

    **Returns:**
    - List of demo user email addresses
    """
    return {
        "demo_users": service.get_demo_users(),
        "note": "Use these emails with their respective passwords for testing"
    }
