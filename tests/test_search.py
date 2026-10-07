import pytest
from unittest.mock import MagicMock, patch
from src.deep_research_agent.search_executor import SearchExecutor

@patch("src.deep_research_agent.search_executor.TavilyClient")
def test_search_executor_parallel_calls(mock_tavily_class):
    # Arrange: Mock Tavily client search response
    mock_client = MagicMock()
    mock_tavily_class.return_value = mock_client

    mock_client.search.return_value = {
        "results": [
            {"title": "Test Result 1", "url": "https://example.com/1", "content": "Sample content 1"}
        ]
    }

    executor = SearchExecutor()
    queries = ["query one", "query two"]

    # Act: Execute searches
    results = executor.execute_searches(queries)

    # Assert: Check that search was called for each query and results are structured properly
    assert len(results) == 2
    assert results[0]["query"] == "query one"
    assert len(results[0]["results"]) == 1
    assert results[0]["results"][0]["title"] == "Test Result 1"
    assert mock_client.search.call_count == 2