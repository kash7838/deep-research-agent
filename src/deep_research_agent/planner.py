# This module takes a high-level research topic and uses structured LLM output (via Pydantic) to break it down into focused sub-questions and search intents.

import json
from typing import List
from pydantic import BaseModel, Field
from openai import OpenAI
from config.settings import settings

class SubQuery(BaseModel):
    query: str = Field(description="A specific, highly targeted search query to investigate a sub-aspect of the topic.")
    rationale: str = Field(description="Brief explanation of why this sub-query is necessary for comprehensive research.")

class ResearchPlan(BaseModel):
    main_topic: str
    sub_queries: List[SubQuery] = Field(description="A list of targeted sub-queries covering different angles of the topic.")

class Planner:
    """
    Step 1: Deconstructs a high-level user research topic into modular, targeted sub-queries.
    """
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.MODEL_NAME

    def generate_plan(self, topic: str) -> ResearchPlan:
        """
        Generates a structured research plan with sub-questions using LLM-based function/structured output.
        """
        prompt = (
            f"You are an expert research strategist. Your goal is to deconstruct the following research topic "
            f"into exactly {settings.MAX_SUB_QUESTIONS} distinct, highly focused sub-queries that together provide "
            f"comprehensive coverage of the subject.\n\n"
            f"Research Topic: {topic}\n\n"
            f"Provide your response in valid JSON matching this schema:\n"
            f"{{\n"
            f"  \"main_topic\": \"{topic}\",\n"
            f"  \"sub_queries\": [\n"
            f"    {{\"query\": \"<search query 1>\", \"rationale\": \"<why this query is needed>\"}},\n"
            f"    ...\n"
            f"  ]\n"
            f"}}"
        )

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a precise research planning assistant that outputs strict JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=settings.TEMPERATURE,
            response_format={"type": "json_object"}
        )

        content = response.choices[0].message.content
        data = json.loads(content)
        return ResearchPlan(**data)