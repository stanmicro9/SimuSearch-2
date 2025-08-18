import pytest
import os
from unittest.mock import Mock, patch
from src.workflows.scientific_workflow import ScientificWorkflow
from src.config import Config
from langchain_google_genai import ChatGoogleGenerativeAI

class TestSystemIntegration:
    """Integration tests for the complete system"""
    
    @pytest.fixture
    def mock_llm(self):
        """Create mock LLM for testing"""
        llm = Mock(spec=ChatGoogleGenerativeAI)
        llm.invoke.return_value = Mock(content="Test response from LLM")
        return llm
    
    @pytest.fixture
    def workflow(self, mock_llm):
        """Create workflow with mocked LLM"""
        return ScientificWorkflow(mock_llm)
    
    def test_physics_investigation(self, workflow):
        """Test complete physics investigation"""
        question = "How does temperature affect electrical resistance?"
        
        with patch.object(workflow.theoretical_agent, 'generate_hypothesis') as mock_hyp, \
             patch.object(workflow.experimental_agent, 'execute_experiment') as mock_exp:
            
            # Mock responses
            from src.schemas import HypothesisResponse, ExperimentalResults
            
            mock_hyp.return_value = HypothesisResponse(
                id="test_hyp",
                statement="Electrical resistance increases linearly with temperature",
                confidence=0.9,
                mathematical_model="R(T) = R₀(1 + αT)",
                variables=["temperature", "resistance"]
            )
            
            mock_exp.return_value = ExperimentalResults(
                experiment_id="test_exp",
                raw_data={"temperature": [20, 40, 60], "resistance": [100, 110, 120]},
                analysis="Linear relationship confirmed",
                conclusion="Temperature positively affects resistance",
                supports_hypothesis=True,
                confidence=0.85
            )
            
            result = workflow.investigate(question)
            
            assert result is not None
            assert result.scientific_question == question
            assert mock_hyp.called
            assert mock_exp.called
    
    def test_chemistry_investigation(self, workflow):
        """Test complete chemistry investigation"""
        question = "How does concentration affect reaction rate?"
        
        result = workflow.investigate(question)
        
        # Should not raise exceptions and return valid result
        assert result is not None
        assert hasattr(result, 'final_conclusion')
    
    def test_biology_investigation(self, workflow):
        """Test complete biology investigation"""
        question = "How does light intensity affect plant growth?"
        
        result = workflow.investigate(question)
        
        assert result is not None
        assert hasattr(result, 'experimental_results')
    
    def test_error_handling(self, workflow):
        """Test system error handling"""
        
        with patch.object(workflow.theoretical_agent, 'generate_hypothesis', side_effect=Exception("Test error")):
            result = workflow.investigate("Test question")
            
            # Should return failure analysis instead of crashing
            assert result is not None
            assert "error" in result.final_conclusion.lower()