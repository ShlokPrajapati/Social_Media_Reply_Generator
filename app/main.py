"""
Main application entry point for the Social Media Reply Generator API.
"""
import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from contextlib import asynccontextmanager

from app.api.routes import router
from app.db.database import Database
from app.config import API_TITLE, API_DESCRIPTION, API_VERSION, DEBUG


# Configure logging
logging.basicConfig(
    level=logging.DEBUG if DEBUG else logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    await Database.connect()
    yield
    # Shutdown logic
    await Database.close()
# Create FastAPI application
app = FastAPI(
    title=API_TITLE,
    description=API_DESCRIPTION,
    version=API_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan  # Attach the lifespan function here
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this to specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router, prefix="/api")


# @app.on_event("startup")
# async def startup_event():
#     """Execute actions on application startup."""
#     # Connect to MongoDB
#     await Database.connect()


# @app.on_event("shutdown")
# async def shutdown_event():
#     """Execute actions on application shutdown."""
#     # Close MongoDB connection
#     await Database.close()


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler for unhandled exceptions."""
    # Log the error
    logging.error(f"Unhandled exception: {exc}", exc_info=True)
    
    # Return a generic error response
    return JSONResponse(
        status_code=500,
        content={
            "detail": "An unexpected error occurred",
            "code": "internal_server_error"
        }
    )


@app.get("/")
def root():
    """Root endpoint that confirms the API is running."""
    return {
        "message": "Social Media Reply Generator API is running!",
        "docs": "/docs",
        "api_prefix": "/api"
    }


# if __name__ == "__main__":
#     uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=DEBUG)