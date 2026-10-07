# This module takes the search results from the search executor, cleans and strips out noise/boilerplate text or raw HTML, chunks the content logically, and prepares clean text bundles with source URLs for the synthesizer.
    
import re
from typing import List, Dict, Any
from bs4 import BeautifulSoup

class ContentExtractor:
    """
    Step 3: Cleans, parses, and structures raw search results and HTML data.
    """
    def __init__(self, max_chunk_length: int = 2000):
        self.max_chunk_length = max_chunk_length

    def clean_html_to_text(self, html_content: str) -> str:
        """
        Parses raw HTML and strips out scripts, styles, and unwanted tags, 
        returning clean readable plain text.
        """
        if not html_content:
            return ""
        
        # Use BeautifulSoup to parse and remove noise elements
        soup = BeautifulSoup(html_content, "html.parser")
        
        for element in soup(["script", "style", "nav", "footer", "header", "aside"]):
            element.decompose()
            
        text = soup.get_text(separator=" ")
        
        # Normalize whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    def extract_and_chunk_results(self, search_responses: List[Dict[str, Any]]) -> List[Dict[str, str]]:
        """
        Processes a list of Tavily search responses, cleans content, and structures 
        them into referenceable chunks with URL metadata.
        """
        processed_sources = []

        for response in search_responses:
            query = response.get("query", "")
            results = response.get("results", [])

            for item in results:
                url = item.get("url", "")
                title = item.get("title", "")
                raw_content = item.get("raw_content") or item.get("content", "")

                # Clean text
                clean_text = self.clean_html_to_text(raw_content)

                if not clean_text:
                    continue

                # Chunk content if it's too long to fit efficiently in a single LLM context window
                for i in range(0, len(clean_text), self.max_chunk_length):
                    chunk = clean_text[i:i + self.max_chunk_length]
                    processed_sources.append({
                        "query": query,
                        "title": title,
                        "url": url,
                        "content": chunk
                    })

        return processed_sources