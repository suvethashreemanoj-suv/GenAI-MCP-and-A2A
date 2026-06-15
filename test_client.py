import httpx
import asyncio
import sys

BASE_URL = "http://http://172.16.32.51:3000/"


async def request(method: str, path: str, json: dict = None, timeout: float = 10.0):
    async with httpx.AsyncClient(timeout=timeout) as client:
        try:
            resp = await client.request(method, f"{BASE_URL}{path}", json=json)
            return resp.status_code, resp.json()
        except httpx.ConnectError:
            return 0, {"error": f"Cannot connect to {BASE_URL}. Is the server running?"}
        except Exception as e:
            return 0, {"error": str(e)}


async def test_health():
    status, data = await request("GET", "/")
    if status == 200:
        print(f"[Health] OK — {data.get('message', data)}")
    else:
        print(f"[Health] FAIL (HTTP {status}) — {data}")
    return status == 200


async def test_agentcard():
    status, data = await request("GET", "/api/a2a/agentcard")
    if status == 200 and "agent_name" in data:
        print(f"[AgentCard] {data['agent_name']} — {data['primary_role']}")
    else:
        print(f"[AgentCard] FAIL (HTTP {status}) — {data}")


async def test_discovery():
    status, data = await request("GET", "/api/a2a/discovery")
    if status == 200 and "agents" in data:
        print(f"[Discovery] Found {len(data['agents'])} agent(s)")
        for agent in data["agents"]:
            print(f"  - {agent['agent_name']} ({agent['assigned_member']})")
    else:
        print(f"[Discovery] FAIL (HTTP {status}) — {data}")


async def test_mcp_list():
    status, data = await request("GET", "/api/a2a/mcp/list")
    if status == 200 and "tools" in data:
        tools = data["tools"]
        print(f"[MCP] {len(tools)} tool(s) available:")
        for t in tools:
            desc = t.get("description", "")[:60]
            print(f"  - {t['name']}: {desc}...")
    else:
        print(f"[MCP List] FAIL (HTTP {status}) — {data}")


async def test_mcp_call():
    status, data = await request(
        "POST",
        "/api/a2a/mcp/call",
        json={"tool": "recommend_algorithms", "arguments": {"task_type": "classification", "data_size": "large"}},
    )
    if status == 200 and "result" in data:
        print(f"[MCP Call] recommend_algorithms -> {data['result']}")
    else:
        print(f"[MCP Call] FAIL (HTTP {status}) — {data}")


async def test_agent_request():
    print("[Agent Request] Sending query (may take 10-30s)...")
    status, data = await request(
        "POST",
        "/api/a2a/request",
        json={"query": "transformer architectures for time series forecasting"},
        timeout=60.0,
    )
    if status == 200 and "agent_name" in data:
        print(f"[Agent Request] Response from {data['agent_name']}:")
        print(f"  Recommendations: {data.get('recommendations', [])[:2]}...")
        print(f"  Datasets: {data.get('datasets', [])[:2]}...")
        print(f"  Models: {data.get('models', [])[:2]}...")
        reasoning = data.get("reasoning", "")
        print(f"  Reasoning: {reasoning[:150]}...")
    else:
        print(f"[Agent Request] FAIL (HTTP {status}) — {data}")


async def main():
    print("=" * 50)
    print("Multi-Agent Research Assistant — Test Client")
    print(f"Target: {BASE_URL}")
    print("=" * 50)

    ok = await test_health()
    if not ok:
        print("\nServer is not running. Start it with: python main.py")
        sys.exit(1)

    await test_agentcard()
    await test_discovery()
    await test_mcp_list()
    await test_mcp_call()
    await test_agent_request()

    print("\n" + "=" * 50)
    print("All tests completed.")
    print("=" * 50)


if __name__ == "__main__":
    asyncio.run(main())
