from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any


class AgentCard(BaseModel):
    agent_name: str
    primary_role: str
    assigned_member: str
    capabilities: List[str]
    supported_tasks: List[str]
    endpoint: str = "/process"
    version: str = "1.0.0"
    protocol: str = "a2a"


class AgentRequest(BaseModel):
    query: str = Field(..., description="Target search query or concept guidelines.")
    context: Optional[str] = Field(None, description="Optional background system guidelines.")


class AgentResponse(BaseModel):
    agent_name: str
    recommendations: List[str] = Field(default_factory=list)
    datasets: List[str] = Field(default_factory=list)
    models: List[str] = Field(default_factory=list)
    reasoning: str = ""


class SendRequest(BaseModel):
    sender: str
    receiver: str
    task: str
    query: str
    context: Optional[Dict[str, Any]] = None


class SendResponse(BaseModel):
    sender: str
    receiver: str
    status: str = "success"
    result: AgentResponse
    error: Optional[str] = None


class DiscoveryResponse(BaseModel):
    agents: List[AgentCard]
    protocol_version: str = "1.0.0"
    ecosystem: str = "Multi-Agent Research Assistant"
