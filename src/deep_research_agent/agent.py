# This script connects all four modular components we built (Planner, SearchExecutor, ContentExtractor, and Synthesizer) into a seamless end-to-end autonomous research workflow.

import logging
from typing import Dict, Any
from src.deep_research_agent.planner import Planner
from src.deep_research_agent.search_executor import SearchExecutor
from src.deep_research_agent.extractor import ContentExtractor
from src.deep_research_agent.synthesizer import Synthesizer

# Configure basic logging to track pipeline progress
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("DeepResearchAgent")

class DeepResearchAgent:
    """
    Orchestration hub that coordinates the Planner, SearchExecutor, 
    ContentExtractor, and Synthesizer into an end-to-end research pipeline.
    """
    def __init__(self):
        logger.info("Initializing Deep Research Agent components...")
        self.planner = Planner()
        self.search_executor = SearchExecutor()
        self.extractor = ContentExtractor()
        self.synthesizer = Synthesizer()

    def run_research(self, topic: str) -> str:
        """
        Executes the full autonomous deep research workflow for a given topic.
        """
        logger.info(f"=== Starting Deep Research on Topic: '{topic}' ===")

        # Step 1: Generate Research Plan & Sub-Queries
        logger.info("Step 1: Deconstructing topic into targeted sub-queries (Planner)...")
        research_plan = self.planner.generate_plan(topic)
        queries = [sq.query for sq in research_plan.sub_queries]
        logger.info(f"Generated {len(queries)} sub-queries:")
        for idx, q in enumerate(queries, 1):
            logger.info(f"  {idx}. {q}")

        # Step 2: Execute Parallel Searches via Tavily
        logger.info("Step 2: Executing concurrent searches across sub-queries (SearchExecutor)...")
        search_responses = self.search_executor.execute_searches(queries)
        logger.info(f"Retrieved search data from {len(search_responses)} query executions.")

        # Step 3: Extract and Chunk Content
        logger.info("Step 3: Cleaning HTML, extracting text, and building source chunks (ContentExtractor)...")
        extracted_sources = self.extractor.extract_and_chunk_results(search_responses)
        logger.info(f"Extracted and prepared {len(extracted_sources)} clean text chunks with source metadata.")

        # Step 4: Synthesize Final Markdown Report
        logger.info("Step 4: Synthesizing final comprehensive research report with inline citations (Synthesizer)...")
        report = self.synthesizer.synthesize_report(topic, extracted_sources)
        logger.info("=== Deep Research Completed Successfully ===")

        return report