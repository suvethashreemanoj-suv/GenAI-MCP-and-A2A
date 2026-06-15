# CV Research Agent — Multi-Agent Ecosystem (Member A)

Computer Vision Research Agent aligned with the team [a2a-suve](https://github.com/suvethashreemanoj-suv/GenAI-MCP-and-A2A/tree/a2a-suve) architecture: **MCP tools**, **A2A protocol**, **dynamic LLM tool-calling**, and **Host orchestration**.

## Architecture

```
main.py (Gateway :8003)
├── /api/a2a/*       → A2A protocol endpoints
├── /api/a2a/mcp/*   → MCP tool discovery & execution
├── /api/host/*      → Host orchestrator
└── /process         → Backward-compatible CV agent endpoint

src/a2a/             → Shared A2A protocol layer
src/cv_agent/        → CV agent (6 tools, LLM-powered)
src/host_agent/      → Orchestrator (routes to cv/nlp/ml)
```

## CV Tools (MCP)

| Tool | Type | Description |
|------|------|-------------|
| `find_datasets` | Specialized | COCO, ImageNet, Open Images, medical datasets |
| `recommend_models` | Specialized | CNNs, ViTs, segmentation models |
| `search_benchmarks` | Specialized | SOTA leaderboard search |
| `search_cv_papers` | General | ArXiv cs.CV literature |
| `analyze_cv_research_gap` | General | Research gap analysis |
| `plan_cv_experiment` | General | Experiment plan with metrics |

## Getting Started

### 1. Install

```bash
pip install -r requirements.txt
```

### 2. Configure `.env`

```env
OPENROUTER_API_KEY=sk-or-v1-your_key
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
MODEL_ID=meta-llama/llama-4-scout
CV_AGENT_PORT=8003
```

### 3. Run Gateway

```bash
python main.py
```

Server: http://127.0.0.1:8003

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/a2a/discovery` | GET | Discover agents |
| `/api/a2a/agentcard` | GET | CV agent card |
| `/api/a2a/request` | POST | Send task to CV agent |
| `/api/a2a/mcp/list` | GET | List MCP tools |
| `/api/a2a/mcp/call` | POST | Call MCP tool directly |
| `/api/host/orchestrate` | POST | Multi-agent orchestration |
| `/process` | POST | Legacy A2A endpoint |
| `/agentcard` | GET | Legacy agent card |

### 4. Test

```bash
python test_client.py
```

### 5. Optional — CLI modes

```bash
python -m src.cv_agent          # CV agent CLI
python -m src.host_agent        # Host orchestrator CLI
python -m src.cv_agent.mcp_server  # Standalone MCP server
```

## Team Ports

| Agent | Port |
|-------|------|
| CV (this repo) | 8003 |
| ML (teammate) | 8002 |
| NLP (teammate) | 8005 |

## Tech Stack

- LLM: OpenRouter (`meta-llama/llama-4-scout`)
- A2A: `a2a-sdk[http-server]`
- MCP: `fastmcp`
- API: FastAPI + uvicorn
