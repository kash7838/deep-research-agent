import json
import os
import pytest
from src.deep_research_agent.agent import DeepResearchAgent

def load_eval_dataset():
    path = os.path.join(os.path.dirname(__file__), "eval_dataset.json")
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return [{"topic": "Multi-agent frameworks comparison", "expected_keywords": ["framework"], "min_sources_cited": 2}]

@pytest.mark.parametrize("test_case", load_eval_dataset())
def test_deep_research_agent(test_case):
    topic = test_case["topic"]
    agent = DeepResearchAgent()
    
    # Run the agent pipeline
    report = agent.run_research(topic)
    
    # 1. Structural & Length Checks
    assert report is not None, "Report should not be empty"
    assert len(report) > 500, "Report is too short to be a deep research synthesis"
    
    # 2. Keyword Grounding Checks
    for keyword in test_case.get("expected_keywords", []):
        assert keyword.lower() in report.lower(), f"Expected keyword '{keyword}' missing from report."
        
    # 3. Citation Check (Ensures inline citations like [1] or URLs exist)
    assert "[" in report and "]" in report, "Report lacks inline citations."
    
    print(f"✅ Successfully evaluated research report for topic: '{topic}'")