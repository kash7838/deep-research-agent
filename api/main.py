import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

# Adjust this import to match your actual agent package structure
from src.deep_research_agent.agent import DeepResearchAgent

app = FastAPI(title="Deep Research Agent API", version="1.0")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ResearchRequest(BaseModel):
    topic: str = Field(..., description="The research topic or question to investigate.")

class ResearchResponse(BaseModel):
    topic: str
    report: str
    storage_mode: str = Field(default="ChromaDB RAG", description="Persistent vector memory storage")

@app.post("/api/research", response_model=ResearchResponse)
def run_research(request: ResearchRequest):
    try:
        logger.info(f"Received research topic: '{request.topic}'")
        
        # Initialize agent (token budget and RAG checks are handled internally)
        agent = DeepResearchAgent()
        report = agent.run_research(request.topic)

        return ResearchResponse(
            topic=request.topic,
            report=report,
            storage_mode="Successfully indexed in local ChromaDB vector memory"
        )
        
    except Exception as e:
        logger.error(f"Error executing research: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))