"""
Multi-Agent Scientific Investigation System

A system that uses AI agents to conduct scientific investigations
across multiple domains through hypothesis generation, experimental
design, execution, and analysis.
"""

__version__ = "1.0.0"
__author__ = "Scientific AI Research Team"

from .agents import TheoreticalAgent, ExperimentalAgent, CollectorAgent
from .workflows import ScientificWorkflow
from .communication import AgentCommunicationHub
from .tools import GenericSimulator
from .config import Config

__all__ = [
    'TheoreticalAgent',
    'ExperimentalAgent', 
    'CollectorAgent',
    'ScientificWorkflow',
    'AgentCommunicationHub',
    'GenericSimulator',
    'Config'
]