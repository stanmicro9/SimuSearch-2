"""
Unit tests for the multi-agent system
"""

import pytest
from unittest.mock import Mock, patch
from src.agents.core.theoretical_agent import TheoreticalAgent
from src.agents.core.experimental_agent import ExperimentalAgent
from src.agents.collector_agent import CollectorAgent
from src.schemas import HypothesisResponse, ExperimentDesign, ExperimentalResults
from langchain_google_genai import ChatGoogleGenerativeAI

class TestTheoreticalAgent:
    """Test suite for TheoreticalAgent"""
    
    def setup_method(self):
        self.mock_llm = Mock(spec=ChatGoogleGenerativeAI)
        self.agent = TheoreticalAgent(self.mock_llm)
    
    def test_domain_identification(self):
        """Test scientific domain identification"""
        physics_question = "How does force affect acceleration?"
        domain = self.agent._identify_scientific_domain(physics_question)
        assert domain == "physics"
        
        chemistry_question = "How does temperature affect reaction rate?"
        domain = self.agent._identify_scientific_domain(chemistry_question)
        assert domain == "chemistry"
    
    def test_knowledge_base_initialization(self):
        """Test knowledge base contains expected domains"""
        kb = self.agent.knowledge_base
        assert "physics" in kb
        assert "chemistry" in kb
        assert "biology" in kb
        
    @patch.object(TheoreticalAgent, 'run')
    def test_hypothesis_generation(self, mock_run):
        """Test hypothesis generation process"""
        mock_run.return_value = "Test hypothesis about temperature effects"
        
        result = self.agent.generate_hypothesis("How does temperature affect plant growth?")
        
        assert isinstance(result, HypothesisResponse)
        assert result.id.startswith("hyp_")
        assert mock_run.called

class TestExperimentalAgent:
    """Test suite for ExperimentalAgent"""
    
    def setup_method(self):
        self.mock_llm = Mock(spec=ChatGoogleGenerativeAI)
        self.agent = ExperimentalAgent(self.mock_llm)
    
    def test_domain_parameters_generation(self):
        """Test domain-specific parameter generation"""
        physics_params = self.agent._generate_domain_parameters("physics", "test hypothesis", {})
        assert "temperature" in physics_params
        
        chemistry_params = self.agent._generate_domain_parameters("chemistry", "test hypothesis", {})
        assert "concentration" in chemistry_params
    
    def test_simulation_execution(self):
        """Test simulation execution"""
        design = ExperimentDesign(
            experiment_id="test_exp",
            hypothesis_id="test_hyp",
            parameters={"temperature": [20, 30, 40]},
            setup="test setup",
            measurements=["response"],
            expected_outcome="test outcome",
            tools_required=["thermometer"]
        )
        
        results = self.agent.execute_experiment(design)
        assert isinstance(results, ExperimentalResults)
        assert results.experiment_id == "test_exp"

class TestWorkflowIntegration:
    """Integration tests for the complete workflow"""
    
    def setup_method(self):
        self.mock_llm = Mock(spec=ChatGoogleGenerativeAI)
    
    @patch('src.workflows.scientific_workflow.ScientificWorkflow.investigate')
    def test_complete_workflow(self, mock_investigate):
        """Test complete scientific investigation workflow"""
        from src.workflows.scientific_workflow import ScientificWorkflow
        
        workflow = ScientificWorkflow(self.mock_llm)
        
        # Mock a successful investigation
        mock_investigate.return_value = Mock()
        
        result = workflow.investigate("How does light affect photosynthesis?")
        assert mock_investigate.called

# Run tests with: pytest tests/test_agents.py -v