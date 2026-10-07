import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from pydantic import ConfigDict

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    """
    Centralized configuration settings for the Autonomous Deep Research Agent.
    Loads API keys and hyperparameters from environment variables.
    """
    # API Keys
    TAVILY_API_KEY: str = os.getenv("TAVILY_API_KEY", "")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    # OPENROUTER_API_KEY: str = os.getenv("OPENROUTER_API_KEY", "")
    # GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")
    # GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    
    # LLM Configuration
    MODEL_NAME: str = os.getenv("MODEL_NAME", "gpt-4o-mini")
    TEMPERATURE: float = float(os.getenv("TEMPERATURE", "0.1"))
    
    # Research Agent Limits
    MAX_SUB_QUESTIONS: int = int(os.getenv("MAX_SUB_QUESTIONS", "5"))
    MAX_SEARCH_RESULTS_PER_QUERY: int = int(os.getenv("MAX_SEARCH_RESULTS_PER_QUERY", "5"))

    model_config = ConfigDict(
        env_file=".env",
        extra="ignore"
    )

# Instantiate global settings object
settings = Settings()