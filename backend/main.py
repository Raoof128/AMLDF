"""Main application entry point for AMLD-F."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from backend.api import attack, defend, detect, evaluate
from backend.utils.logger import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup/shutdown events."""
    logger.info("AMLD-F System Starting up...")
    yield
    logger.info("AMLD-F System Shutting down...")


app = FastAPI(
    title="Adversarial Machine Learning Defense Framework (AMLD-F)",
    description=(
        "A framework to detect, mitigate, simulate, and report adversarial attacks."
    ),
    version="1.0.0",
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(attack.router, prefix="/attack", tags=["attacks"])
app.include_router(detect.router, prefix="/detect", tags=["detection"])
app.include_router(defend.router, prefix="/defend", tags=["defense"])
app.include_router(evaluate.router, prefix="/evaluate", tags=["evaluation"])


@app.get("/health")
async def health_check():
    """Return system health status."""
    return {"status": "healthy", "version": "1.0.0"}


# Mount Frontend (MUST be last to avoid shadowing API routes)
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
