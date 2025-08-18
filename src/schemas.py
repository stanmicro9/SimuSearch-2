# from pydantic import BaseModel
# from typing import List

# class ResearchResponse(BaseModel):
#     topic: str
#     summary: str
#     sources: List[str]
#     tools_used: List[str]

from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime
import json

class HypothesisResponse(BaseModel):
    """Enhanced hypothesis response with domain information"""
    id: str = Field(description="Unique identifier for the hypothesis")
    statement: str = Field(description="The hypothesis statement")
    confidence: float = Field(description="Confidence level (0-1)", ge=0.0, le=1.0)
    mathematical_model: Optional[str] = Field(description="Mathematical representation if applicable")
    variables: List[str] = Field(default=[], description="Key variables involved")
    domain: Optional[str] = Field(description="Scientific domain", default="general")
    theoretical_basis: Optional[str] = Field(description="Theoretical foundation", default="")
    literature_support: Optional[List[str]] = Field(description="Supporting literature", default=[])

class ExperimentDesign(BaseModel):
    """Enhanced experiment design with validation"""
    experiment_id: str = Field(description="Unique experiment identifier")
    hypothesis_id: str = Field(description="Reference to the hypothesis being tested")
    parameters: Dict[str, Any] = Field(description="Experimental parameters")
    setup: str = Field(description="Experimental setup description")
    measurements: List[str] = Field(description="What to measure")
    expected_outcome: str = Field(description="Expected experimental outcome")
    tools_required: List[str] = Field(description="Required experimental tools")
    control_variables: Optional[List[str]] = Field(description="Variables to control", default=[])
    duration: Optional[float] = Field(description="Experiment duration", default=60.0)
    sample_size: Optional[int] = Field(description="Number of samples", default=5)

class ExperimentalResults(BaseModel):
    """Enhanced experimental results with statistical information"""
    experiment_id: str
    raw_data: Dict[str, List[float]]
    analysis: str
    conclusion: str
    supports_hypothesis: bool
    confidence: float = Field(ge=0.0, le=1.0)
    statistical_significance: Optional[float] = Field(description="P-value or significance measure", default=None)
    effect_size: Optional[float] = Field(description="Magnitude of observed effect", default=None)
    limitations: Optional[List[str]] = Field(description="Experimental limitations", default=[])

class FinalAnalysis(BaseModel):
    """Comprehensive final analysis of the scientific investigation"""
    scientific_question: str
    hypothesis: HypothesisResponse
    experiment_design: ExperimentDesign
    experimental_results: ExperimentalResults
    theoretical_vs_experimental: str
    final_conclusion: str
    future_research: List[str]
    methodology_assessment: Optional[str] = Field(description="Assessment of methods used", default="")
    confidence_level: Optional[str] = Field(description="Overall confidence in findings", default="moderate")
    practical_implications: Optional[List[str]] = Field(description="Real-world applications", default=[])

class CommunicationMessage(BaseModel):
    """Standard message format for agent communication"""
    from_agent: str
    to_agent: str
    message_type: str
    content: Dict[str, Any]
    timestamp: str
    priority: Optional[str] = Field(description="Message priority", default="normal")