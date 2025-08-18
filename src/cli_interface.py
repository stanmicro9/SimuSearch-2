import sys
import os
from typing import Optional
from src.workflows.scientific_workflow import ScientificWorkflow
from src.config import Config
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from fastapi import FastAPI
import uvicorn

app = FastAPI()

class ScientificCLI:
    """Command-line interface for the scientific investigation system"""
    
    def __init__(self):
        load_dotenv()
        if not Config.validate_config():
            sys.exit(1)
        
        self.llm = ChatGoogleGenerativeAI(
            model=Config.DEFAULT_LLM_MODEL,
            convert_system_message_to_human=True,
            google_api_key=Config.GOOGLE_API_KEY,
            temperature=Config.DEFAULT_TEMPERATURE
        )
        
        self.workflow = ScientificWorkflow(self.llm)
        
    def display_welcome(self):
        """Display welcome message and instructions"""
        print("🔬 Multi-Agent Scientific Investigation System")
        print("=" * 80)
        print("This system uses AI agents to conduct scientific investigations:")
        print("  📚 Theoretical Agent: Generates hypotheses and mathematical models")
        print("  🧪 Experimental Agent: Designs and executes simulated experiments")  
        print("  📊 Collector Agent: Analyzes results and draws conclusions")
        print("=" * 80)
    
        return InvestigationResponse(
            question=result.scientific_question,
            hypothesis=result.hypothesis.statement,
            experimental_results=result.experimental_results.conclusion,
            final_conclusion=result.final_conclusion,
            confidence=result.experimental_results.confidence,
            future_research=result.future_research
        )
        
    #except Exception as e:
     #   raise HTTPException(status_code=500, detail=f"Investigation failed: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "system": "scientific-agents"}

@app.get("/domains")
async def get_supported_domains():
    """Get list of supported scientific domains"""
    return {
        "domains": [
            "physics",
            "chemistry", 
            "biology",
            "environmental",
            "engineering",
            "medicine"
        ]
    }

if __name__ == "__main__":
    uvicorn.run("src.cli_interface:app", host="0.0.0.0", port=8000, reload=True)