from src.agents.base_agent import BaseAgent
from src.schemas import ResearchResponse

from pydantic import BaseModel
from src.agents.base_agent import BaseAgent

# Schema for experimental responses
class ResearchResponse(BaseModel):
    topic: str
    summary: str
    sources: list[str]
    tools_used: list[str]

class ExperimentalAgent(BaseAgent):
    def __init__(self, llm):
        super().__init__(
            name="ExperimentalAgent",
            llm=llm,
            response_model=ResearchResponse,
            system_prompt="You are an experimental scientist. Design and analyze experiments."
        )

    def design_experiment(self, hypothesis: str):
        return self.run(query=f"Design an experiment to test: {hypothesis}")
