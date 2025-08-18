from typing import List, Dict, Any, Optional
from datetime import datetime
from langchain.tools import BaseTool, tool
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from pydantic import BaseModel, Field
from src.agents.base_agent import BaseAgent
from src.schemas import HypothesisResponse
import json
import re

class TheoreticalAgent(BaseAgent):
    def __init__(self, llm):
        super().__init__(
            name="TheoreticalAgent",
            llm=llm,
            response_model=HypothesisResponse,
            system_prompt="""You are a theoretical scientist with expertise across multiple scientific domains.
            
Your responsibilities:
1. Generate well-founded scientific hypotheses based on established theory
2. Create or recall relevant mathematical models for any scientific domain
3. Perform literature review and theoretical analysis
4. Design experiments collaboratively with the experimental agent

When generating hypotheses:
- Base them on established scientific principles from any field (physics, chemistry, biology, etc.)
- Include mathematical formulations when relevant
- Specify key variables and their relationships
- Provide confidence estimates based on theoretical foundation
- Consider interdisciplinary connections

You adapt your knowledge to the specific scientific domain of the question."""
        )
        self.knowledge_base = self._initialize_comprehensive_knowledge()

    def _initialize_comprehensive_knowledge(self) -> Dict[str, Any]:
        """Initialize comprehensive theoretical knowledge base across domains"""
        return {
            "physics": {
                "mechanics": {
                    "equations": ["F=ma", "E=mc²", "F=kx", "τ=Iα"],
                    "concepts": ["energy conservation", "momentum", "oscillations", "waves"]
                },
                "thermodynamics": {
                    "equations": ["PV=nRT", "ΔU=Q-W", "S=k ln W"],
                    "concepts": ["heat transfer", "entropy", "phase transitions"]
                },
                "electromagnetism": {
                    "equations": ["F=qE", "B=μI/2πr", "∇×E=-∂B/∂t"],
                    "concepts": ["electric fields", "magnetic fields", "electromagnetic induction"]
                }
            },
            "chemistry": {
                "kinetics": {
                    "equations": ["rate = k[A]^m[B]^n", "k = Ae^(-Ea/RT)"],
                    "concepts": ["reaction rates", "activation energy", "catalysis"]
                },
                "thermochemistry": {
                    "equations": ["ΔH = ΣH_products - ΣH_reactants", "ΔG = ΔH - TΔS"],
                    "concepts": ["enthalpy", "entropy", "spontaneity"]
                },
                "equilibrium": {
                    "equations": ["K = [products]/[reactants]", "ΔG° = -RT ln K"],
                    "concepts": ["Le Chatelier's principle", "equilibrium constants"]
                }
            },
            "biology": {
                "ecology": {
                    "equations": ["dN/dt = rN(1-N/K)", "Shannon H = -Σpi ln pi"],
                    "concepts": ["population growth", "carrying capacity", "biodiversity"]
                },
                "physiology": {
                    "equations": ["V = TV × RR", "CO = HR × SV"],
                    "concepts": ["homeostasis", "feedback loops", "metabolism"]
                },
                "genetics": {
                    "equations": ["p² + 2pq + q² = 1", "F = (Ho - He)/He"],
                    "concepts": ["Hardy-Weinberg equilibrium", "inheritance patterns"]
                }
            },
            "environmental_science": {
                "climate": {
                    "equations": ["S = σT⁴", "ΔT = λ × ΔF"],
                    "concepts": ["greenhouse effect", "carbon cycle", "climate feedback"]
                }
            }
        }

    def _identify_scientific_domain(self, question: str) -> str:
        """Identify the primary scientific domain of the question"""
        question_lower = question.lower()
        
        domain_keywords = {
            "physics": ["force", "energy", "motion", "temperature", "pressure", "electromagnetic", "quantum", "gravity", "oscillation", "wave"],
            "chemistry": ["reaction", "chemical", "molecule", "catalyst", "pH", "concentration", "element", "compound", "bond"],
            "biology": ["plant", "animal", "cell", "organism", "growth", "evolution", "gene", "protein", "ecosystem", "species"],
            "environmental": ["climate", "pollution", "ecosystem", "carbon", "greenhouse", "sustainability", "water quality"],
            "engineering": ["efficiency", "design", "material", "structure", "optimization", "performance"],
            "medicine": ["health", "disease", "treatment", "drug", "symptom", "therapy", "diagnosis"]
        }
        
        domain_scores = {}
        for domain, keywords in domain_keywords.items():
            score = sum(1 for keyword in keywords if keyword in question_lower)
            domain_scores[domain] = score
        
        return max(domain_scores, key=domain_scores.get) if max(domain_scores.values()) > 0 else "general"

    def _get_domain_knowledge(self, domain: str, question: str) -> Dict[str, Any]:
        """Get relevant knowledge for the identified domain"""
        base_knowledge = self.knowledge_base.get(domain, {})
        
        # Add cross-domain knowledge if relevant
        question_lower = question.lower()
        if "temperature" in question_lower and domain != "physics":
            base_knowledge.update(self.knowledge_base.get("physics", {}).get("thermodynamics", {}))
        if "rate" in question_lower and domain != "chemistry":
            base_knowledge.update(self.knowledge_base.get("chemistry", {}).get("kinetics", {}))
            
        return base_knowledge

    def _perform_literature_review(self, topic: str, domain: str) -> Dict[str, Any]:
        """Simulate literature review based on topic and domain"""
        
        # Domain-specific literature sources
        literature_sources = {
            "physics": [
                "Physical Review Letters", "Nature Physics", "Journal of Applied Physics",
                "Classical Mechanics textbooks", "Quantum Mechanics references"
            ],
            "chemistry": [
                "Journal of the American Chemical Society", "Nature Chemistry", 
                "Chemical Reviews", "Physical Chemistry textbooks"
            ],
            "biology": [
                "Nature", "Science", "Cell", "Journal of Experimental Biology",
                "Molecular Biology texts", "Ecology references"
            ],
            "environmental": [
                "Environmental Science & Technology", "Nature Climate Change",
                "Journal of Environmental Quality", "Environmental Chemistry texts"
            ]
        }
        
        return {
            "sources": literature_sources.get(domain, ["General scientific journals"]),
            "key_findings": f"Literature review for {topic} in {domain} domain",
            "research_gaps": f"Limited studies on specific aspects of {topic}",
            "established_principles": self._get_domain_knowledge(domain, topic)
        }

    def generate_hypothesis(self, scientific_question: str, context: str = "") -> HypothesisResponse:
        """Generate hypothesis for any scientific domain"""
        
        # Identify domain and get relevant knowledge
        domain = self._identify_scientific_domain(scientific_question)
        domain_knowledge = self._get_domain_knowledge(domain, scientific_question)
        literature = self._perform_literature_review(scientific_question, domain)
        
        enhanced_query = f"""
        Scientific Question: {scientific_question}
        Context: {context}
        Scientific Domain: {domain}
        
        Relevant Knowledge Base:
        {json.dumps(domain_knowledge, indent=2)}
        
        Literature Review Results:
        Sources: {', '.join(literature['sources'][:3])}
        Key Findings: {literature['key_findings']}
        Established Principles: {literature['established_principles']}
        
        Generate a testable scientific hypothesis that:
        1. Directly addresses the research question
        2. Is based on established scientific principles
        3. Includes relevant variables and their expected relationships
        4. Can be tested experimentally
        5. Includes a mathematical model or relationship if applicable
        
        Provide your response in the following format:
        HYPOTHESIS: [Clear, testable statement]
        CONFIDENCE: [0.0 to 1.0]
        MATHEMATICAL_MODEL: [Equation or relationship if applicable]
        VARIABLES: [List of key variables]
        REASONING: [Brief explanation of theoretical basis]
        """
        
        result = self.run(query=enhanced_query)
        
        # Parse the structured response
        if isinstance(result, HypothesisResponse):
            result.id = f"hyp_{domain}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            return result
        
        # Parse string response if structured parsing fails
        response_text = str(result)
        hypothesis_match = re.search(r'HYPOTHESIS:\s*(.+?)(?=\n|CONFIDENCE|$)', response_text, re.DOTALL)
        confidence_match = re.search(r'CONFIDENCE:\s*([0-9.]+)', response_text)
        model_match = re.search(r'MATHEMATICAL_MODEL:\s*(.+?)(?=\n|VARIABLES|$)', response_text, re.DOTALL)
        variables_match = re.search(r'VARIABLES:\s*(.+?)(?=\n|REASONING|$)', response_text, re.DOTALL)
        
        return HypothesisResponse(
            id=f"hyp_{domain}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            statement=hypothesis_match.group(1).strip() if hypothesis_match else response_text[:200],
            confidence=float(confidence_match.group(1)) if confidence_match else 0.7,
            mathematical_model=model_match.group(1).strip() if model_match else "Domain-specific relationship",
            variables=variables_match.group(1).strip().split(', ') if variables_match else ["independent_var", "dependent_var"]
        )

    def collaborate_on_experiment_design(self, hypothesis: HypothesisResponse) -> Dict[str, Any]:
        """Provide theoretical guidance for experiment design"""
        
        domain = self._identify_scientific_domain(hypothesis.statement)
        domain_knowledge = self._get_domain_knowledge(domain, hypothesis.statement)
        
        design_query = f"""
        Hypothesis: {hypothesis.statement}
        Mathematical Model: {hypothesis.mathematical_model}
        Domain: {domain}
        Variables: {', '.join(hypothesis.variables)}
        
        Domain Knowledge: {json.dumps(domain_knowledge, indent=2)}
        
        Provide theoretical guidance for experimental design:
        
        1. CONTROL VARIABLES: What should be kept constant
        2. INDEPENDENT VARIABLES: What should be manipulated
        3. DEPENDENT VARIABLES: What should be measured
        4. EXPECTED RELATIONSHIPS: Theoretical predictions
        5. MEASUREMENT PRECISION: Required accuracy
        6. POTENTIAL CONFOUNDING FACTORS: What could interfere
        7. THEORETICAL PREDICTIONS: Expected quantitative results
        
        Consider the specific requirements of {domain} experiments.
        """
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are providing theoretical guidance for experimental design."),
            ("human", "{input}")
        ])
        
        chain = prompt | self.llm | StrOutputParser()
        result = chain.invoke({"input": design_query})
        
        return {
            "theoretical_guidance": result,
            "domain": domain,
            "predicted_parameters": self._generate_predicted_parameters(hypothesis, domain),
            "mathematical_model": hypothesis.mathematical_model,
            "knowledge_base_used": domain_knowledge,
            "literature_basis": self._perform_literature_review(hypothesis.statement, domain)
        }
    
    def _generate_predicted_parameters(self, hypothesis: HypothesisResponse, domain: str) -> Dict[str, Any]:
        """Generate domain-specific predicted parameters"""
        
        domain_params = {
            "physics": {
                "measurement_ranges": "Standard SI units",
                "precision_requirements": "±1% for quantitative measurements",
                "control_conditions": "Temperature, pressure, humidity"
            },
            "chemistry": {
                "measurement_ranges": "Concentration: 0.1-10 M, Temperature: 0-100°C",
                "precision_requirements": "±0.1 M for concentrations, ±1°C for temperature",
                "control_conditions": "pH, pressure, stirring rate"
            },
            "biology": {
                "measurement_ranges": "Growth rates, population counts, biomass",
                "precision_requirements": "±5% for biological measurements",
                "control_conditions": "Light, nutrients, temperature, pH"
            }
        }
        
        return domain_params.get(domain, {
            "measurement_ranges": "Domain-appropriate ranges",
            "precision_requirements": "Standard scientific precision",
            "control_conditions": "Relevant environmental factors"
        })