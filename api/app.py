from fastapi import FastAPI
from .routers import docs  # Import the docs router

app = FastAPI(
    title="IntelliDoc API",
    description="API service for generating and updating documentation.",
    version="0.1.0",
)

# Include the documentation generation routes
app.include_router(docs.router)

@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "ok"}
