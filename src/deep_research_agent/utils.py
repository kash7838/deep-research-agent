# This module provides helpful helper functions for the agent, such as automatically saving generated Markdown reports to a local reports/ directory with clean timestamped filenames.

import os
import re
from datetime import datetime
import logging

logger = logging.getLogger("DeepResearchAgent.Utils")

def sanitize_filename(name: str) -> str:
    """
    Sanitizes a string to make it safe for use as a file name.
    """
    # Remove invalid characters and replace spaces with underscores
    clean_name = re.sub(r'[^\w\s-]', '', name).strip().lower()
    clean_name = re.sub(r'[\s_-]+', '_', clean_name)
    return clean_name[:50]  # Limit length

def save_research_report(topic: str, report_content: str, output_dir: str = "reports") -> str:
    """
    Saves the final markdown research report to a file with a timestamped filename.
    Returns the path to the saved file.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        logger.info(f"Created output directory: {output_dir}")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_topic = sanitize_filename(topic)
    filename = f"research_{safe_topic}_{timestamp}.md"
    file_path = os.path.join(output_dir, filename)

    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(report_content)
        logger.info(f"Report successfully saved to {file_path}")
        return file_path
    except Exception as e:
        logger.error(f"Failed to save report to file: {e}")
        raise e