#future enhancements
"""
Optional REST API server for the scientific investigation system
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.workflows.scientific_workflow import ScientificWorkflow
from src.config import Config
from langchain_google_genai import ChatGoogleGenerativeAI
import uvicorn

app = FastAPI(
    title="Scientific Investigation API",
    description="Multi-agent system for automated scientific investigations",
    version="1.0.0"
)

class InvestigationRequest(BaseModel):
    question: str
    domain: Optional[str] = None
    parameters: Optional[Dict[str, Any]] = None

class InvestigationResponse(BaseModel):
    question: str
    hypothesis: str
    experimental_results: str
    final_conclusion: str
    confidence: float
    future_research: List[str]

# Initialize workflow
llm = ChatGoogleGenerativeAI(
    model=Config.DEFAULT_LLM_MODEL,
    google_api_key=Config.GOOGLE_API_KEY
)
workflow = ScientificWorkflow(llm)

@app.post("/investigate", response_model=InvestigationResponse)
async def investigate_question(request: InvestigationRequest):
    """Endpoint to run scientific investigation"""
    
    try:
        result = workflow.investigate(request.question)
        
        return InvestigationResponse(
            question=result.scientific_question,
            hypothesis=result.hypothesis.statement,
            experimental_results=result.experimental_results.conclusion,
            final_conclusion=result.final_conclusion,
            confidence=result.experimental_results