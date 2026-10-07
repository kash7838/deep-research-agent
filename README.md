# Autonomous "Deep Research" Agent 🚀

An autonomous, production-grade AI research agent built in Python that takes complex user topics, plans a multi-step search strategy, executes parallel web queries (via Tavily), reads and extracts content from multiple sources, synthesizes the findings, and outputs a structured markdown report with exact citations.

Designed as a portfolio project showcasing the core pillars of agentic engineering: **Planning, Tool Looping, Synthesis, and Evaluation**.

---

## 🏗️ Project Architecture & Core Pillars

1. **Autonomous Planning (`planner.py`):** Deconstructs a high-level user research topic into modular, targeted sub-questions and search intents.
2. **Parallel Search Execution (`search_executor.py`):** Leverages Tavily API to run concurrent web and database queries.
3. **Content Extraction & Processing (`extractor.py`):** Cleans, parses, and structures raw HTML/text data retrieved from multiple web sources.
4. **Synthesis & Citation (`synthesizer.py`):** Combines extracted findings into a comprehensive report with rigorous source mapping.
5. **Production Evaluation Harness (`evaluation/evaluate.py`):** Employs an LLM-as-a-judge framework to programmatically grade factual accuracy and citation correctness.

---

## 📁 Monolithic Project Structure

```text
deep-research-agent/
│
├── .env.example                 # Template for API keys (TAVILY_API_KEY, OPENAI/GROQ)
├── .gitignore                   # Excludes virtual environments, logs, and sensitive data
├── .python-version              # Python version pinned by uv
├── README.md                    # Project documentation
├── PROBLEM_STATEMENT.md         # Detailed problem & solution documentation
├── pyproject.toml               # uv dependency configuration & project metadata
├── uv.lock                      # Locked dependency versions
├── run.py                       # Main CLI entry point script
│
├── config/                      # System configurations and prompt templates
│   ├── __init__.py
│   └── settings.py              # Centralized app settings and model hyperparameters
│
├── src/deep_research_agent/     # Core application source code module
│   ├── __init__.py
│   ├── agent.py                 # Main agent orchestration graph/loop
│   ├── planner.py               # Step 1: Autonomous query decomposition
│   ├── search_executor.py       # Step 2: Parallel Tavily search handling
│   ├── extractor.py             # Step 3: Content reading and chunking
│   ├── synthesizer.py           # Step 4: Final synthesis & exact citation mapping
│   └── utils.py                 # Logging, text cleaning, and helper utilities
│
├── evaluation/                  # Production touch: Evaluation harness & LLM-as-a-judge
│   ├── __init__.py
│   ├── evaluate.py              # Automated grading script for accuracy and citations
│   └── test_cases.json          # Benchmark dataset of test queries and golden references
│
├── outputs/                     # Generated markdown reports and execution trace logs
│   ├── .gitkeep
│   └── sample_report.md
│
└── tests/                       # Unit tests for core agent components
    ├── __init__.py
    ├── test_planner.py
    └── test_search.py