from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
import json
import math
import numpy as np
from dataclasses import dataclass
from langchain.schema import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.tools import BaseTool
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from pydantic import BaseModel, Field
from src.agents.base_agent import BaseAgent
from src.config import api_key
import os
from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_tool_calling_agent, AgentExecutor
#from tools import search_tool, wiki_tool, save_tool
from langchain_google_genai import ChatGoogleGenerativeAI
#the pydantic model
#from src.schemas import ResearchResponse

from typing import List
from langchain.tools import tool
from langchain.tools.base import BaseTool
from datetime import datetime
from pydantic import BaseModel
from langchain_core.output_parsers import PydanticOutputParser
from src.agents.base_agent import BaseAgent

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
            system_prompt="You are a theoretical scientist. Generate hypotheses and models."
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

        return [generate_hypothesis]

    def generate_hypothesis(self, topic: str, context: str = "") -> str:
        """Convenience method (direct call without agent executor)."""
        return self.run(query=f"Generate a hypothesis about {topic}. Context: {context}")