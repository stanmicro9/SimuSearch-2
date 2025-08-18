"""
Comprehensive system runner with multiple execution modes
"""

import sys
import argparse
from src.main import main
from src.cli_interface import ScientificCLI
from src.config import Config
from src.utils.logging_config import ScientificLogger
import os

def setup_logging():
    """Setup system logging"""
    os.makedirs("logs", exist_ok=True)
    logger = ScientificLogger()
    return logger

def run_batch_mode(questions_file: str):
    """Run investigations from a file of questions"""
    
    logger = setup_logging()
    
    try:
        with open(questions_file, 'r') as f:
            questions = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        
        logger.logger.info(f"Running batch mode with {len(questions)} questions")
        
        from src.workflows.scientific_workflow import ScientificWorkflow
        from langchain_google_genai import ChatGoogleGenerativeAI
        
        llm = ChatGoogleGenerativeAI(
            model=Config.DEFAULT_LLM_MODEL,
            google_api_key=Config.GOOGLE_API_KEY
        )
        
        workflow = ScientificWorkflow(llm)
        
        results = []
        for i, question in enumerate(questions, 1):
            print(f"\n🔬 Investigation {i}/{len(questions)}: {question}")
            
            try:
                result = workflow.investigate(question)
                results.append((question, result))
                logger.logger.info(f"Completed investigation {i}: {question}")
                
            except Exception as e:
                logger.logger.error(f"Failed investigation {i}: {str(e)}")
                results.append((question, None))
        
        # Save batch results
        save_batch_results(results)
        
    except FileNotFoundError:
        print(f"❌ Questions file not found: {questions_file}")
    except Exception as e:
        print(f"❌ Batch mode error: {str(e)}")

def save_batch_results(results: List[tuple]):
    """Save batch investigation results to file"""
    
    os.makedirs("results", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"results/batch_results_{timestamp}.txt"
    
    with open(filename, 'w') as f:
        f.write("Multi-Agent Scientific Investigation - Batch Results\n")
        f.write("=" * 80 + "\n\n")
        
        for i, (question, result) in enumerate(results, 1):
            f.write(f"Investigation {i}: {question}\n")
            f.write("-" * 60 + "\n")
            
            if result:
                f.write(f"Hypothesis: {result.hypothesis.statement}\n")
                f.write(f"Conclusion: {result.final_conclusion}\n")
                f.write(f"Supports Hypothesis: {result.experimental_results.supports_hypothesis}\n")
            else:
                f.write("Status: FAILED\n")
            
            f.write("\n" + "=" * 80 + "\n\n")
    
    print(f"📄 Batch results saved to: {filename}")

def main_runner():
    """Main entry point with argument parsing"""
    
    parser = argparse.ArgumentParser(description="Multi-Agent Scientific Investigation System")
    parser.add_argument("question", nargs="?", help="Scientific question to investigate")
    parser.add_argument("--interactive", "-i", action="store_true", help="Run in interactive mode")
    parser.add_argument("--batch", "-b", help="Run batch mode with questions file")
    parser.add_argument("--config-check", action="store_true", help="Check configuration")
    parser.add_argument("--examples", action="store_true", help="Show example questions")
    parser.add_argument("--benchmark", action="store_true", help="Run performance benchmark")
    
    args = parser.parse_args()
    
    # Configuration check
    if args.config_check:
        Config.validate_config()
        return
    
    # Show examples
    if args.examples:
        show_example_questions()
        return
    
    # Performance benchmark
    if args.benchmark:
        from benchmarks.benchmark_agents import benchmark_investigation_speed
        benchmark_investigation_speed()
        return
    
    # Batch mode
    if args.batch:
        run_batch_mode(args.batch)
        return
    
    # Interactive mode
    if args.interactive:
        cli = ScientificCLI()
        cli.run_interactive_mode()
        return
    
    # Single question mode
    if args.question:
        from src.workflows.scientific_workflow import ScientificWorkflow
        from langchain_google_genai import ChatGoogleGenerativeAI
        
        llm = ChatGoogleGenerativeAI(
            model=Config.DEFAULT_LLM_MODEL,
            google_api_key=Config.GOOGLE_API_KEY
        )
        
        workflow = ScientificWorkflow(llm)
        result = workflow.investigate(args.question)
        
        if result:
            print(f"\n🎯 Question: {result.scientific_question}")
            print(f"💡 Hypothesis: {result.hypothesis.statement}")
            print(f"🔬 Conclusion: {result.final_conclusion}")
        return
    
    # Default: run main
    main()

def show_example_questions():
    """Display example questions for different domains"""
    
    examples = {
        "Physics": [
            "How does temperature affect electrical resistance?",
            "What is the relationship between force and acceleration?",
            "How does frequency affect wave energy?",
            "What factors influence pendulum oscillation period?"
        ],
        "Chemistry": [
            "How does concentration affect reaction rate?",
            "What is the effect of temperature on chemical equilibrium?",
            "How does pH affect enzyme activity?",
            "What factors influence catalyst effectiveness?"
        ],
        "Biology": [
            "How does light intensity affect photosynthesis rate?",
            "What factors influence population growth?",
            "How does temperature affect enzyme function?",
            "What is the relationship between nutrient availability and plant growth?"
        ],
        "Environmental Science": [
            "How does air pollution affect ecosystem health?",
            "What factors influence carbon sequestration?",
            "How does deforestation affect local climate?",
            "What is the impact of ocean acidification on marine life?"
        ],
        "Engineering": [
            "How does material thickness affect structural strength?",
            "What factors influence solar panel efficiency?",
            "How does aerodynamics affect fuel consumption?",
            "What is the relationship between design parameters and performance?"
        ]
    }
    
    print("🔬 Example Scientific Questions by Domain")
    print("=" * 80)
    
    for domain, questions in examples.items():
        print(f"\n{domain}:")
        for i, question in enumerate(questions, 1):
            print(f"  {i}. {question}")
    
    print("\n" + "=" * 80)
    print("💡 Usage: python run_system.py \"Your question here\"")

if __name__ == "__main__":
    main_runner()