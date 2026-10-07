import sys
import argparse
from src.deep_research_agent.agent import DeepResearchAgent
from src.deep_research_agent.utils import save_research_report

def main():
    parser = argparse.ArgumentParser(description="Autonomous Deep Research Agent CLI")
    parser.add_argument(
        "--topic", 
        type=str, 
        required=True, 
        help="The research topic or question you want the agent to investigate."
    )
    args = parser.parse_args()

    topic = args.topic
    print(f"\n🚀 Initializing Deep Research Agent for topic: '{topic}'...\n")

    try:
        # Initialize and run the agent
        agent = DeepResearchAgent()
        report = agent.run_research(topic)

        # Save the report using utils
        saved_path = save_research_report(topic, report)

        print("\n" + "="*50)
        print("✨ RESEARCH REPORT SUCCESSFULLY GENERATED ✨")
        print("="*50)
        print(report[:1500] + "\n\n... [Truncated for console display] ...\n")
        print("="*50)
        print(f"📁 Full report saved locally to: {saved_path}")
        print("="*50 + "\n")

    except Exception as e:
        print(f"\n❌ Error during research execution: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()