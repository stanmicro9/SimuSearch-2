from src.agents.core.theoretical_agent import TheoreticalAgent
from src.agents.core.experimental_agent import ExperimentalAgent
from src.agents.collector_agent import CollectorAgent
from src.communication.agent_communication import AgentCommunicationHub
from src.workflows.scientific_workflow import ScientificWorkflow
from src.config import Config
from src.utils.logging_config import ScientificLogger
from src.utils.performance_monitor import PerformanceMonitor
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os
import sys
import time

def main():
    """Enhanced main function with comprehensive features"""
    
    # Setup
    load_dotenv()
    logger = ScientificLogger()
    monitor = PerformanceMonitor()
    
    # Validate configuration
    if not Config.validate_config():
        print("❌ Configuration validation failed. Please check your .env file.")
        sys.exit(1)
    
    # Initialize LLM
    try:
        llm = ChatGoogleGenerativeAI(
            model=Config.DEFAULT_LLM_MODEL,
            convert_system_message_to_human=True,
            google_api_key=Config.GOOGLE_API_KEY,
            temperature=Config.DEFAULT_TEMPERATURE
        )
        logger.logger.info("✅ LLM initialized successfully")
    except Exception as e:
        logger.logger.error(f"❌ LLM initialization failed: {str(e)}")
        sys.exit(1)
    
    # Initialize workflow
    workflow = ScientificWorkflow(llm)
    monitor.start_monitoring()
    
    # Display system information
    print("🔬 Multi-Agent Scientific Investigation System v1.0")
    print("=" * 80)
    print("🤖 Agents: Theoretical, Experimental, Collector")
    print("🌐 Domains: Physics, Chemistry, Biology, Environmental, Engineering, Medicine")
    print("🔧 Powered by: LangChain + Google Gemini")
    print("=" * 80)
    
    # Get user question
    if len(sys.argv) > 1:
        # Command line argument
        scientific_question = " ".join(sys.argv[1:])
    else:
        # Interactive input
        print("\n🔍 Enter your scientific question to investigate:")
        print("\nExample questions:")
        print("  • How does temperature affect the rate of chemical reactions?")
        print("  • What factors influence the efficiency of photosynthesis?")
        print("  • How do different materials affect sound absorption?")
        print("  • What is the relationship between exercise intensity and heart rate?")
        print("  • How does air pressure affect the boiling point of water?")
        print("=" * 80)
        
        scientific_question = input("❓ Your scientific question: ").strip()
        
        if not scientific_question:
            print("❌ No question provided. Exiting.")
            sys.exit(1)
    
    # Log investigation start
    logger.log_agent_action("System", "Investigation Started", scientific_question)
    
    print(f"\n🎯 Investigating: {scientific_question}")
    print("=" * 80)
    
    # Run investigation with performance monitoring
    start_time = time.time()
    
    try:
        with monitor.measure_performance("complete_investigation", "workflow"):
            final_analysis = workflow.investigate(scientific_question)
        
        execution_time = time.time() - start_time
        
        # Display results
        print("\n" + "=" * 80)
        print("🎯 SCIENTIFIC INVESTIGATION COMPLETE")
        print("=" * 80)
        print(f"⏱️  Total Execution Time: {execution_time:.1f} seconds")
        print(f"❓ Question: {final_analysis.scientific_question}")
        
        print(f"\n📚 THEORETICAL ANALYSIS:")
        print(f"  💡 Hypothesis: {final_analysis.hypothesis.statement}")
        print(f"  🎯 Confidence: {final_analysis.hypothesis.confidence:.1%}")
        print(f"  🧮 Mathematical Model: {final_analysis.hypothesis.mathematical_model}")
        print(f"  🔬 Variables: {', '.join(final_analysis.hypothesis.variables)}")
        
        print(f"\n🧪 EXPERIMENTAL RESULTS:")
        print(f"  📊 Analysis: {final_analysis.experimental_results.analysis}")
        print(f"  📋 Conclusion: {final_analysis.experimental_results.conclusion}")
        print(f"  ✅ Supports Hypothesis: {final_analysis.experimental_results.supports_hypothesis}")
        print(f"  🎯 Confidence: {final_analysis.experimental_results.confidence:.1%}")
        
        print(f"\n🤝 THEORY vs EXPERIMENT:")
        print(f"  {final_analysis.theoretical_vs_experimental}")
        
        print(f"\n🎯 FINAL CONCLUSION:")
        print(f"  {final_analysis.final_conclusion}")
        
        print(f"\n🔮 FUTURE RESEARCH DIRECTIONS:")
        for i, direction in enumerate(final_analysis.future_research, 1):
            print(f"  {i}. {direction}")
        
        # Performance summary
        performance_report = monitor.get_performance_report()
        print(f"\n📈 PERFORMANCE SUMMARY:")
        print(f"  🕒 Total Operations: {performance_report.get('operations_count', 0)}")
        print(f"  💾 Avg Memory: {performance_report.get('average_memory_usage_mb', 0):.1f} MB")
        print(f"  🖥️  Avg CPU: {performance_report.get('average_cpu_usage', 0):.1f}%")
        
        logger.log_agent_action("System", "Investigation Completed", f"Success in {execution_time:.1f}s")
        
    except KeyboardInterrupt:
        print("\n⚠️  Investigation interrupted by user.")
        logger.logger.warning("Investigation interrupted by user")
        
    except Exception as e:
        print(f"\n❌ Investigation failed: {str(e)}")
        logger.logger.error(f"Investigation failed: {str(e)}")
        
        # Display helpful error information
        print("\n🔧 Troubleshooting:")
        print("  1. Check your .env file contains GOOGLE_API_KEY")
        print("  2. Verify your API key is valid and has quota")
        print("  3. Check your internet connection")
        print("  4. Try a simpler scientific question")
        
    finally:
        monitor.stop_monitoring()
        print(f"\n👋 Thank you for using the Scientific Investigation System!")

if __name__ == "__main__":
    main()