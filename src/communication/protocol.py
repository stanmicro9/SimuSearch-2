from typing import Dict, Any, List

class AgentCommunicationProtocol:
    """
    Enables structured message passing between agents using their LangChain-based run method.
    """
    def __init__(self, agents: Dict[str, Any]):
        self.agents = agents  # Dict of agent_name: agent_instance

    def send_message(self, sender: str, receiver: str, message: str, chat_history: List[str] = None, agent_scratchpad: str = "") -> Any:
        if receiver not in self.agents:
            raise ValueError(f"Receiver agent '{receiver}' not found.")
        response = self.agents[receiver].run(
            query=message,
            chat_history=chat_history or [],
            agent_scratchpad=agent_scratchpad
        )
        return response