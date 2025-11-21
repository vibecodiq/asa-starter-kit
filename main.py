"""
ASA Starter Kit - Main FastAPI Application
MVP 0.9

This is the entry point for the ASA starter kit.
It includes the demo slice and provides health check endpoints.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

# Import slice routers
from domains.auth.slices.login_demo import router as login_demo_router

app = FastAPI(
    title="ASA Starter Kit",
    description="AI-Sliced Architecture - MVP 0.9",
    version="0.9.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS middleware - allow all origins for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include slice routers
app.include_router(login_demo_router)


@app.get("/")
async def root():
    """
    Root endpoint - health check

    Returns basic information about the API.
    """
    return {
        "status": "ok",
        "message": "ASA Starter Kit MVP 0.9",
        "version": "0.9.0",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health")
async def health():
    """
    Detailed health check endpoint

    Returns information about loaded slices and system status.
    """
    return {
        "status": "healthy",
        "version": "0.9.0",
        "slices": ["auth/login_demo"],
        "environment": "development"
    }


@app.exception_handler(404)
async def not_found_handler(request, exc):
    """Custom 404 handler"""
    return JSONResponse(
        status_code=404,
        content={
            "detail": "Endpoint not found",
            "path": str(request.url.path),
            "suggestion": "Visit /docs for API documentation"
        }
    )


if __name__ == "__main__":
    import uvicorn

    print("=" * 60)
    print("ASA Starter Kit MVP 0.9")
    print("=" * 60)
    print("Starting server...")
    print("API Documentation: http://localhost:8000/docs")
    print("Health Check: http://localhost:8000/health")
    print("=" * 60)

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
