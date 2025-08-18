from typing import Dict, Any, List
from langchain.schema import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langchain.memory import ConversationBufferMemory
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from src.schemas import HypothesisResponse, ExperimentDesign, ExperimentalResults
import json

class AgentCommunicationHub:
    """Enhanced communication hub using LangChain for agent coordination"""
    
    def __init__(self, llm=None):
        self.memory = ConversationBufferMemory(return_messages=True)
        self.shared_context = {}
        self.llm = llm
        self.communication_history = []
        
    def theoretical_to_experimental_handoff(self, 
                                          hypothesis: HypothesisResponse,
                                          theoretical_guidance: Dict[str, Any]) -> Dict[str, Any]:
        """Enhanced handoff with structured communication"""
        
        # Create structured message
        handoff_message = {
            "from_agent": "theoretical",
            "to_agent": "experimental",
            "message_type": "hypothesis_transfer",
            "content": {
                "hypothesis": {
                    "id": hypothesis.id,
                    "statement": hypothesis.statement,
                    "confidence": hypothesis.confidence,
                    "mathematical_model": hypothesis.mathematical_model,
                    "variables": hypothesis.variables
                },
                "theoretical_guidance": theoretical_guidance,
                "recommendations": self._extract_experimental_recommendations(theoretical_guidance)
            },
            "timestamp": datetime.now().isoformat()
        }
        
        # Store in communication history
        self.communication_history.append(handoff_message)
        
        # Add to LangChain memory
        message = HumanMessage(content=f"""
        🔬 HYPOTHESIS TRANSFER FROM THEORETICAL AGENT
        
        📋 Hypothesis Details:
        - ID: {hypothesis.id}
        - Statement: {hypothesis.statement}
        - Confidence: {hypothesis.confidence:.2f}
        - Mathematical Model: {hypothesis.mathematical_model}
        - Key Variables: {', '.join(hypothesis.variables)}
        
        🎯 Theoretical Guidance:
        {self._format_guidance_for_communication(theoretical_guidance)}
        
        🎯 Experimental Recommendations:
        {json.dumps(handoff_message['content']['recommendations'], indent=2)}
        
        Please design and execute an experiment to test this hypothesis.
        """)
        
        self.memory.chat_memory.add_message(message)
        
        return handoff_message

    def experimental_to_collector_handoff(self,
                                        experiment_design: ExperimentDesign,
                                        experimental_results: ExperimentalResults) -> Dict[str, Any]:
        """Enhanced handoff with comprehensive data transfer"""
        
        # Create structured message
        handoff_message = {
            "from_agent": "experimental",
            "to_agent": "collector",
            "message_type": "results_transfer",
            "content": {
                "experiment_design": {
                    "id": experiment_design.experiment_id,
                    "parameters": experiment_design.parameters,
                    "setup": experiment_design.setup,
                    "measurements": experiment_design.measurements
                },
                "experimental_results": {
                    "id": experimental_results.experiment_id,
                    "analysis": experimental_results.analysis,
                    "conclusion": experimental_results.conclusion,
                    "supports_hypothesis": experimental_results.supports_hypothesis,
                    "confidence": experimental_results.confidence,
                    "data_summary": self._summarize_experimental_data(experimental_results.raw_data)
                }
            },
            "timestamp": datetime.now().isoformat()
        }
        
        # Store in communication history
        self.communication_history.append(handoff_message)
        
        # Add to LangChain memory
        message = AIMessage(content=f"""
        📊 EXPERIMENTAL RESULTS FROM EXPERIMENTAL AGENT
        
        🔬 Experiment Details:
        - ID: {experimental_results.experiment_id}
        - Analysis: {experimental_results.analysis}
        - Conclusion: {experimental_results.conclusion}
        - Supports Hypothesis: {experimental_results.supports_hypothesis}
        - Confidence: {experimental_results.confidence:.2f}
        
        📈 Data Summary:
        {handoff_message['content']['experimental_results']['data_summary']}
        
        🛠️ Experimental Setup:
        - Parameters: {json.dumps(experiment_design.parameters, indent=2)}
        - Measurements: {', '.join(experiment_design.measurements)}
        
        Ready for final analysis and aggregation.
        """)
        
        self.memory.chat_memory.add_message(message)
        
        return handoff_message

    def _extract_experimental_recommendations(self, theoretical_guidance: Dict[str, Any]) -> Dict[str, Any]:
        """Extract actionable recommendations for experimental design"""
        return {
            "parameter_ranges": "Use theoretically predicted ranges",
            "measurement_precision": "High precision required for domain",
            "control_variables": "Standard domain controls",
            "expected_trends": "Based on mathematical model predictions"
        }

    def _format_guidance_for_communication(self, guidance: Dict[str, Any]) -> str:
        """Format theoretical guidance for clear communication"""
        formatted = []
        for key, value in guidance.items():
            if key == "theoretical_guidance":
                formatted.append(f"Theory: {value}")
            elif key == "predicted_parameters":
                formatted.append(f"Predictions: {json.dumps(value, indent=2)}")
            elif key == "mathematical_model":
                formatted.append(f"Model: {value}")
        return "\n".join(formatted)

    def _summarize_experimental_data(self, raw_data: Dict[str, List[float]]) -> str:
        """Create summary of experimental data for communication"""
        summary = []
        for key, values in raw_data.items():
            if values:
                avg = np.mean(values)
                min_val = min(values)
                max_val = max(values)
                summary.append(f"{key}: avg={avg:.2f}, range=[{min_val:.2f}, {max_val:.2f}], n={len(values)}")
        return "\n".join(summary)

    def get_communication_history(self) -> List[Dict[str, Any]]:
        """Get complete communication history between agents"""
        return self.communication_history

    def get_shared_context(self) -> Dict[str, Any]:
        """Get shared context across all agents"""
        return self.shared_context