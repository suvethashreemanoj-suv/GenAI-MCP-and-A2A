from pydantic import BaseModel
from typing import List, Optional

class AgentRequest(BaseModel):
    query: str
    context: Optional[str] = None

class AgentResponse(BaseModel):
    agent_name: str
    recommendations: List[str]
    datasets: List[str]
    models: List[str]
    reasoning: str

class AgentCard(BaseModel):
    agent_name: str
    primary_role: str
    assigned_member: str
    capabilities: List[str]
    supported_tasks: List[str]
    endpoint: str = "/process"