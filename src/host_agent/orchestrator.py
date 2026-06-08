import os
import httpx
import asyncio
from openai import OpenAI
from dotenv import load_dotenv
from src.shared.schema import AgentRequest, AgentResponse

load_dotenv()

class HostAgent:
    def __init__(self):
        custom_http_client = httpx.Client()
        self.client = OpenAI(
            api_key=os.getenv("DEEPSEEK_API_KEY"),
            base_url=os.getenv("DEEPSEEK_BASE_URL", "https://apiv5.hareeshworks.in/v1")
        )
        self.model_id = os.getenv("MODEL_ID", "deepseek-chat")


        self.agent_urls = {
            "ml": "http://localhost:8003/process",
            # "cv": "http://localhost:8000/process",
            # "nlp": "http://localhost:8001/process"
        }

    async def call_specialized_agent(self, agent_key: str, query: str) -> dict:
        """Helper to send a request to a teammate's agent."""
        url = self.agent_urls.get(agent_key)
        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                print(f"Calling {agent_key.upper()} Agent...")
                response = await client.post(url, json={"query": query})
                return response.json()
            except Exception as e:
                return {"error": f"Could not reach {agent_key} agent: {str(e)}"}

    async def orchestrate(self, user_query: str):
        """The core logic: Decide, Delegate, and Aggregate."""

        decision_prompt = f"""
        Analyze the user's research request: "{user_query}"
        Which specialized agents are needed? 
        Answer only with a comma-separated list of: 'ml', 'cv', 'nlp'.
        Example: if it's about medical images, answer: 'ml, cv'.
        """

        decision_res = self.client.chat.completions.create(
            model=self.model_id,
            messages=[{"role": "user", "content": decision_prompt}]
        )
        required_agents = [a.strip() for a in decision_res.choices[0].message.content.lower().split(',')]

        print(f"Orchestrator decided to use: {required_agents}")

        tasks = [self.call_specialized_agent(agent, user_query) for agent in required_agents if agent in self.agent_urls]
        agent_results = await asyncio.gather(*tasks)

        final_prompt = f"""
        You are the Research Lead. Combine the following agent reports into one master research proposal.
        USER QUERY: {user_query}
        AGENT REPORTS: {agent_results}
        
        Structure your answer into:
        1. Executive Summary
        2. Technical Architecture (combining CV/NLP/ML)
        3. Implementation Plan
        """

        final_res = self.client.chat.completions.create(
            model=self.model_id,
            messages=[{"role": "user", "content": final_prompt}]
        )

        return final_res.choices[0].message.content

if __name__ == "__main__":
    host = HostAgent()

    # Example scenario: A Multimodal Medical Diagnosis Project
    # test_query =
    query = input("Enter your query:")

    async def run():
        result = await host.orchestrate(query)
        print("\n" + "="*50)
        print("FINAL RESEARCH PROPOSAL")
        print("="*50)
        print(result)

    asyncio.run(run())