import asyncio
from openai import OpenAI
from src.a2a.client import A2AClient
from src.a2a.utils import merge_responses
from src.shared.config import (
    CV_AGENT_PORT,
    ML_AGENT_URL,
    NLP_AGENT_URL,
    LLM_API_KEY,
    LLM_BASE_URL,
    MODEL_ID,
    OPENROUTER_SITE_URL,
    OPENROUTER_APP_NAME,
)


class HostAgent:
    def __init__(self):
        self._client = None
        self._model_id = None
        self.a2a = A2AClient(timeout=60.0)

        self.agent_urls = {
            "cv": f"http://127.0.0.1:{CV_AGENT_PORT}",
            "ml": ML_AGENT_URL,
            "nlp": NLP_AGENT_URL,
        }

        self.agent_endpoints = {
            "cv": "/process",
            "ml": "/process",
            "nlp": "/process",
        }

    @property
    def client(self):
        if self._client is None:
            headers = {}
            if "openrouter.ai" in LLM_BASE_URL:
                headers = {
                    "HTTP-Referer": OPENROUTER_SITE_URL,
                    "X-Title": OPENROUTER_APP_NAME,
                }
            self._client = OpenAI(
                api_key=LLM_API_KEY,
                base_url=LLM_BASE_URL,
                default_headers=headers or None,
            )
        return self._client

    @property
    def model_id(self):
        if self._model_id is None:
            self._model_id = MODEL_ID
        return self._model_id

    async def discover_agents(self):
        cards = await self.a2a.discover_all(list(self.agent_urls.values()))
        for card in cards:
            print(f"[Host] Discovered: {card.agent_name} ({card.assigned_member})")
        return cards

    async def call_specialized_agent(self, agent_key: str, query: str):
        url = self.agent_urls.get(agent_key)
        if not url:
            return None
        endpoint = self.agent_endpoints.get(agent_key, "/process")
        full_url = f"{url}{endpoint}"
        try:
            print(f"[Host] Delegating to {agent_key.upper()} agent at {full_url}...")
            return await self.a2a.send_task_raw(full_url, query)
        except Exception as e:
            print(f"[Host] Error calling {agent_key} agent: {e}")
            return None

    async def orchestrate(self, user_query: str) -> str:
        decision_prompt = f"""
        Analyze the user's research request: "{user_query}"
        Which specialized agents are needed?
        Answer only with a comma-separated list of: 'ml', 'cv', 'nlp'.
        Example: if it's about medical images, answer: 'ml, cv'.
        """

        decision_res = self.client.chat.completions.create(
            model=self.model_id,
            messages=[{"role": "user", "content": decision_prompt}],
        )
        required_agents = [
            a.strip()
            for a in decision_res.choices[0].message.content.lower().split(",")
            if a.strip() in self.agent_urls
        ]
        print(f"[Host] Orchestrator decided to use: {required_agents}")

        tasks = [
            self.call_specialized_agent(agent, user_query)
            for agent in required_agents
            if agent in self.agent_urls
        ]
        agent_results = await asyncio.gather(*tasks)
        valid_results = [r for r in agent_results if r is not None]

        if not valid_results:
            return "No agent responses were received. Please ensure at least one agent is running."

        merged = merge_responses(valid_results)

        final_prompt = f"""
        You are the Research Lead. Combine the following agent reports into one master research proposal.
        USER QUERY: {user_query}

        AGENT REPORTS:
        {merged['reasoning']}

        RECOMMENDATIONS: {merged['recommendations']}
        DATASETS: {merged['datasets']}
        MODELS: {merged['models']}

        Structure your answer into:
        1. Executive Summary
        2. Technical Architecture (combining all agent insights)
        3. Implementation Plan
        4. Recommended Datasets & Models
        """

        final_res = self.client.chat.completions.create(
            model=self.model_id,
            messages=[{"role": "user", "content": final_prompt}],
        )

        return final_res.choices[0].message.content
