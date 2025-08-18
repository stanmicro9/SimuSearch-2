# from agents.core.experimental_agent import ExperimentalAgent
# from agents.core.theoretical_agent import TheoreticalAgent
# # from environments.physics_lab import PhysicsLab
# from communication.protocol import CommunicationAgent
# # from experiments.pendulum_discovery import run_pendulum_experiment

# def main():
#     lab = PhysicsLab()

#     agent1 = ExperimentalAgent(name="ExpAgent-1")
#     agent2 = TheoreticalAgent(name="TheoAgent-1")

#     protocol = CommunicationAgent([agent1, agent2])

#     # 4. Run experiment
#     print("🔬 Starting Pendulum Discovery Experiment...")
#     run_pendulum_experiment(lab, [agent1, agent2], protocol)


# if __name__ == "__main__":
#     main()


# from agents.core.theoretical_agent import TheoreticalAgent

# def main():
#     lab = PhysicsLab()

#     agent1 = ExperimentalAgent(name="ExpAgent-1")
#     agent2 = TheoreticalAgent(name="TheoAgent-1")

#     protocol = CommunicationAgent([agent1, agent2])

#     # 4. Run experiment
#     print("🔬 Starting Pendulum Discovery Experiment...")
#     run_pendulum_experiment(lab, [agent1, agent2], protocol)


# if __name__ == "__main__":
#     main()





# import os
# from dotenv import load_dotenv
# from pydantic import BaseModel
# from langchain_openai import ChatOpenAI
# from langchain_anthropic import ChatAnthropic
# from langchain_core.prompts import ChatPromptTemplate
# from langchain_core.output_parsers import PydanticOutputParser
# from langchain.agents import create_tool_calling_agent, AgentExecutor
# #from tools import search_tool, wiki_tool, save_tool
# from langchain_google_genai import ChatGoogleGenerativeAI

# load_dotenv()
# llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")

# class ResearchResponse(BaseModel):
#     topic: str
#     summary: str
#     sources: list[str]
#     tools_used: list[str]

# parser = PydanticOutputParser(pydantic_object=ResearchResponse)

# prompt = ChatPromptTemplate.from_messages(
#     [
#         (
#             "system",
#             """
#             You are a research assistant that will help generate a research paper.
#             Answer the user query and use neccessary tools. 
#             Wrap the output in this format and provide no other text\n{format_instructions}
#             """,
#         ),
#         ("placeholder", "{chat_history}"),
#         ("human", "{query}"),
#         ("placeholder", "{agent_scratchpad}"),
#     ]
# ).partial(format_instructions=parser.get_format_instructions())

from src.agents.core.theoretical_agent import TheoreticalAgent
from src.agents.core.experimental_agent import ExperimentalAgent
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    convert_system_message_to_human=True
)

theo = TheoreticalAgent(llm)
exp = ExperimentalAgent(llm)

# 1. Theory
hyp = theo.generate_hypothesis("pendulum motion")
print("🧠 Theoretical Agent Hypothesis:", hyp)

# 2. Experiment
exp_design = exp.design_experiment(hyp.statement)
print("🔬 Experimental Agent Design:", exp_design)
