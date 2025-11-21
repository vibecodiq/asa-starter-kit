"""
Tests for login_demo slice
"""
import pytest
from httpx import ASGITransport, AsyncClient
from main import app


@pytest.mark.asyncio
async def test_successful_login():
    """Test successful login with valid credentials"""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post(
            "/api/v1/auth/login-demo",
            json={"email": "demo@vibecodiq.com", "password": "demo123"}
        )

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["user"]["email"] == "demo@vibecodiq.com"
    assert data["user"]["name"] == "Demo User"
    assert data["user"]["id"] == 1


@pytest.mark.asyncio
async def test_invalid_email():
    """Test login with non-existent email"""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post(
            "/api/v1/auth/login-demo",
            json={"email": "wrong@example.com", "password": "demo123"}
        )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"


@pytest.mark.asyncio
async def test_invalid_password():
    """Test login with wrong password"""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post(
            "/api/v1/auth/login-demo",
            json={"email": "demo@vibecodiq.com", "password": "wrongpassword"}
        )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"


@pytest.mark.asyncio
async def test_invalid_email_format():
    """Test login with invalid email format"""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post(
            "/api/v1/auth/login-demo",
            json={"email": "not-an-email", "password": "demo123"}
        )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_missing_password():
    """Test login with missing password"""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post(
            "/api/v1/auth/login-demo",
            json={"email": "demo@vibecodiq.com"}
        )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_missing_email():
    """Test login with missing email"""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post(
            "/api/v1/auth/login-demo",
            json={"password": "demo123"}
        )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_all_demo_users():
    """Test login with all demo users"""
    test_cases = [
        ("demo@vibecodiq.com", "demo123", "Demo User"),
        ("test@vibecodiq.com", "test456", "Test User"),
        ("admin@vibecodiq.com", "admin789", "Admin User"),
    ]

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        for email, password, expected_name in test_cases:
            response = await client.post(
                "/api/v1/auth/login-demo",
                json={"email": email, "password": password}
            )

            assert response.status_code == 200
            data = response.json()
            assert data["user"]["email"] == email
            assert data["user"]["name"] == expected_name


@pytest.mark.asyncio
async def test_list_demo_users():
    """Test listing demo users endpoint"""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/v1/auth/demo-users")

    assert response.status_code == 200
    data = response.json()
    assert "demo_users" in data
    assert len(data["demo_users"]) == 3
    assert "demo@vibecodiq.com" in data["demo_users"]
