from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from enum import Enum

from intellidoc.core import DocumentationTask, detect_language, Language

router = APIRouter(
    prefix="/docs",
    tags=["documentation"],
    responses={404: {"description": "Not found"}},
)


class LanguageEnum(str, Enum):
    """Supported languages for API."""
    PYTHON = "python"
    JAVASCRIPT = "javascript"
    TYPESCRIPT = "typescript"
    JAVA = "java"
    CPP = "cpp"
    CSHARP = "c_sharp"
    GO = "go"
    RUST = "rust"
    AUTO = "auto"


class DocGenerationRequest(BaseModel):
    """Request model for documentation generation."""
    code: str = Field(..., description="Source code to document")
    language: LanguageEnum = Field(LanguageEnum.AUTO, description="Programming language")
    filename: Optional[str] = Field(None, description="Filename (for auto language detection)")
    context: Optional[str] = Field(None, description="Additional context for generation")
    doc_type: str = Field("general", description="Type of documentation (general, api, tutorial)")


class DocGenerationResponse(BaseModel):
    """Response model for documentation generation."""
    documentation: str
    confidence_score: float
    strategy_used: str
    models_used: int
    total_tokens: int
    metadata: Dict[str, Any] = {}


@router.post("/generate", response_model=DocGenerationResponse)
async def generate_docs(request: DocGenerationRequest):
    """
    Generate documentation for provided code using multiple AI models.
    
    This endpoint uses IntelliDoc's multi-model collaboration system to produce
    high-quality documentation by leveraging multiple AI models working together.
    """
    from ..app import get_orchestrator
    
    orchestrator = get_orchestrator()
    
    # Determine language
    language = None
    if request.language != LanguageEnum.AUTO:
        try:
            language = Language(request.language.value)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Unsupported language: {request.language}")
    elif request.filename:
        language = detect_language(request.filename)
        if not language:
            raise HTTPException(status_code=400, detail="Could not detect language from filename")
    
    if not language:
        raise HTTPException(
            status_code=400,
            detail="Language must be specified or filename provided for auto-detection"
        )
    
    # Create documentation task
    task = DocumentationTask(
        code=request.code,
        language=language.value,
        context=request.context,
        doc_type=request.doc_type
    )
    
    try:
        # Generate documentation
        result = await orchestrator.generate_documentation(task)
        
        return DocGenerationResponse(
            documentation=result.final_documentation,
            confidence_score=result.confidence_score,
            strategy_used=result.strategy_used.value,
            models_used=len(result.contributions),
            total_tokens=result.metadata.get("total_tokens", 0),
            metadata={
                "models": [
                    {
                        "provider": c.provider.value,
                        "model": c.model,
                        "tokens": c.tokens_used
                    }
                    for c in result.contributions
                ]
            }
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Documentation generation failed: {str(e)}")


class BatchDocRequest(BaseModel):
    """Request for batch documentation generation."""
    files: List[DocGenerationRequest] = Field(..., description="List of files to document")


class BatchDocResponse(BaseModel):
    """Response for batch documentation generation."""
    results: List[DocGenerationResponse]
    total_files: int
    successful: int
    failed: int


@router.post("/batch", response_model=BatchDocResponse)
async def batch_generate(request: BatchDocRequest):
    """
    Generate documentation for multiple files in batch.
    
    This endpoint processes multiple files concurrently, making it efficient
    for documenting entire projects.
    """
    from ..app import get_orchestrator
    import asyncio
    
    orchestrator = get_orchestrator()
    
    async def process_one(file_request: DocGenerationRequest):
        try:
            return await generate_docs(file_request)
        except Exception as e:
            return {"error": str(e)}
    
    # Process all files concurrently
    results = await asyncio.gather(*[process_one(f) for f in request.files])
    
    # Separate successful from failed
    successful_results = [r for r in results if not isinstance(r, dict) or "error" not in r]
    
    return BatchDocResponse(
        results=successful_results,
        total_files=len(request.files),
        successful=len(successful_results),
        failed=len(request.files) - len(successful_results)
    )


@router.get("/languages")
async def list_languages():
    """List supported programming languages."""
    return {
        "languages": [lang.value for lang in Language],
        "auto_detection": True
    }


@router.get("/strategies")
async def list_strategies():
    """List available collaboration strategies."""
    from intellidoc.core import CollaborationStrategy
    
    return {
        "strategies": [
            {
                "name": strategy.value,
                "description": _get_strategy_description(strategy)
            }
            for strategy in CollaborationStrategy
        ]
    }


def _get_strategy_description(strategy) -> str:
    """Get description for a collaboration strategy."""
    descriptions = {
        "consensus": "All models generate documentation, outputs are intelligently merged",
        "specialization": "Different models handle different aspects (overview, technical, examples)",
        "review": "Primary model generates, others review and improve",
        "voting": "Models generate independently, best output is selected"
    }
    return descriptions.get(strategy.value, "")
