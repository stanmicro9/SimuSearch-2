from typing import List, Dict, Any, Optional
from datetime import datetime
import numpy as np
import random
import math
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from src.agents.base_agent import BaseAgent
from src.schemas import ExperimentDesign, ExperimentalResults
from src.tools.simulation_tools import GenericSimulator
import json

class ExperimentalAgent(BaseAgent):
    def __init__(self, llm):
        super().__init__(
            name="ExperimentalAgent",
            llm=llm,
            response_model=ExperimentDesign,
            system_prompt="""You are an experimental scientist capable of designing and conducting experiments across multiple scientific domains.

Your responsibilities:
1. Design rigorous experiments to test hypotheses in any scientific field
2. Execute experiments in simulated environments
3. Collect and analyze raw experimental data
4. Provide objective experimental conclusions

When designing experiments:
- Adapt methodology to the specific scientific domain
- Specify clear parameters and controls
- Define measurement procedures appropriate for the field
- Consider domain-specific error sources and mitigation
- Plan for appropriate statistical analysis

You have access to flexible simulation environments for various scientific domains."""
        )
        self.simulator = GenericSimulator()

    def design_experiment(self, hypothesis: str, theoretical_guidance: Dict[str, Any] = None) -> ExperimentDesign:
        """Design experiment for any scientific domain"""
        
        domain = theoretical_guidance.get("domain", "general") if theoretical_guidance else "general"
        
        design_query = f"""
        Design a controlled experiment to test: {hypothesis}
        Scientific Domain: {domain}
        
        Theoretical guidance: {json.dumps(theoretical_guidance, indent=2) if theoretical_guidance else 'None provided'}
        
        Create an experimental design that specifies:
        
        1. EXPERIMENTAL PARAMETERS (independent variables to control):
           - List specific values/levels to test
           - Include reasonable ranges for the domain
        
        2. SETUP AND PROCEDURE:
           - Detailed experimental setup
           - Step-by-step procedure
           - Control measures
        
        3. MEASUREMENTS (dependent variables):
           - What to measure
           - How to measure it
           - Expected measurement units
        
        4. EXPECTED OUTCOME:
           - Predicted results based on hypothesis
           - Expected trends or patterns
        
        5. REQUIRED TOOLS/EQUIPMENT:
           - Domain-appropriate instruments
           - Measurement devices
           - Control equipment
        
        Adapt your design to be appropriate for {domain} research.
        """
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", self.prompt.messages[0].prompt.template),
            ("human", "{input}")
        ])
        
        chain = prompt | self.llm | StrOutputParser()
        result = chain.invoke({"input": design_query})
        
        experiment_id = f"exp_{domain}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Parse domain-specific parameters
        parameters = self._generate_domain_parameters(domain, hypothesis, theoretical_guidance)
        measurements = self._generate_domain_measurements(domain, hypothesis)
        tools = self._generate_domain_tools(domain)
        
        return ExperimentDesign(
            experiment_id=experiment_id,
            hypothesis_id=getattr(hypothesis, 'id', 'unknown'),
            parameters=parameters,
            setup=f"Controlled {domain} experiment setup with precise measurement capabilities",
            measurements=measurements,
            expected_outcome=result,
            tools_required=tools
        )

    def _generate_domain_parameters(self, domain: str, hypothesis: str, guidance: Dict[str, Any]) -> Dict[str, Any]:
        """Generate domain-specific experimental parameters"""
        
        domain_params = {
            "physics": {
                "temperature": [20, 30, 40, 50, 60],  # Celsius
                "pressure": [1.0, 1.2, 1.4, 1.6],    # atm
                "time_duration": 300,                  # seconds
                "sample_rate": 100                     # Hz
            },
            "chemistry": {
                "concentration": [0.1, 0.5, 1.0, 2.0, 5.0],  # M
                "temperature": [25, 35, 45, 55, 65],          # Celsius
                "pH": [6.0, 7.0, 8.0, 9.0],                  # pH units
                "reaction_time": 3600                          # seconds
            },
            "biology": {
                "light_intensity": [100, 300, 500, 700, 1000],  # lux
                "nutrient_concentration": [0.5, 1.0, 1.5, 2.0], # g/L
                "temperature": [15, 20, 25, 30, 35],            # Celsius
                "observation_period": 168                        # hours (1 week)
            },
            "environmental": {
                "humidity": [30, 50, 70, 90],         # %
                "air_quality_index": [50, 100, 150, 200],
                "wind_speed": [0, 5, 10, 15],         # m/s
                "monitoring_duration": 720             # hours (1 month)
            }
        }
        
        return domain_params.get(domain, {
            "variable_1": [1, 2, 3, 4, 5],
            "variable_2": [10, 20, 30, 40, 50],
            "duration": 100,
            "sample_size": 50
        })

    def _generate_domain_measurements(self, domain: str, hypothesis: str) -> List[str]:
        """Generate domain-specific measurements"""
        
        domain_measurements = {
            "physics": ["force", "acceleration", "velocity", "energy", "frequency", "amplitude"],
            "chemistry": ["concentration", "reaction_rate", "yield", "temperature_change", "pH_change"],
            "biology": ["growth_rate", "biomass", "population_size", "metabolic_rate", "survival_rate"],
            "environmental": ["pollution_levels", "biodiversity_index", "air_quality", "water_quality"]
        }
        
        base_measurements = domain_measurements.get(domain, ["variable_response", "effect_magnitude"])
        
        # Add time-series measurements
        return base_measurements + ["time_series_data", "statistical_variance", "measurement_error"]

    def _generate_domain_tools(self, domain: str) -> List[str]:
        """Generate domain-specific required tools"""
        
        domain_tools = {
            "physics": ["force_sensor", "motion_detector", "temperature_probe", "pressure_gauge", "oscilloscope"],
            "chemistry": ["pH_meter", "spectrophotometer", "balance", "thermometer", "titration_setup"],
            "biology": ["microscope", "growth_chamber", "pH_meter", "light_meter", "biomass_scale"],
            "environmental": ["air_quality_monitor", "water_testing_kit", "weather_station", "soil_analyzer"]
        }
        
        return domain_tools.get(domain, ["measurement_device", "data_logger", "control_system"])

    def execute_experiment(self, experiment_design: ExperimentDesign) -> ExperimentalResults:
        """Execute experiment using generic simulation"""
        print(f"🔬 Executing experiment: {experiment_design.experiment_id}")
        
        # Extract domain from experiment ID
        domain = experiment_design.experiment_id.split('_')[1] if '_' in experiment_design.experiment_id else "general"
        
        # Run domain-specific simulation
        raw_data = self.simulator.run_experiment(
            domain=domain,
            parameters=experiment_design.parameters,
            measurements=experiment_design.measurements
        )
        
        # Analyze results
        analysis = self._analyze_experimental_data(raw_data, domain)
        
        return ExperimentalResults(
            experiment_id=experiment_design.experiment_id,
            raw_data=raw_data,
            analysis=analysis["summary"],
            conclusion=analysis["conclusion"],
            supports_hypothesis=analysis["supports_hypothesis"],
            confidence=analysis["confidence"]
        )

    def _analyze_experimental_data(self, raw_data: Dict[str, List[float]], domain: str) -> Dict[str, Any]:
        """Analyze experimental data with domain-specific methods"""
        
        # Extract key variables for analysis
        independent_vars = []
        dependent_vars = []
        
        for key, values in raw_data.items():
            if "level" in key or "concentration" in key or "temperature" in key:
                independent_vars = values
            elif "rate" in key or "response" in key or "measurement" in key:
                dependent_vars = values
        
        if not independent_vars or not dependent_vars:
            # Use first two data series if structure unclear
            data_keys = list(raw_data.keys())
            independent_vars = raw_data[data_keys[0]] if data_keys else [1, 2, 3]
            dependent_vars = raw_data[data_keys[1]] if len(data_keys) > 1 else [1, 2, 3]
        
        # Calculate correlation
        if len(independent_vars) == len(dependent_vars) and len(independent_vars) > 1:
            correlation = np.corrcoef(independent_vars, dependent_vars)[0, 1]
        else:
            correlation = 0.5  # Default moderate correlation
        
        # Domain-specific analysis
        domain_analysis = {
            "physics": self._physics_analysis(correlation),
            "chemistry": self._chemistry_analysis(correlation),
            "biology": self._biology_analysis(correlation),
            "environmental": self._environmental_analysis(correlation)
        }
        
        return domain_analysis.get(domain, self._general_analysis(correlation))

    def _physics_analysis(self, correlation: float) -> Dict[str, Any]:
        return {
            "summary": f"Physical relationship shows correlation coefficient of {correlation:.3f}",
            "conclusion": f"{'Strong' if abs(correlation) > 0.8 else 'Moderate' if abs(correlation) > 0.5 else 'Weak'} physical relationship observed",
            "supports_hypothesis": abs(correlation) > 0.4,
            "confidence": min(abs(correlation), 0.95)
        }

    def _chemistry_analysis(self, correlation: float) -> Dict[str, Any]:
        return {
            "summary": f"Chemical kinetics analysis shows correlation of {correlation:.3f}",
            "conclusion": f"{'Significant' if abs(correlation) > 0.7 else 'Moderate' if abs(correlation) > 0.4 else 'Minimal'} chemical effect detected",
            "supports_hypothesis": abs(correlation) > 0.3,
            "confidence": min(abs(correlation) * 1.1, 0.95)
        }

    def _biology_analysis(self, correlation: float) -> Dict[str, Any]:
        return {
            "summary": f"Biological response analysis shows correlation of {correlation:.3f}",
            "conclusion": f"{'Strong' if abs(correlation) > 0.6 else 'Moderate' if abs(correlation) > 0.3 else 'Weak'} biological response observed",
            "supports_hypothesis": abs(correlation) > 0.25,
            "confidence": min(abs(correlation) * 0.9, 0.85)  # Biology often has more variability
        }

    def _environmental_analysis(self, correlation: float) -> Dict[str, Any]:
        return {
            "summary": f"Environmental impact analysis shows correlation of {correlation:.3f}",
            "conclusion": f"{'Significant' if abs(correlation) > 0.7 else 'Detectable' if abs(correlation) > 0.4 else 'Minimal'} environmental effect",
            "supports_hypothesis": abs(correlation) > 0.35,
            "confidence": min(abs(correlation) * 0.95, 0.9)
        }

    def _general_analysis(self, correlation: float) -> Dict[str, Any]:
        return {
            "summary": f"General analysis shows correlation of {correlation:.3f}",
            "conclusion": f"{'Strong' if abs(correlation) > 0.7 else 'Moderate' if abs(correlation) > 0.4 else 'Weak'} relationship detected",
            "supports_hypothesis": abs(correlation) > 0.4,
            "confidence": min(abs(correlation), 0.8)
        }