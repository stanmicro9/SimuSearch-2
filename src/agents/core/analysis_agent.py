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
            system_prompt="You are a data analyst. Analyze experimental results and provide statistical insights."
        )

    def analyze_data(self, experiment_results: str) -> AnalysisResponse:
        query = f"Analyze the following experimental results and provide a summary and statistics.\nResults: {experiment_results}"
        return self.run(query=query)

    def visualize_results(self, experiment_results: str) -> str:
        query = f"Visualize the following experimental results.\nResults: {experiment_results}"
        return self.run(query=query)
