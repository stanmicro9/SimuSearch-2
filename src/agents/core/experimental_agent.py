from src.agents.base_agent import BaseAgent

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
            system_prompt="""You are the Experimental Agent. Your role is to test and validate ideas through empirical methods, simulated experiments, and available tools.
                            You design and run experiments (real, simulated, or computational) to collect evidence.
                            You report clear results, including methodology, tools used, data collected, and observations.
                            You do not speculate beyond what your experimental evidence supports.
                            Your goal is to provide grounded, reproducible findings that can confirm, refine, or refute theoretical claims.
                            Always return your results in a structured, precise format, with sources, data, and limitations."""
        )

    def design_experiment(self, hypothesis: str):
        """Design an experiment to test a given hypothesis."""
        return self.run(query=f"Design an experiment to test: {hypothesis}")

    def run_simulation(self, experiment_description: str):
        """Run a simulation or computational experiment and return the results."""
        return self.run(query=f"Run a simulation for the following experiment: {experiment_description}")