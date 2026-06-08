**Multi-Agent Research Assistant Ecosystem (ML Agent)**

**Overview**
This project is a collaborative multi-agent research ecosystem built using Agentic AI principles. It leverages Model Context Protocol (MCP) for tool use and Agent-to-Agent (A2A) communication to enable three specialized researchers (Computer Vision, NLP, and Machine Learning) to collaborate on complex research proposals.
I am responsible for the Machine Learning Research Agent, which provides expertise in classical ML, feature engineering, and experiment design.

**System Architecture**
The ecosystem follows a "Host-Worker" architecture:
-Host Agent (Orchestrator): The brain that decomposes user queries and delegates tasks to specialized agents over the network.
-ML Research Agent (Specialized Agent): A DeepSeek-powered expert that uses local MCP tools to provide technical ML strategies.
-MCP Server: A collection of specialized tools that allow the agent to search ArXiv and provide algorithm recommendations.
-A2A Layer: A FastAPI-based communication bridge that allows teammates to access the ML Agent via HTTP.

**Specialized ML Tools** 
My agent is equipped with a "Specialized Toolbox" built on the Model Context Protocol:
Tool Name	                 Description
-search_ml_papers	         Scrapes ArXiv API for the latest peer-reviewed ML literature.
-recommend_algorithms	     Heuristic engine that suggests specific models (XGBoost, SVM, etc.) based on data size.
-plan_experiment	             Generates structured validation strategies (e.g., Stratified K-Fold).
-suggest_hyperparameters	     Provides expert-level tuning ranges for the chosen models.
-advise_feature_engineering	 Recommends data transformations like RobustScaling or One-Hot Encoding.

**Tech Stack**
LLM: DeepSeek 
Web Framework: FastAPI (for A2A)
Protocol: Model Context Protocol (MCP) via fastmcp
Async Logic: httpx and asyncio
Schema: Pydantic (for shared request and response schema)

**Project Structure**
src/
├── host_agent/
│   └── orchestrator.py    # The Orchestrator (CEO Agent)
├── ml_agent/
│   ├── main.py            # FastAPI A2A Service (Port 8002)
│   ├── mcp_client.py      # DeepSeek Agent Logic
│   └── mcp_server.py      # MCP Tool definitions
└── shared/
    └── schema.py          # Team-shared Pydantic models

 **Getting Started**
1. Prerequisites
Ensure you have Python 3.11+ and an active virtual environment.

`pip install -r requirement.txt`

2. Configuration
.env file :
DEEPSEEK_API_KEY=your_key
DEEPSEEK_BASE_URL=model_url
MODEL_ID=your_model_id

3. Run the ML Agent (A2A Service)
This allows your teammates to connect to your agent.

`python -m src.ml_agent.main`
Access the interactive docs at: http://localhost:8002/docs

4. Run the Host Agent (Orchestrator)
This is your personal entry point to talk to the whole team.

`python -m src.host_agent.orchestrator`


**A2A Communication Design**
To ensure the team can collaborate, every agent follows a Shared Schema.
-Request Format: {"query": "string", "context": "optional string"}

-Response Format:
{
  "agent_name": "ML_Research_Agent",
  "recommendations": [],
  "datasets": [],
  "models": [],
  "reasoning": "Detailed technical analysis..."
}

**Demonstration Scenarios**
Scenario 1 (ML Specific): "Design a credit card fraud detection system."
Result: Agent recommends XGBoost, SMOTE for imbalance, and AUPRC metrics.
Scenario 2 (Multi-Agent): "Design a system for pneumonia detection from X-rays and patient notes."
Result: The Host Agent calls the CV Agent for image analysis, the NLP Agent for clinical notes, and the ML Agent for the final diagnostic logic.
