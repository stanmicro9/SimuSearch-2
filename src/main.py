from src.agents.core.theoretical_agent import TheoreticalAgent
from src.agents.core.experimental_agent import ExperimentalAgent
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    convert_system_message_to_human=True
)

theo = TheoreticalAgent(llm)
exp = ExperimentalAgent(llm)

# 1. Theory
hyp = theo.generate_hypothesis("3d-reconstruction from 2d input")
print("🧠 Theoretical Agent Hypothesis:", hyp)

# 2. Experiment
exp_design = exp.design_experiment(hyp.statement)
print("🔬 Experimental Agent Design:", exp_design)