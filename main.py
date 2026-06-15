import uvicorn
from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager

from a2a.server.request_handlers.default_request_handler import LegacyRequestHandler
from a2a.server.tasks.inmemory_task_store import InMemoryTaskStore
from a2a.server.routes import (
    create_agent_card_routes,
    create_jsonrpc_routes,
    add_a2a_routes_to_fastapi,
)
from a2a.types.a2a_pb2 import (
    AgentCard as A2AAgentCard,
    AgentCapabilities,
    AgentInterface,
    AgentSkill,
)

from src.a2a.types import AgentRequest, AgentResponse, AgentCard, DiscoveryResponse
from src.cv_agent.agent_executor import CVAgentExecutor
from src.host_agent.agent import HostAgent
from src.shared.config import CV_AGENT_HOST, CV_AGENT_PORT, get_public_base_url

cv_executor = CVAgentExecutor()
host_agent = HostAgent()


def build_agent_card() -> A2AAgentCard:
    return A2AAgentCard(
        name="CV_Research_Agent",
        description="Specialized Computer Vision Research Agent with 6 tools",
        version="1.0.0",
        capabilities=AgentCapabilities(streaming=True),
        skills=[
            AgentSkill(
                id="cv_research",
                name="Computer Vision Research",
                description="Dataset finder, model recommender, benchmark search, medical imaging",
            ),
        ],
        supported_interfaces=[
            AgentInterface(
                protocol_binding="JSONRPC",
                url=get_public_base_url(),
            ),
        ],
        default_input_modes=["text/plain"],
        default_output_modes=["text/plain"],
    )


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("[Gateway] Initializing CV Agent Executor...")
    try:
        cv_executor.initialize()
        print("[Gateway] CV Agent ready.")
    except Exception as e:
        print(f"[Gateway] ERROR during initialization: {e}")
    yield
    print("[Gateway] Shutting down.")


app = FastAPI(
    title="CV Research Agent Gateway",
    description="A2A endpoints, MCP tools, and Host Orchestration for Computer Vision",
    version="2.0.0",
    lifespan=lifespan,
)

a2a_agent_card = build_agent_card()
task_store = InMemoryTaskStore()
request_handler = LegacyRequestHandler(
    agent_executor=cv_executor,
    task_store=task_store,
    agent_card=a2a_agent_card,
)

agent_card_routes = create_agent_card_routes(a2a_agent_card)
jsonrpc_routes = create_jsonrpc_routes(request_handler, rpc_url="/a2a")

add_a2a_routes_to_fastapi(
    app,
    agent_card_routes=agent_card_routes,
    jsonrpc_routes=jsonrpc_routes,
)


@app.get("/")
async def root():
    return {"message": "CV Research Agent Gateway is Online", "version": "2.0.0"}


@app.get("/api/a2a/discovery", response_model=DiscoveryResponse)
async def a2a_discovery():
    return DiscoveryResponse(agents=[cv_executor.get_card()])


@app.get("/api/a2a/agentcard", response_model=AgentCard)
async def a2a_agentcard():
    return cv_executor.get_card()


@app.get("/agentcard", response_model=AgentCard)
async def legacy_agentcard():
    return cv_executor.get_card()


@app.post("/api/a2a/request", response_model=AgentResponse)
async def a2a_request(request: AgentRequest):
    try:
        return await cv_executor.agent.solve(request.query)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/process", response_model=AgentResponse)
async def legacy_process(request: AgentRequest):
    try:
        return await cv_executor.agent.solve(request.query)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/a2a/mcp/list")
async def mcp_list_tools():
    from src.cv_agent.tools import TOOL_DEFINITIONS
    tools = [
        {
            "name": t["function"]["name"],
            "description": t["function"].get("description", ""),
        }
        for t in TOOL_DEFINITIONS
    ]
    return {"tools": tools}


@app.post("/api/a2a/mcp/call")
async def mcp_call_tool(body: dict):
    from src.cv_agent.tools import TOOL_MAP

    tool_name = body.get("tool_name") or body.get("tool")
    arguments = body.get("arguments", {})
    if not tool_name:
        raise HTTPException(status_code=400, detail="Missing 'tool' or 'tool_name' field")
    if tool_name not in TOOL_MAP:
        raise HTTPException(status_code=404, detail=f"Tool '{tool_name}' not found")
    try:
        result = await TOOL_MAP[tool_name](**arguments)
        return {"status": "success", "tool": tool_name, "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/host/orchestrate")
async def host_orchestrate(request: AgentRequest):
    try:
        proposal = await host_agent.orchestrate(request.query)
        return {"query": request.query, "proposal": proposal}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run("main:app", host=CV_AGENT_HOST, port=CV_AGENT_PORT, reload=True)
