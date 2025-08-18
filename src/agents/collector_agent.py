from typing import Dict, Any, List
from src.schemas import HypothesisResponse, ExperimentDesign, ExperimentalResults, FinalAnalysis
from src.agents.base_agent import BaseAgent
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import json

class CollectorAgent(BaseAgent):
    def __init__(self, llm):
        super().__init__(
            name="CollectorAgent",
            llm=llm,
            response_model=FinalAnalysis,
            system_prompt="""You are a scientific analysis collector and synthesizer with expertise across multiple domains.

Your responsibilities:
1. Compare experimental results to theoretical predictions across any scientific field
2. Analyze data collected by the experimental agent using appropriate statistical methods
3. Aggregate findings from all agents into coherent conclusions
4. Provide final scientific conclusions and recommendations

Your analysis should be:
- Objective and evidence-based across all scientific domains
- Clear about limitations and uncertainties
- Suggestive of future research directions appropriate to the field
- Comprehensive yet accessible to both experts and general audiences
- Statistically sound and methodologically rigorous"""
        )

    def analyze_and_aggregate(self, 
                            scientific_question: str,
                            hypothesis: HypothesisResponse,
                            experiment_design: ExperimentDesign,
                            experimental_results: ExperimentalResults,
                            theoretical_guidance: Dict[str, Any]) -> FinalAnalysis:
        """Aggregate all findings and provide comprehensive final analysis"""
        
        # Extract domain information
        domain = theoretical_guidance.get("domain", "general")
        
        # Prepare comprehensive analysis query
        analysis_query = f"""
        SCIENTIFIC INVESTIGATION ANALYSIS
        
        Research Question: {scientific_question}
        Scientific Domain: {domain}
        
        THEORETICAL COMPONENT:
        - Hypothesis: {hypothesis.statement}
        - Mathematical Model: {hypothesis.mathematical_model}
        - Theoretical Confidence: {hypothesis.confidence}
        - Variables: {', '.join(hypothesis.variables)}
        
        EXPERIMENTAL COMPONENT:
        - Experiment ID: {experimental_results.experiment_id}
        - Supports Hypothesis: {experimental_results.supports_hypothesis}
        - Experimental Confidence: {experimental_results.confidence}
        - Analysis: {experimental_results.analysis}
        - Conclusion: {experimental_results.conclusion}
        - Raw Data Summary: {self._summarize_raw_data(experimental_results.raw_data)}
        
        THEORETICAL GUIDANCE USED:
        {json.dumps(theoretical_guidance.get("predicted_parameters", {}), indent=2)}
        
        Provide a comprehensive scientific analysis that:
        1. Compares theoretical predictions with experimental outcomes
        2. Evaluates the strength of evidence
        3. Identifies limitations and uncertainties
        4. Assesses the validity of the hypothesis
        5. Provides domain-specific insights
        6. Recommends future research directions
        
        Consider the specific methodologies and standards of {domain} research.
        """
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", self.prompt.messages[0].prompt.template),
            ("human", "{input}")
        ])
        
        chain = prompt | self.llm | StrOutputParser()
        analysis_result = chain.invoke({"input": analysis_query})
        
        # Calculate comprehensive agreement score
        agreement_score = self._calculate_comprehensive_agreement(hypothesis, experimental_results, domain)
        
        # Generate domain-specific future research
        future_research = self._generate_future_research(scientific_question, domain, experimental_results)
        
        return FinalAnalysis(
            scientific_question=scientific_question,
            hypothesis=hypothesis,
            experiment_design=experiment_design,
            experimental_results=experimental_results,
            theoretical_vs_experimental=f"Agreement score: {agreement_score:.2f}. {analysis_result}",
            final_conclusion=self._generate_comprehensive_conclusion(
                hypothesis, experimental_results, agreement_score, domain
            ),
            future_research=future_research
        )

    def _summarize_raw_data(self, raw_data: Dict[str, List[float]]) -> str:
        """Summarize raw experimental data"""
        summary = []
        for key, values in raw_data.items():
            if values:
                avg = np.mean(values)
                std = np.std(values)
                summary.append(f"{key}: mean={avg:.2f}, std={std:.2f}, n={len(values)}")
        return "; ".join(summary)

    def _calculate_comprehensive_agreement(self, hypothesis: HypothesisResponse, 
                                         results: ExperimentalResults, domain: str) -> float:
        """Calculate comprehensive agreement score considering domain-specific factors"""
        
        base_agreement = self._calculate_basic_agreement(hypothesis, results)
        
        # Domain-specific adjustments
        domain_factors = {
            "physics": 1.0,      # Physics often has high precision
            "chemistry": 0.95,   # Chemical reactions can have variability
            "biology": 0.85,     # Biological systems inherently variable
            "environmental": 0.8, # Environmental systems very complex
            "general": 0.9
        }
        
        domain_factor = domain_factors.get(domain, 0.9)
        adjusted_agreement = base_agreement * domain_factor
        
        return min(adjusted_agreement, 0.98)

    def _calculate_basic_agreement(self, hypothesis: HypothesisResponse, results: ExperimentalResults) -> float:
        """Calculate basic agreement between theory and experiment"""
        if results.supports_hypothesis:
            # Both theoretical and experimental confidence contribute
            return (hypothesis.confidence + results.confidence) / 2
        else:
            # Disagreement - lower score
            return max(0.1, 1.0 - abs(hypothesis.confidence - results.confidence))

    def _generate_comprehensive_conclusion(self, hypothesis: HypothesisResponse, 
                                         results: ExperimentalResults, 
                                         agreement_score: float, domain: str) -> str:
        """Generate comprehensive final conclusion"""
        
        confidence_level = "high" if agreement_score > 0.8 else "moderate" if agreement_score > 0.6 else "low"
        support_strength = "strongly" if agreement_score > 0.8 else "moderately" if agreement_score > 0.6 else "weakly"
        
        domain_context = {
            "physics": "physical principles and mathematical relationships",
            "chemistry": "chemical kinetics and thermodynamic principles", 
            "biology": "biological processes and ecological relationships",
            "environmental": "environmental interactions and sustainability factors",
            "general": "scientific principles and empirical relationships"
        }
        
        context = domain_context.get(domain, "scientific principles")
        
        if results.supports_hypothesis:
            return f"""The experimental evidence {support_strength} supports the hypothesis "{hypothesis.statement}" 
with {confidence_level} confidence (agreement score: {agreement_score:.2f}). The results are consistent with 
established {context}. The mathematical model {hypothesis.mathematical_model} provides a theoretical 
framework that aligns with the observed experimental data."""
        else:
            return f"""The experimental evidence does not strongly support the hypothesis "{hypothesis.statement}". 
While the theoretical foundation based on {context} suggested this relationship, the experimental data 
shows {confidence_level} agreement (score: {agreement_score:.2f}). This suggests the need for hypothesis 
refinement or consideration of additional variables not accounted for in the current model."""

    def _generate_future_research(self, question: str, domain: str, results: ExperimentalResults) -> List[str]:
        """Generate domain-specific future research directions"""
        
        domain_research = {
            "physics": [
                "Investigate quantum effects at microscopic scales",
                "Examine relativistic corrections for high-speed phenomena",
                "Study non-linear dynamics and chaos theory applications",
                "Explore temperature-dependent material properties"
            ],
            "chemistry": [
                "Investigate catalyst effects on reaction pathways",
                "Study solvent effects on reaction kinetics",
                "Examine pressure dependence of equilibrium constants",
                "Explore green chemistry alternatives"
            ],
            "biology": [
                "Study genetic variations affecting the observed response",
                "Investigate seasonal and circadian rhythm effects",
                "Examine inter-species variations and evolutionary implications",
                "Explore molecular mechanisms underlying the observed phenomena"
            ],
            "environmental": [
                "Scale up to ecosystem-level impacts",
                "Study long-term temporal trends and climate interactions",
                "Investigate human activity influences",
                "Examine geographical variations and local factors"
            ]
        }
        
        base_research = domain_research.get(domain, [
            "Expand parameter ranges for broader applicability",
            "Investigate confounding variables not yet considered",
            "Replicate study in different conditions",
            "Develop more sophisticated theoretical models"
        ])
        
        # Add result-specific research directions
        if results.supports_hypothesis:
            base_research.extend([
                "Optimize conditions for practical applications",
                "Investigate mechanisms underlying the confirmed relationship"
            ])
        else:
            base_research.extend([
                "Revise theoretical model to account for unexpected results",
                "Investigate alternative explanations for observed phenomena"
            ])
        
        return base_research[:6]  # Return top 6 research directions