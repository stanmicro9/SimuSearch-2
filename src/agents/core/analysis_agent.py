from typing import Any
from pydantic import BaseModel, Field
from src.agents.base_agent import BaseAgent

class AnalysisResponse(BaseModel):
    summary: str
    statistics: dict
    confidence: float

class AnalysisAgent(BaseAgent):
    def __init__(self, llm):
        super().__init__(
            name="DataAnalysisAgent",
            llm=llm,
            response_model=AnalysisResponse,
            system_prompt="""You are the Analytical Agent. Your role is to evaluate, synthesize, and interpret the results from both the Experimental and Theoretical Agents.
                            You compare theoretical predictions with experimental results.
                            You highlight consistencies, contradictions, and uncertainties.
                            You suggest refinements: e.g., clarifying theoretical assumptions, designing better experiments, or improving analysis methods.
                            You produce summaries, insights, and recommendations for the next steps in research.
                            Always structure your analysis with:

                            1. Key Findings
                            2. Agreements/Contradictions
                            3. Limitations
                            4. Next Steps"""
        )

    def analyze_data(self, experiment_results: str) -> AnalysisResponse:
        query = f"Analyze the following experimental results and provide a summary and statistics.\nResults: {experiment_results}"
        return self.run(query=query)

    def visualize_results(self, experiment_results: str) -> str:
        query = f"Visualize the following experimental results.\nResults: {experiment_results}"
        return self.run(query=query)
