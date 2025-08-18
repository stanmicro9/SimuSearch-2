# import os
# from dotenv import load_dotenv

# load_dotenv()

# # Load API key from environment
# api_key = os.getenv("GOOGLE_API_KEY")

# # Configuration constants
# DEFAULT_LLM_MODEL = "gemini-2.0-flash"
# DEFAULT_TEMPERATURE = 0.1

import os
from dotenv import load_dotenv
from typing import Dict, Any

load_dotenv()

class Config:
    """Enhanced configuration management"""
    
    # API Configuration
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    
    # Model Configuration
    DEFAULT_LLM_MODEL = "gemini-2.0-flash"
    DEFAULT_TEMPERATURE = 0.1
    MAX_TOKENS = 4096
    
    # Agent Configuration
    AGENT_TIMEOUT = 120  # seconds
    MAX_RETRY_ATTEMPTS = 3
    
    # Simulation Configuration
    DEFAULT_SIMULATION_STEPS = 1000
    DEFAULT_TIME_STEP = 0.01
    
    # Domain-specific settings
    DOMAIN_SETTINGS = {
        "physics": {
            "precision": 0.001,
            "noise_level": 0.02,
            "default_units": "SI"
        },
        "chemistry": {
            "precision": 0.01,
            "noise_level": 0.05,
            "default_units": "molarity"
        },
        "biology": {
            "precision": 0.1,
            "noise_level": 0.15,
            "default_units": "relative"
        },
        "environmental": {
            "precision": 0.05,
            "noise_level": 0.10,
            "default_units": "standard"
        }
    }
    
    @classmethod
    def validate_config(cls) -> bool:
        """Validate configuration settings"""
        if not cls.GOOGLE_API_KEY:
            print("❌ GOOGLE_API_KEY not found in environment variables")
            return False
        
        print("✅ Configuration validated successfully")
        return True
    
    @classmethod
    def get_domain_config(cls, domain: str) -> Dict[str, Any]:
        """Get configuration for specific domain"""
        return cls.DOMAIN_SETTINGS.get(domain, cls.DOMAIN_SETTINGS["general"])
