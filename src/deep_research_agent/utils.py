# This module provides helpful helper functions for the agent, such as text sanitization and token estimation.

import re
import logging

logger = logging.getLogger("DeepResearchAgent.Utils")

def sanitize_text(text: str) -> str:
    """
    Cleans and sanitizes text strings for efficient storage and retrieval.
    """
    if not text:
        return ""
    # Normalize whitespace and strip trailing noise
    clean_text = re.sub(r'\s+', ' ', text).strip()
    return clean_text

def estimate_tokens(text: str) -> int:
    """
    Provides a rough token count estimation (approx 4 characters per token) 
    to enforce strict budget constraints.
    """
    if not text:
        return 0
    return len(text) // 4