from typing import Dict, Any
from langchain.schema import BaseMessage
from src.agents.core.theoretical_agent import TheoreticalAgent
from src.agents.core.experimental_agent import ExperimentalAgent
from src.agents.collector_agent import CollectorAgent
from src.communication.agent_communication import AgentCommunicationHub
from src.schemas import FinalAnalysis
import time
import traceback

class ScientificWorkflow:
    """Enhanced orchestration of the complete scientific investigation workflow"""
    
    def __init__(self, llm):
        self.theoretical_agent = TheoreticalAgent(llm)
        self.experimental_agent = ExperimentalAgent(llm)
        self.collector_agent = CollectorAgent(llm)
        self.comm_hub = AgentCommunicationHub(llm)
        self.llm = llm
        
    def investigate(self, scientific_question: str) -> FinalAnalysis:
        """Run complete scientific investigation workflow with enhanced error handling"""
        
        try:
            print("🚀 Starting scientific investigation workflow...")
            
            # Phase 1: Theoretical Analysis
            print("\n📚 Phase 1: Theoretical Analysis")
            start_time = time.time()
            
            hypothesis = self.theoretical_agent.generate_hypothesis(scientific_question)
            print(f"✅ Hypothesis generated in {time.time() - start_time:.1f}s")
            print(f"   📝 {hypothesis.statement}")
            print(f"   🎯 Confidence: {hypothesis.confidence:.2f}")
            
            theoretical_guidance = self.theoretical_agent.collaborate_on_experiment_design(hypothesis)
            print(f"✅ Theoretical guidance prepared")
            
            # Phase 2: Agent Communication
            print("\n🤝 Phase 2: Agent Communication")
            handoff_1 = self.comm_hub.theoretical_to_experimental_handoff(
                hypothesis, theoretical_guidance
            )
            print(f"✅ Theoretical → Experimental handoff completed")
            
            # Phase 3: Experimental Design & Execution
            print("\n🔬 Phase 3: Experimental Design & Execution")
            start_time = time.time()
            
            experiment_design = self.experimental_agent.design_experiment(
                hypothesis.statement, theoretical_guidance
            )
            print(f"✅ Experiment designed in {time.time() - start_time:.1f}s")
            print(f"   🆔 ID: {experiment_design.experiment_id}")
            print(f"   📊 Measurements: {len(experiment_design.measurements)} variables")
            
            start_time = time.time()
            experimental_results = self.experimental_agent.execute_experiment(experiment_design)
            print(f"✅ Experiment executed in {time.time() - start_time:.1f}s")
            print(f"   📈 Supports hypothesis: {experimental_results.supports_hypothesis}")
            print(f"   🎯 Confidence: {experimental_results.confidence:.2f}")
            
            # Phase 4: Results Communication
            print("\n📡 Phase 4: Results Communication")
            handoff_2 = self.comm_hub.experimental_to_collector_handoff(
                experiment_design, experimental_results
            )
            print(f"✅ Experimental → Collector handoff completed")
            
            # Phase 5: Final Analysis
            print("\n📋 Phase 5: Final Analysis & Synthesis")
            start_time = time.time()
            
            final_analysis = self.collector_agent.analyze_and_aggregate(
                scientific_question=scientific_question,
                hypothesis=hypothesis,
                experiment_design=experiment_design,
                experimental_results=experimental_results,
                theoretical_guidance=theoretical_guidance
            )
            print(f"✅ Final analysis completed in {time.time() - start_time:.1f}s")
            
            return final_analysis
            
        except Exception as e:
            print(f"❌ Error in workflow: {str(e)}")
            print(f"📍 Traceback: {traceback.format_exc()}")
            
            # Return a basic failure analysis
            return self._create_failure_analysis(scientific_question, str(e))

    def _create_failure_analysis(self, question: str, error: str) -> FinalAnalysis:
        """Create a failure analysis when workflow encounters errors"""
        from src.schemas import HypothesisResponse, ExperimentDesign, ExperimentalResults
        
        # Create minimal objects for failure case
        failed_hypothesis = HypothesisResponse(
            id="failed_hypothesis",
            statement=f"Investigation of: {question}",
            confidence=0.0,
            mathematical_model="Investigation failed",
            variables=["error"]
        )
        
        failed_design = ExperimentDesign(
            experiment_id="failed_experiment",
            hypothesis_id="failed_hypothesis",
            parameters={"error": error},
            setup="Investigation failed",
            measurements=["error_analysis"],
            expected_outcome="System error occurred",
            tools_required=["debugging_tools"]
        )
        
        failed_results = ExperimentalResults(
            experiment_id="failed_experiment",
            raw_data={"error": [0]},
            analysis=f"System error: {error}",
            conclusion="Investigation could not be completed",
            supports_hypothesis=False,
            confidence=0.0
        )
        
        return FinalAnalysis(
            scientific_question=question,
            hypothesis=failed_hypothesis,
            experiment_design=failed_design,
            experimental_results=failed_results,
            theoretical_vs_experimental="Analysis failed due to system error",
            final_conclusion=f"The scientific investigation could not be completed due to: {error}",
            future_research=["Debug system errors", "Improve error handling", "Retry investigation"]
        )

    def get_workflow_status(self) -> Dict[str, Any]:
        """Get current status of the workflow"""
        return {
            "communication_history": self.comm_hub.get_communication_history(),
            "shared_context": self.comm_hub.get_shared_context(),
            "agents_initialized": {
                "theoretical": self.theoretical_agent is not None,
                "experimental": self.experimental_agent is not None,
                "collector": self.collector_agent is not None
            }
        }

# Additional missing imports for numpy
import numpy as np
from datetime import datetime