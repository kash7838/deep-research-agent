import time
import logging
from typing import Optional
from .rag import ResearchRAG
from .planner import Planner
from .search_executor import SearchExecutor
from .extractor import ContentExtractor
from .synthesizer import Synthesizer

logger = logging.getLogger("DeepResearchAgent")

class DeepResearchAgent:
    """
    Orchestrates the autonomous deep research pipeline:
    RAG check -> Planning -> Searching -> Extracting -> Synthesizing -> Storing in ChromaDB.
    """
    def __init__(self):
        self.rag = ResearchRAG()
        self.planner = Planner()
        self.search_executor = SearchExecutor()
        self.extractor = ContentExtractor()
        self.synthesizer = Synthesizer()

    def estimate_tokens(self, text: str) -> int:
        """Rough token estimator (approx 4 chars per token) to enforce budget."""
        return len(text) // 4

    def run_research(self, topic: str) -> str:
        # 1. Enforce strict token safeguard on incoming topic
        if self.estimate_tokens(topic) > 100:
            topic = topic[:400]
            logger.info("Topic exceeded token limit and was truncated.")

        # 2. Query local ChromaDB RAG vector store for prior context
        relevant_docs = self.rag.query_documents(topic, n_results=2)
        
        if relevant_docs:
            logger.info(f"Found {len(relevant_docs)} relevant local document(s) in ChromaDB.")
            context_str = "\n".join(relevant_docs)
            rag_context_header = f"### Prior Knowledge Retrieved from Local ChromaDB RAG:\n{context_str}\n\n"
        else:
            logger.info("No prior context found in ChromaDB. Executing fresh research pipeline.")
            rag_context_header = ""

        try:
            # 3. Step 1: Generate research plan (Sub-queries)
            logger.info(f"Generating research plan for topic: '{topic}'")
            plan = self.planner.generate_plan(topic)
            sub_query_strings = [sq.query for sq in plan.sub_queries]

            # 4. Step 2: Execute parallel web searches via Tavily
            logger.info(f"Executing {len(sub_query_strings)} parallel searches...")
            search_responses = self.search_executor.execute_searches(sub_query_strings)

            # 5. Step 3: Extract and chunk content
            logger.info("Extracting and cleaning search results...")
            extracted_sources = self.extractor.extract_and_chunk_results(search_responses)

            if not extracted_sources:
                return f"### Research Failed\nCould not extract valid text content from search results for topic: **{topic}**."

            # 6. Step 4: Synthesize final comprehensive report
            logger.info("Synthesizing final research report via LLM...")
            report_body = self.synthesizer.synthesize_report(topic, extracted_sources)

            # Combine with RAG context header if prior docs existed
            final_report = f"{rag_context_header}{report_body}"

        except Exception as e:
            logger.error(f"Error during deep research pipeline execution: {e}")
            raise e

        # 7. Step 5: Save the new report directly into ChromaDB RAG memory
        doc_id = f"research_{int(time.time())}"
        self.rag.add_document(
            doc_id=doc_id, 
            text=final_report, 
            metadata={"topic": topic, "timestamp": str(time.time())}
        )
        logger.info(f"Successfully saved research report into ChromaDB (ID: {doc_id})")

        return final_report