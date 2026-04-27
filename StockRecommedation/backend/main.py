"""FastAPI main application."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api.routes import router
from config.settings import settings
from utils.logger import logger

# Create FastAPI app
app = FastAPI(
    title="Stock Recommendation API",
    description="Agentic AI system for stock market analysis and recommendations",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(router)


@app.on_event("startup")
async def startup_event():
    """Startup event handler."""
    logger.info("Starting Stock Recommendation API")
    logger.info(f"Backend running on {settings.backend_host}:{settings.backend_port}")


@app.on_event("shutdown")
async def shutdown_event():
    """Shutdown event handler."""
    logger.info("Shutting down Stock Recommendation API")


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Stock Recommendation API",
        "version": "1.0.0",
        "docs": "/docs"
    }
