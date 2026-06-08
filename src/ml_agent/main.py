import uvicorn
import os
import sys
from fastapi import FastAPI, HTTPException
from src.shared.schema import AgentCard


project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.shared.schema import AgentRequest, AgentResponse
from src.ml_agent.mcp_client import MLAgent

app = FastAPI(title="ML Agent Service")

ml_logic = None

@app.on_event("startup")
async def startup_event():
    global ml_logic
    print("Initializing ML Agent logic...")
    ml_logic = MLAgent()
    print("ML Agent is ready!")

@app.get("/")
async def root():
    return {"message": "ML Agent is Online"}

@app.get("/agentcard")
async def get_agent_card():
    return AgentCard(
        agent_name="ML_Research_Agent",
        primary_role="Specialized Researcher in Classical Machine Learning & Deep Learning Architectures",
        assigned_member="Member C (Machine Learning Specialist)",
        capabilities=[
            "Algorithm Recommendation",
            "Feature Engineering Advisory",
            "Experiment Design & Metric Planning",
            "Hyperparameter Optimization Logic"
        ],
        supported_tasks=["Literature Review", "Research Paper Discovery (ArXiv)", "Research Gap Analysis", "Citation Generator"],
        endpoint="/process"
)


@app.post("/process", response_model=AgentResponse)
async def process_request(request: AgentRequest):
    if ml_logic is None:
        raise HTTPException(status_code=503, detail="Agent not initialized")
    try:
        return await ml_logic.solve(request.query)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run("src.ml_agent.main:app", host="127.0.0.1", port=8003, reload=True)