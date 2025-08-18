"""
Example usage script for the scientific investigation system
"""

from src.main import main
from src.config import Config
import sys

def run_example_investigations():
    """Run several example investigations to demonstrate capabilities"""
    
    if not Config.validate_config():
        print("Configuration validation failed. Please check your .env file.")
        return
    
    example_questions = [
        "How does temperature affect the rate of enzyme reactions?",
        "What is the relationship between solar panel angle and energy output?",
        "How do different light wavelengths affect plant photosynthesis?",
        "What factors influence the efficiency of wind turbines?",
        "How does pH affect the solubility of different compounds?"
    ]
    
    print("🔬 Scientific Investigation System - Example Runs")
    print("=" * 80)
    
    for i, question in enumerate(example_questions, 1):
        print(f"\n🧪 Example {i}: {question}")
        print("-" * 60)
        
        try:
            # This would run the investigation
            # For demo purposes, we'll just show the setup
            print(f"✅ Question prepared: {question}")
            print("   🔄 Would run: Theory → Experiment → Analysis → Conclusion")
            
        except Exception as e:
            print(f"❌ Error in example {i}: {str(e)}")
    
    print("\n" + "=" * 80)
    print("💡 To run your own investigation, execute: python -m src.main")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--examples":
        run_example_investigations()
    else:
        main()