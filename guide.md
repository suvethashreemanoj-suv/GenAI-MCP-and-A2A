# Multi-Agent Research Assistant — Local Setup Guide

## Prerequisites

- Python 3.11+
- pip

## 1. Clone & Create Virtual Environment

```bash
git clone <your-repo-url>
cd MCP_Ecosystem
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS/Linux
```

## 2. Install Dependencies

```bash
pip install -r requirements.txt
```

## 3. Configure Environment

Copy the example env file and fill in your API key:

```bash
cp .env
```

Edit `.env`:

```
DEEPSEEK_API_KEY="sk-your-key-here"
DEEPSEEK_BASE_URL="https://apiv5.hareeshworks.in/v1"
MODEL_ID="cmd/deepseek/deepseek-v4-flash"
```

## 4. Run the Gateway (Recommended)

Start the unified FastAPI gateway that serves all endpoints:

```bash
python main.py
```

This starts the server at `http://127.0.0.1:8000` with:

| Endpoint | Method | Description |
|---|---|---|
| `/api/a2a/discovery` | GET | Discover all registered agents |
| `/api/a2a/agentcard` | GET | Get ML agent card |
| `/api/a2a/request` | POST | Send a task to the ML agent |
| `/api/a2a/mcp/list` | GET | List all MCP tools |
| `/api/a2a/mcp/call` | POST | Call an MCP tool directly |
| `/api/host/orchestrate` | POST | Host orchestrator (multi-agent) |
| `/process` | POST | Backward-compatible ML agent endpoint |
| `/agentcard` | GET | Backward-compatible agent card |

## 5. Run the Standalone ML Agent (Optional)

To run the ML agent as a separate service on port 8003:

```bash
python -m src.ml_agent.main
```

## 6. Run the MCP Server Standalone (Optional)

```bash
python -m src.ml_agent.mcp_server
```

## 7. Test the System

```bash
python test_client.py
```

## 8. Teammate Collaboration

To connect with CV (port 8004) and NLP (port 8005) agents from teammates:

1. Start their services on the expected ports
2. Update `agent_urls` in `src/host_agent/agent.py` if needed
3. Use `POST /api/host/orchestrate` — the orchestrator will auto-discover and delegate

## Architecture

```
main.py (Gateway :8000)
├── /api/a2a/*       → A2A protocol endpoints
├── /api/a2a/mcp/*   → MCP tool discovery & execution
├── /api/host/*      → Host orchestrator
└── /process         → Direct ML agent access

src/a2a/             → Shared A2A protocol layer
src/ml_expert_crew/  → ML agent (8 tools, LLM-powered)
src/host_agent_adk/  → Orchestrator (routes to agents)
src/ml_agent/        → Standalone ML service (port 8003)
```
