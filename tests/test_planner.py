import pytest
import json
from unittest.mock import MagicMock, patch
from src.deep_research_agent.planner import Planner, ResearchPlan

@patch("src.deep_research_agent.planner.OpenAI")
def test_planner_generates_valid_plan(mock_openai_class):
    # Arrange: Mock the OpenAI client and response structure
    mock_client = MagicMock()
    mock_openai_class.return_value = mock_client

    # Create a valid JSON string representing the ResearchPlan structure
    sample_plan_data = {
        "main_topic": "Test AI Topic",
        "sub_queries": [
            {"query": "Sub-query 1 about AI", "rationale": "Test rationale 1"},
            {"query": "Sub-query 2 about frameworks", "rationale": "Test rationale 2"}
        ]
    }
    
    # Configure mock chat completion response to return this JSON string inside message.content
    mock_response = MagicMock()
    mock_response.choices[0].message.content = json.dumps(sample_plan_data)
    mock_client.chat.completions.create.return_value = mock_response

    # Act: Instantiate Planner and generate a plan
    planner = Planner()
    plan = planner.generate_plan("Test AI Topic")

    # Assert: Verify output structure
    assert isinstance(plan, ResearchPlan)
    assert len(plan.sub_queries) == 2
    assert plan.sub_queries[0].query == "Sub-query 1 about AI"
    assert plan.sub_queries[1].rationale == "Test rationale 2"