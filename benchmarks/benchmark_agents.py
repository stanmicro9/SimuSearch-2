#Performance benchmarking
import time
import statistics
from src.workflows.scientific_workflow import ScientificWorkflow
from langchain_google_genai import ChatGoogleGenerativeAI
from src.config import Config
from dotenv import load_dotenv

def benchmark_investigation_speed():
    """Benchmark investigation speed across domains"""
    
    load_dotenv()
    
    if not Config.GOOGLE_API_KEY:
        print("❌ No API key found - using mock timing")
        return
    
    llm = ChatGoogleGenerativeAI(
        model=Config.DEFAULT_LLM_MODEL,
        google_api_key=Config.GOOGLE_API_KEY,
        temperature=0.1
    )
    
    workflow = ScientificWorkflow(llm)
    
    test_questions = [
        ("Physics", "How does force affect acceleration?"),
        ("Chemistry", "How does temperature affect reaction rate?"),
        ("Biology", "How does light affect photosynthesis?"),
        ("Environmental", "How does pollution affect air quality?")
    ]
    
    results = {}
    
    print("🏃‍♂️ Benchmarking Scientific Investigation Speed")
    print("=" * 60)
    
    for domain, question in test_questions:
        print(f"\n🔬 Testing {domain}: {question}")
        
        times = []
        for run in range(3):  # 3 runs per domain
            start_time = time.time()
            
            try:
                result = workflow.investigate(question)
                end_time = time.time()
                
                if result:
                    times.append(end_time - start_time)
                    print(f"  ✅ Run {run + 1}: {times[-1]:.1f}s")
                else:
                    print(f"  ❌ Run {run + 1}: Failed")
                    
            except Exception as e:
                print(f"  ❌ Run {run + 1}: Error - {str(e)}")
        
        if times:
            avg_time = statistics.mean(times)
            std_time = statistics.stdev(times) if len(times) > 1 else 0
            results[domain] = {
                "average_time": avg_time,
                "std_deviation": std_time,
                "successful_runs": len(times)
            }
            print(f"  📊 Average: {avg_time:.1f}s ± {std_time:.1f}s")
    
    print("\n" + "=" * 60)
    print("📈 BENCHMARK SUMMARY")
    print("=" * 60)
    
    for domain, stats in results.items():
        print(f"{domain:15} | {stats['average_time']:6.1f}s ± {stats['std_deviation']:4.1f}s | {stats['successful_runs']}/3 success")

if __name__ == "__main__":
    benchmark_investigation_speed()