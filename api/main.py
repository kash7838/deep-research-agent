from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
import logging
import os

from src.deep_research_agent.agent import DeepResearchAgent

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("DeepResearchAPI")

app = FastAPI(
    title="Autonomous Deep Research Agent API",
    version="1.0.0",
    description="Backend API for triggering autonomous deep research, web crawling, and synthesis."
)

# Enable CORS for frontend integration (e.g., Streamlit, React, Next.js)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for production domains as needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ResearchRequest(BaseModel):
    topic: str = Field(..., description="The research topic or question to investigate.", examples=["Latest advancements in agentic AI frameworks in 2026"])

class ResearchResponse(BaseModel):
    topic: str
    report: str
    file_path: str

# Mount static folder
app.mount("/static", StaticFiles(directory="api/static"), name="static")

@app.get("/")
async def serve_frontend():
    return FileResponse("api/static/index.html")

@app.get("/")  # Or FastAPI standard @app.get("/")
@app.get("/")
def health_check():
    return {"status": "healthy", "service": "Deep Research Agent API"}

@app.post("/api/research", response_model=ResearchResponse)
def run_research(request: ResearchRequest):
    """
    Triggers the end-to-end autonomous deep research pipeline for a given topic.
    """
    try:
        # --- Add token budget safeguard here ---
        def estimate_tokens(text: str) -> int:
            return len(text) // 4

        if estimate_tokens(request.topic) > 100:
            request.topic = request.topic[:400]
        # ----------------------------------------

        logger.info(f"Received API request for research topic: '{request.topic}'")
        agent = DeepResearchAgent()
        
        # Run the full research pipeline
        report = agent.run_research(request.topic)
        
        # Find the latest saved report in the outputs directory
        output_dir = "outputs"
        files = [os.path.join(output_dir, f) for f in os.listdir(output_dir) if f.endswith(".md")]
        latest_file = max(files, key=os.path.getmtime) if files else "outputs/report.md"

        return ResearchResponse(
            topic=request.topic,
            report=report,
            file_path=latest_file
        )
    except Exception as e:
        logger.error(f"Error executing research via API: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))