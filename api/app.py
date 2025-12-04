from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from intellidoc import __version__
from intellidoc.core import load_config, validate_config, MultiModelOrchestrator
from .routers import docs

# Global orchestrator instance
orchestrator = None
config = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize and cleanup application resources."""
    global orchestrator, config
    
    # Load configuration
    config = load_config()
    
    if not validate_config(config):
        raise RuntimeError("Invalid configuration. Please check your API keys.")
    
    # Initialize orchestrator
    orchestrator = MultiModelOrchestrator(config.models, config.strategy)
    
    print(f"Initialized IntelliDoc API v{__version__}")
    print(f"Models: {len(config.models)}")
    print(f"Strategy: {config.strategy.value}")
    
    yield
    
    # Cleanup
    orchestrator = None
    config = None


app = FastAPI(
    title="IntelliDoc API",
    description="Multi-Model AI Documentation Generation API",
    version=__version__,
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(docs.router)


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": "IntelliDoc API",
        "version": __version__,
        "status": "operational",
        "models": len(config.models) if config else 0,
        "strategy": config.strategy.value if config else "unknown"
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    if orchestrator is None:
        raise HTTPException(status_code=503, detail="Service not initialized")
    
    return {
        "status": "healthy",
        "models": len(orchestrator.providers),
        "strategy": orchestrator.strategy.value
    }


def get_orchestrator() -> MultiModelOrchestrator:
    """Get the global orchestrator instance."""
    if orchestrator is None:
        raise HTTPException(status_code=503, detail="Orchestrator not initialized")
    return orchestrator
