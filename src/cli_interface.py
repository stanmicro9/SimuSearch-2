
import sys
from src.agents.core.theoretical_agent import TheoreticalAgent
from src.agents.core.experimental_agent import ExperimentalAgent
from src.agents.core.analysis_agent import AnalysisAgent
from src.communication.protocol import AgentCommunicationProtocol
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from src.config import serpapi_api_key

load_dotenv()
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
)

theo = TheoreticalAgent(llm)
exp = ExperimentalAgent(llm)
analysis = AnalysisAgent(llm)

MAX_TURNS = 5
CONFIDENCE_THRESHOLD = 0.9

agents = {
    "theoretical": theo,
    "experimental": exp,
    "analysis": analysis,
}
protocol = AgentCommunicationProtocol(agents)

def main():
    topic = input("Enter your research topic/question: ")
    turn = 1
    confidence = 0.0
    context = ""
    hyp = protocol.send_message(
        sender="user",
        receiver="theoretical",
        message=topic
    )
    print("\n Theoretical Agent Hypothesis:", hyp)
    confidence = getattr(hyp, "confidence", 0.0)

    while confidence < CONFIDENCE_THRESHOLD and turn <= MAX_TURNS:
        print(f"\n--- Turn {turn} ---")
        user_input = input("Choose next agent (experimental/analysis/) or type 'stop' to end: ").strip().lower()
        if user_input == "stop":
            print("\nConversation stopped by user.")
            break
        elif user_input == "experimental":
            exp_design = protocol.send_message(
                sender="theoretical",
                receiver="experimental",
                message=hyp.statement
            )
            print("\nExperimental Agent Design:", exp_design)
            sim_result = protocol.send_message(
                sender="experimental",
                receiver="experimental",
                message=f"Run simulation for: {exp_design}"
            )
            print("\nSimulation Result:", sim_result)
            hyp = protocol.send_message(
                sender="experimental",
                receiver="theoretical",
                message=sim_result
            )
            print("\nTheoretical Agent Revised Hypothesis:", hyp)
            confidence = getattr(hyp, "confidence", confidence)
        elif user_input == "analysis":
            analysis_result = protocol.send_message(
                sender="experimental",
                receiver="analysis",
                message=f"Analyze results for: {hyp.statement}"
            )
            print("\nAnalysis Agent Result:", analysis_result)
        else:
            print("Invalid choice. Please select 'experimental', 'analysis', 'literature', or 'stop'.")
        turn += 1

    print(f"\nConversation ended after {turn-1} turns with confidence: {confidence:.2f}")

if __name__ == "__main__":
    main()