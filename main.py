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
from src.ml_agent.agent_executor import MLAgentExecutor
from src.host_agent.agent import HostAgent
from src.shared.config import ML_AGENT_HOST, ML_AGENT_PORT

ml_executor = MLAgentExecutor()
host_agent = HostAgent()


def build_agent_card() -> A2AAgentCard:
    return A2AAgentCard(
        name="ML_Research_Agent",
        description="Specialized ML Research Agent with 9 tools",
        version="1.0.0",
        capabilities=AgentCapabilities(streaming=True),
        skills=[
            AgentSkill(
                id="ml_research",
                name="ML Research",
                description="Algorithm recommendation, hyperparameter tuning, experiment planning",
            ),
        ],
        supported_interfaces=[
            AgentInterface(
                protocol_binding="JSONRPC",
                url=f"http://{ML_AGENT_HOST}:{ML_AGENT_PORT}",
            ),
        ],
        default_input_modes=["text/plain"],
        default_output_modes=["text/plain"],
    )


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("[Gateway] Initializing ML Agent Executor...")
    try:
        ml_executor.initialize()
        print("[Gateway] ML Agent ready.")
    except Exception as e:
        print(f"[Gateway] ERROR during initialization: {e}")
    yield
    print("[Gateway] Shutting down.")


app = FastAPI(
    title="Multi-Agent Research Assistant Gateway",
    description="Root gateway serving A2A endpoints, MCP tools, and Host Orchestration",
    version="2.0.0",
    lifespan=lifespan,
)


a2a_agent_card = build_agent_card()
task_store = InMemoryTaskStore()
request_handler = LegacyRequestHandler(
    agent_executor=ml_executor,
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
    return {"message": "Multi-Agent Research Assistant Gateway is Online", "version": "2.0.0"}


@app.get("/api/a2a/discovery", response_model=DiscoveryResponse)
async def a2a_discovery():
    card = ml_executor.get_card()
    return DiscoveryResponse(agents=[card])


@app.get("/api/a2a/agentcard", response_model=AgentCard)
async def a2a_agentcard():
    return ml_executor.get_card()


@app.post("/api/a2a/request", response_model=AgentResponse)
async def a2a_request(request: AgentRequest):
    try:
        return await ml_executor.agent.solve(request.query)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/a2a/mcp/list")
async def mcp_list_tools():
    from src.ml_agent.tools import TOOL_DEFINITIONS
    return {"tools": TOOL_DEFINITIONS}


@app.post("/api/a2a/mcp/call")
async def mcp_call_tool(body: dict):
    from src.ml_agent.tools import TOOL_MAP

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
    uvicorn.run("main:app", host=ML_AGENT_HOST, port=ML_AGENT_PORT, reload=True)
