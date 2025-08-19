from langgraph.graph import StateGraph, END
from src.agents.core.theoretical_agent import TheoreticalAgent
from src.agents.core.experimental_agent import ExperimentalAgent
from src.agents.core.analysis_agent import AnalysisAgent
from src.agents.research.literature_agent import LiteratureAgent
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from src.config import serpapi_api_key
from pydantic import BaseModel
from typing_extensions import TypedDict

load_dotenv()
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

theo = TheoreticalAgent(llm)
exp = ExperimentalAgent(llm)
analysis = AnalysisAgent(llm)
literature = LiteratureAgent(llm, serpapi_api_key)

CONFIDENCE_THRESHOLD = 0.9
MAX_TURNS = 5


# Define state schema
class WorkflowState(TypedDict, total=False):
    topic: str
    context: str
    hypothesis: dict
    experiment: dict
    analysis: dict
    literature: dict
    confidence: float
    turn: int

def theoretical_node(state):
    topic = state.get("topic")
    context = state.get("context", "")
    hyp = theo.generate_hypothesis(topic, context)
    state["hypothesis"] = hyp
    state["confidence"] = getattr(hyp, "confidence", 0.0)
    return state

def experimental_node(state):
    hyp = state["hypothesis"]
    exp_design = exp.design_experiment(hyp.statement)
    state["experiment"] = exp_design
    return state

def analysis_node(state):
    hyp = state["hypothesis"]
    exp_design = state["experiment"]
    analysis_result = analysis.run(query=f"Compare theoretical hypothesis: {hyp} with experimental results: {exp_design}")
    state["analysis"] = analysis_result
    return state

def literature_node(state):
    topic = state["topic"]
    lit_result = literature.search_literature(topic)
    state["literature"] = lit_result
    return state

def decision_node(state):
    confidence = state.get("confidence", 0.0)
    turn = state.get("turn", 1)

    if confidence >= CONFIDENCE_THRESHOLD or turn >= MAX_TURNS:
        return {"__end__": {"reason": "confidence threshold reached"}}

    analysis_result = state.get("analysis")

    if analysis_result and "recommend_literature" in getattr(analysis_result, "next_steps", ""):
        return {"next": "literature", "turn": turn + 1}

    return {"next": "experimental", "turn": turn + 1}

graph_builder = StateGraph(WorkflowState)   # or a Pydantic model / TypedDict schema
graph_builder.add_node("theoretical", theoretical_node)
graph_builder.add_node("experimental", experimental_node)
graph_builder.add_node("analysis", analysis_node)
graph_builder.add_node("literature", literature_node)
graph_builder.add_node("decision", decision_node)

graph_builder.add_edge("theoretical", "experimental")
graph_builder.add_edge("experimental", "analysis")
graph_builder.add_edge("analysis", "decision")
graph_builder.add_edge("decision", "literature")
graph_builder.add_edge("literature", "experimental")
graph_builder.add_edge("decision", END)

graph_builder.set_entry_point("theoretical")

graph = graph_builder.compile()

def run_workflow(topic):
    state = {"topic": topic, "turn": 1}
    result = result = graph.invoke(state)
    return result

# Example usage
if __name__ == "__main__":
    topic = input("Enter your research topic/question: ")
    result = run_workflow(topic)
    graph.visualize(output_file="workflow_graph.png")
    print("\nFinal workflow state:", result)
