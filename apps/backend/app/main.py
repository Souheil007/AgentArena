"""AgentArena API entry point."""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initializes database schema and background worker connections on startup."""
    await init_db()
    yield


app = FastAPI(
    title="AgentArena API",
    description="The Competitive AI Agent Colosseum & ELO Benchmark API",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", tags=["system"])
async def health_check():
    """Health status probe for the AgentArena cluster."""
    return {
        "status": "healthy",
        "service": "AgentArena",
        "env": settings.app_env,
        "database": "connected",
    }
