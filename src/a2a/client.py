import httpx
from typing import Optional, Dict, Any, List
from src.a2a.types import (
    AgentCard,
    AgentRequest,
    AgentResponse,
    SendRequest,
    SendResponse,
    DiscoveryResponse,
)


class A2AClient:
    def __init__(self, timeout: float = 30.0):
        self.timeout = timeout
        self._discovered_agents: Dict[str, AgentCard] = {}

    async def discover(self, base_url: str) -> AgentCard:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            resp = await client.get(f"{base_url}/agentcard")
            resp.raise_for_status()
            card = AgentCard(**resp.json())
            self._discovered_agents[card.agent_name] = card
            return card

    async def discover_all(self, endpoints: List[str]) -> List[AgentCard]:
        cards = []
        for ep in endpoints:
            try:
                card = await self.discover(ep)
                cards.append(card)
            except Exception as e:
                print(f"[A2A] Discovery failed for {ep}: {e}")
        return cards

    async def send_task(self, base_url: str, request: SendRequest) -> SendResponse:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            resp = await client.post(
                f"{base_url}/process",
                json=AgentRequest(query=request.query, context=str(request.context) if request.context else None).model_dump(),
            )
            resp.raise_for_status()
            result = AgentResponse(**resp.json())
            return SendResponse(
                sender=request.receiver,
                receiver=request.sender,
                result=result,
            )

    async def send_task_raw(self, url: str, query: str, context: str = None) -> AgentResponse:
        payload = {"query": query}
        if context:
            payload["context"] = context
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            resp = await client.post(url, json=payload)
            resp.raise_for_status()
            data = resp.json()
            return self._parse_agent_response(data)

    def get_agent(self, agent_name: str) -> Optional[AgentCard]:
        return self._discovered_agents.get(agent_name)

    def _parse_agent_response(self, data: dict) -> AgentResponse:
        return AgentResponse(
            agent_name=data.get("agent_name", data.get("name", "unknown")),
            recommendations=data.get("recommendations", []),
            datasets=data.get("datasets", []),
            models=data.get("models", []),
            reasoning=data.get("reasoning", data.get("analysis", data.get("result", ""))),
        )

    @property
    def known_agents(self) -> Dict[str, AgentCard]:
        return self._discovered_agents.copy()
