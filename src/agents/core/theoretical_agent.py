from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
import json
import math
import numpy as np
from dataclasses import dataclass
from langchain.schema import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.tools import BaseTool, tool
from langchain.agents import AgentExecutor, create_openai_functions_agent, create_tool_calling_agent, AgentExecutor
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import PydanticOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field
from src.agents.base_agent import BaseAgent
from src.config import api_key
import os
from dotenv import load_dotenv

class HypothesisResponse(BaseModel):
    id: str
    statement: str
    confidence: float

class TheoreticalAgent(BaseAgent):
    def __init__(self, llm):
        super().__init__(
            name="TheoreticalAgent",
            llm=llm,
            response_model=HypothesisResponse,   # only pass model
            system_prompt="""You are the Theoretical Agent. Your role is to generate, refine, and explain scientific hypotheses and conceptual frameworks.
                            You propose theories, models, and predictions based on logical reasoning and prior knowledge.
                            You suggest testable hypotheses that the Experimental Agent can investigate.
                            You use mathematical, logical, or conceptual reasoning, but you do not run experiments yourself.
                            You critically evaluate whether experimental findings support or contradict theoretical claims.
                            Your outputs should be well-structured, with assumptions, predictions, and implications explicitly stated."""
        )
        self.tools = self._create_tools()

    def _create_tools(self) -> List[BaseTool]:
        """Create LangChain tools for hypothesis generation."""

        @tool
        def generate_hypothesis(topic: str, context: str = "") -> str:
            """Generate a new scientific hypothesis about a topic (with optional context)."""
            query = f"Generate a hypothesis about {topic}. Context: {context}"
            result = self.run(query=query)

            hypothesis_id = f"hyp_{datetime.now().strftime('%Y%m%d%H%M%S')}"
            return f"✅ {hypothesis_id}: {result}"

        @tool
        def revise_hypothesis(experiment_results: str, current_hypothesis: str = "") -> str:
            """Revise the current hypothesis based on experimental results."""
            query = (
                f"Revise the following hypothesis based on these experimental results.\n"
                f"Hypothesis: {current_hypothesis}\n"
                f"Experimental Results: {experiment_results}"
            )
            result = self.run(query=query)
            revised_id = f"rev_{datetime.now().strftime('%Y%m%d%H%M%S')}"
            return f"🔄 {revised_id}: {result}"

        return [generate_hypothesis, revise_hypothesis]


    def generate_hypothesis(self, topic: str, context: str = "") -> str:
        """Convenience method (direct call without agent executor)."""
        return self.run(query=f"Generate a hypothesis about {topic}. Context: {context}")
    def revise_hypothesis(self, experiment_results: str, current_hypothesis: str = "") -> str:
        """Convenience method to revise a hypothesis based on experimental results."""
        query = (
            f"Revise the following hypothesis based on these experimental results.\n"
            f"Hypothesis: {current_hypothesis}\n"
            f"Experimental Results: {experiment_results}"
        )
        return self.run(query=query)