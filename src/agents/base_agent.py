from langchain_core.exceptions import OutputParserException
import json
import re
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
class BaseAgent:
    def __init__(self, name, llm, response_model, system_prompt: str):
        self.name = name
        self.llm = llm
        self.parser = PydanticOutputParser(pydantic_object=response_model)

        self.prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt + "\n{format_instructions}"),
                ("placeholder", "{chat_history}"),
                ("human", "{query}"),
                ("placeholder", "{agent_scratchpad}"),
            ]
        ).partial(format_instructions=self.parser.get_format_instructions())

    def act(self, observations):
        raise NotImplementedError("Each agent must implement its own 'act' method.")
    
    def run(self, query: str, chat_history=None, agent_scratchpad=""):
        prompt = self.prompt.format_prompt(
            query=query,
            chat_history=chat_history or [],
            agent_scratchpad=agent_scratchpad or []
        )
        result = self.llm.invoke(prompt.to_messages())

        try:
            return self.parser.parse(result.content)
        except OutputParserException:
            # --- attempt a repair ---
            cleaned = self._repair_json(result.content)
            try:
                return self.parser.parse(cleaned)
            except Exception:
                # fallback if still broken
                return {"error": "Failed to parse", "raw": result.content}

    def _repair_json(self, text: str) -> str:
        """Try to salvage malformed JSON from LLM output."""
        # Extract JSON between braces
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            return match.group(0)
        return text.strip()
