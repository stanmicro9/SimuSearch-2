# Multi-Agent Scientific Investigation System

## Overview

This system implements a multi-agent AI framework for conducting automated scientific investigations across multiple domains. The system uses three specialized agents that collaborate to:

1. **Theoretical Agent**: Generates hypotheses and mathematical models
2. **Experimental Agent**: Designs and executes simulated experiments  
3. **Collector Agent**: Analyzes results and synthesizes conclusions

## Features

- 🔬 **Multi-domain support**: Physics, Chemistry, Biology, Environmental Science, Engineering, Medicine
- 🤖 **Agent collaboration**: Structured communication using LangChain
- 🧪 **Simulation environments**: Generic simulators for various scientific domains
- 📊 **Statistical analysis**: Correlation analysis, confidence scoring, error estimation
- 📚 **Literature integration**: Theoretical knowledge base with domain-specific principles
- 🎯 **Dynamic adaptation**: Automatically adapts to user's scientific question

## Installation

1. Clone the repository
2. Create virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env file and add your GOOGLE_API_KEY
   ```

## Usage

### Interactive Mode
```bash
python -m src.main
```

### Command Line Mode
```bash
python -m src.main "How does temperature affect chemical reaction rates?"
```

### Programmatic Usage
```python
from src.workflows.scientific_workflow import ScientificWorkflow
from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key="your_key")
workflow = ScientificWorkflow(llm)

result = workflow.investigate("Your scientific question here")
print(result.final_conclusion)
```

## System Architecture

```
User Question → Theoretical Agent → Experimental Agent → Collector Agent → Final Analysis
                      ↓                    ↓                   ↓
                 Hypothesis         Experiment Design     Statistical Analysis
                Mathematical       Simulation Results    Theory vs Experiment
                   Model              Data Collection       Conclusions
```

## Agent Responsibilities

### Theoretical Agent
- Domain identification and knowledge retrieval
- Hypothesis generation based on scientific principles
- Mathematical model creation
- Literature review simulation
- Experimental design guidance

### Experimental Agent  
- Domain-specific experiment design
- Parameter optimization for each scientific field
- Simulation execution with realistic noise models
- Statistical data analysis
- Results interpretation

### Collector Agent
- Cross-agent data aggregation
- Theory-experiment comparison
- Confidence assessment
- Future research recommendations
- Final conclusion synthesis

## Communication System

The agents communicate through a structured LangChain-based hub that:
- Maintains conversation history
- Provides structured message passing
- Enables context sharing
- Supports workflow coordination

## Simulation Capabilities

The system includes specialized simulators for:

- **Physics**: Thermal effects, mechanical systems, electromagnetic phenomena
- **Chemistry**: Reaction kinetics, thermodynamics, equilibrium systems
- **Biology**: Population dynamics, growth models, ecological interactions
- **Environmental**: Climate effects, pollution impact, ecosystem responses
- **Engineering**: Material properties, efficiency optimization
- **Medicine**: Pharmacokinetics, dose-response relationships

## Example Investigations

1. **Temperature and Reaction Rates**: Investigates Arrhenius equation
2. **Light and Photosynthesis**: Models Michaelis-Menten kinetics
3. **Material Stress-Strain**: Simulates Hooke's law and yield behavior
4. **Drug Dosage Effects**: Models Hill equation dose-response
5. **Environmental Pollution**: Analyzes ecosystem impact relationships

## Configuration

Edit `src/config.py` to customize:
- Model parameters
- Simulation precision
- Domain-specific settings
- Timeout values

## Testing

Run the test suite:
```bash
pytest tests/ -v
```

## Error Handling

The system includes comprehensive error handling:
- Configuration validation
- Agent communication failures
- Simulation errors
- Graceful degradation with fallback modes

## Future Enhancements

- Integration with real experimental data APIs
- Advanced visualization capabilities
- Machine learning model integration
- Multi-hypothesis testing
- Collaborative agent competition modes

## Troubleshooting

Common issues:
1. **API Key Error**: Ensure GOOGLE_API_KEY is set in .env file
2. **Import Errors**: Check all dependencies are installed
3. **Simulation Errors**: Verify parameter ranges are reasonable
4. **Memory Issues**: Reduce simulation time steps or sample sizes

## Contributing

1. Fork the repository
2. Create feature branch
3. Add tests for new functionality
4. Submit pull request