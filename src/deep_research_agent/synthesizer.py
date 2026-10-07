# This module takes all the cleaned and chunked content collected from the search executor and extractor, maps them back to their exact source URLs, and instructs the LLM to write a comprehensive, professional Markdown research report complete with inline citations.

import json
from typing import List, Dict, Any
from openai import OpenAI
from config.settings import settings

class Synthesizer:
    """
    Step 4: Synthesizes extracted text chunks and exact citation URLs into a 
    cohesive, comprehensive Markdown research report.
    """
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.MODEL_NAME

    def synthesize_report(self, topic: str, extracted_sources: List[Dict[str, str]]) -> str:
        """
        Synthesizes the research report using the extracted chunks and links sources 
        back to their precise URLs.
        """
    
        # Limit total chunks to fit safely within context (e.g., max 25 chunks)
        max_chunks = 25
        limited_sources = extracted_sources[:max_chunks]
        
        # Format sources into an accessible text block for the LLM context window
        formatted_sources_text = ""
        for idx, source in enumerate(limited_sources, 1):
            formatted_sources_text += (
                f"Source [{idx}]\n"
                f"Title: {source.get('title', 'Untitled')}\n"
                f"URL: {source.get('url', 'No URL')}\n"
                f"Content: {source.get('content', '')}\n\n"
            )

        system_prompt = (
            "You are an elite research analyst and technical writer. Your task is to write a comprehensive, "
            "rigorous, and well-structured Markdown research report based *strictly* on the provided source material.\n"
            "Guidelines:\n"
            "1. Use clear Markdown headings (##, ###).\n"
            "2. Integrate precise facts, statistics, and insights from the sources.\n"
            "3. Cite sources inline using their reference numbers in brackets (e.g., [1], [2]) corresponding to the source index provided.\n"
            "4. Include a dedicated 'References' section at the very end listing all cited sources with their exact URLs.\n"
            "5. Maintain an objective, professional, and analytical tone. Avoid making up outside claims unsupported by the sources."
        )

        user_prompt = (
            f"Research Topic: {topic}\n\n"
            f"Here are the gathered research sources and extracted snippets:\n\n"
            f"{formatted_sources_text}\n\n"
            f"Please synthesize these into a comprehensive research report now."
        )

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=settings.TEMPERATURE,
        )

        return response.choices[0].message.content