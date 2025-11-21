# Slice: auth/login_demo

## Metadata
- **Domain:** auth
- **Version:** 1.0.0
- **Estimated LOC:** 250

## 1. Goal
Provide a demo authentication endpoint with mock user data for testing ASA architecture.

## 2. User Story
- **As a** developer
- **I want** to test ASA architecture with a working login endpoint
- **So that** I can understand how slices work before building real features

## 3. Functional Requirements
- **[FR1]** Accept email and password via POST request
- **[FR2]** Validate credentials against hardcoded demo users
- **[FR3]** Return JWT token on successful authentication
- **[FR4]** Return 401 error on invalid credentials
- **[FR5]** Return 422 error on validation errors

## 4. API Contract

### Endpoint
```http
POST /api/v1/auth/login-demo
Content-Type: application/json

Request:
{
  "email": "demo@vibecodiq.com",
  "password": "demo123"
}

Response (200):
{
  "access_token": "mock_jwt_token_demo@vibecodiq.com_1234567890",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "email": "demo@vibecodiq.com",
    "name": "Demo User",
    "is_active": true
  }
}

Response (401):
{
  "detail": "Invalid credentials"
}

Response (422):
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "value is not a valid email address",
      "type": "value_error.email"
    }
  ]
}
```

## 5. Technical Design
- **Handler:** `LoginDemoHandler` – FastAPI route, validates request, calls service
- **Service:** `LoginDemoService` – business logic, checks credentials
- **Repository:** `DemoUserRepository` – mock data access (hardcoded users)
- **Schemas:** `LoginRequest`, `LoginResponse`

## 6. Dependencies
- **Shared:** `User` entity, `password_hasher`, `jwt_service`
- **External:** `fastapi`, `pydantic`

## 7. Acceptance Criteria
- **[AC1]** Valid credentials return 200 + token
- **[AC2]** Invalid email returns 401
- **[AC3]** Invalid password returns 401
- **[AC4]** Missing fields return 422
- **[AC5]** Token format is correct
- **[AC6]** Response time < 100ms

## 8. Test Cases
- **[TC1]** Successful login with demo@vibecodiq.com
- **[TC2]** Failed login with wrong email
- **[TC3]** Failed login with wrong password
- **[TC4]** Validation error with invalid email format
- **[TC5]** Validation error with missing password
