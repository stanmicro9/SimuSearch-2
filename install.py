"""
Installation and setup script for the scientific investigation system
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
from typing import Optional
from src.cli_interface import ScientificCLI

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        sys.exit(1)
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")

def create_directory_structure():
    """Create necessary directories"""
    directories = [
        "logs",
        "results", 
        "data",
        "tests",
        "docs",
        "benchmarks"
    ]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"📁 Created directory: {directory}")

def setup_environment():
    """Setup environment file"""
    if not os.path.exists(".env"):
        shutil.copy(".env.example", ".env")
        print("📄 Created .env file from template")
        print("⚠️  Please edit .env file and add your GOOGLE_API_KEY")
    else:
        print("✅ .env file already exists")

def install_dependencies():
    """Install Python dependencies"""
    try:
        print("📦 Installing dependencies...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        sys.exit(1)

def run_tests():
    """Run basic system tests"""
    try:
        print("🧪 Running system tests...")
        subprocess.check_call([sys.executable, "-m", "pytest", "tests/", "-v"])
        print("✅ All tests passed")
    except subprocess.CalledProcessError:
        print("⚠️  Some tests failed - system may still work")
    except FileNotFoundError:
        print("⚠️  pytest not found - skipping tests")

def main():
    """Main installation script"""
    print("🚀 Scientific Investigation System - Installation")
    print("=" * 60)
    
    check_python_version()
    create_directory_structure()
    install_dependencies()
    setup_environment()
    
    print("\n" + "=" * 60)
    print("✅ Installation Complete!")
    print("=" * 60)
    print("Next steps:")
    print("1. Edit .env file with your GOOGLE_API_KEY")
    print("2. Run: python -m src.main")
    print("3. Enter your scientific question")
    print("\nFor help: python run_system.py --help")

if __name__ == "__main__":
    main()
    
    def _is_scientific_question(self, question: str) -> bool:
        """Validate if the question is suitable for scientific investigation"""
        question_lower = question.lower()
        
        # Check for scientific question indicators
        scientific_indicators = [
            "how does", "what is the effect", "what factors", "relationship between",
            "influence", "affect", "impact", "cause", "correlation", "depend"
        ]
        
        question_words = ["how", "what", "why", "which", "when", "where"]
        
        has_scientific_structure = any(indicator in question_lower for indicator in scientific_indicators)
        has_question_word = any(word in question_lower for word in question_words)
        
        return has_scientific_structure or has_question_word
    
    def run_investigation(self, question: str) -> Optional[object]:
        """Run the complete scientific investigation"""
        
        print(f"\n🎯 Starting investigation: {question}")
        print("=" * 80)
        
        try:
            # Run investigation workflow
            result = self.workflow.investigate(question)
            return result
            
        except KeyboardInterrupt:
            print("\n⚠️  Investigation interrupted by user.")
            return None
        except Exception as e:
            print(f"\n❌ Investigation failed: {str(e)}")
            print("🔧 Please check your configuration and try again.")
            return None
    
    def display_results(self, analysis):
        """Display investigation results in a formatted way"""
        if not analysis:
            return
        
        print("\n" + "=" * 80)
        print("🎯 SCIENTIFIC INVESTIGATION RESULTS")
        print("=" * 80)
        
        # Question and hypothesis
        print(f"❓ Research Question: {analysis.scientific_question}")
        print(f"\n💡 Hypothesis: {analysis.hypothesis.statement}")
        print(f"📊 Theoretical Confidence: {analysis.hypothesis.confidence:.1%}")
        print(f"🧮 Mathematical Model: {analysis.hypothesis.mathematical_model}")
        
        # Experimental results
        print(f"\n🔬 Experimental Findings:")
        print(f"  ✅ Supports Hypothesis: {analysis.experimental_results.supports_hypothesis}")
        print(f"  📈 Experimental Confidence: {analysis.experimental_results.confidence:.1%}")
        print(f"  📋 Analysis: {analysis.experimental_results.analysis}")
        
        # Final conclusion
        print(f"\n🎯 Final Scientific Conclusion:")
        print(f"  {analysis.final_conclusion}")
        
        print(f"\n🤝 Theory vs Experiment Agreement:")
        print(f"  {analysis.theoretical_vs_experimental}")
        
        # Future research
        print(f"\n🔮 Recommended Future Research:")
        for i, direction in enumerate(analysis.future_research, 1):
            print(f"  {i}. {direction}")
        
        print("\n" + "=" * 80)
    
    def run_interactive_mode(self):
        """Run interactive mode allowing multiple investigations"""
        
        self.display_welcome()
        
        while True:
            try:
                question = self.get_user_question()
                result = self.run_investigation(question)
                
                if result:
                    self.display_results(result)
                
                print("\n" + "=" * 40)
                choice = input("🔄 Run another investigation? (y/n): ").strip().lower()
                
                if choice not in ['y', 'yes']:
                    print("👋 Thank you for using the Scientific Investigation System!")
                    break
                    
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ System error: {str(e)}")
                choice = input("🔄 Continue despite error? (y/n): ").strip().lower()
                if choice not in ['y', 'yes']:
                    break

def main():
    """Main CLI entry point"""
    cli = ScientificCLI()
    
    if len(sys.argv) > 1:
        # Command line argument provided
        question = " ".join(sys.argv[1:])
        cli.display_welcome()
        result = cli.run_investigation(question)
        if result:
            cli.display_results(result)
    #else:
        # Interactive mode
        #cli.run_interactive_mode()

if __name__ == "__main__":
    main()