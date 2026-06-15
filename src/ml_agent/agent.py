import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from src.a2a.types import AgentResponse
from src.ml_agent.tools import TOOL_MAP, TOOL_DEFINITIONS

load_dotenv()


class MLAgent:
    def __init__(self):
        self._client = None
        self._model_id = None
        self.agent_name = "ML_Research_Agent"
        self.tools = TOOL_MAP
        self.tool_definitions = TOOL_DEFINITIONS

    @property
    def client(self):
        if self._client is None:
            self._client = OpenAI(
                api_key=os.getenv("DEEPSEEK_API_KEY"),
                base_url=os.getenv("DEEPSEEK_BASE_URL", "https://apiv5.hareeshworks.in/v1"),
            )
        return self._client

    @property
    def model_id(self):
        if self._model_id is None:
            self._model_id = os.getenv("MODEL_ID", "deepseek-chat")
        return self._model_id

    async def solve(self, query: str) -> AgentResponse:
        messages = [
            {
                "role": "system",
                "content": (
                    "You are a specialized Machine Learning Research Agent. "
                    "You have access to 9 tools: 4 specialized ML tools "
                    "(recommend_algorithms, suggest_hyperparameters, advise_feature_engineering, plan_experiment) "
                    "and 5 general research tools (search_ml_papers, summarize_paper, analyze_research_gap, "
                    "generate_citation, list_datasets). "
                    "Use tools dynamically based on the query. Not all tools need to be called every time. "
                    "Pick the most relevant tools for the user's request."
                ),
            },
            {"role": "user", "content": query},
        ]

        response = self.client.chat.completions.create(
            model=self.model_id,
            messages=messages,
            tools=self.tool_definitions,
            tool_choice="auto",
        )

        assistant_message = response.choices[0].message

        if assistant_message.tool_calls:
            messages.append(assistant_message)

            for tool_call in assistant_message.tool_calls:
                func_name = tool_call.function.name
                func_args = json.loads(tool_call.function.arguments)

                if func_name in self.tools:
                    result = await self.tools[func_name](**func_args)
                else:
                    result = f"Unknown tool: {func_name}"

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": str(result),
                })

            final_response = self.client.chat.completions.create(
                model=self.model_id,
                messages=messages,
                response_format={"type": "json_object"},
            )
            content = final_response.choices[0].message.content
        else:
            content = assistant_message.content

        try:
            data = json.loads(content)
        except Exception:
            data = {
                "recommendations": [],
                "datasets": [],
                "models": [],
                "reasoning": content or "No response generated.",
            }

        return AgentResponse(
            agent_name=self.agent_name,
            recommendations=data.get("recommendations", []),
            datasets=data.get("datasets", []),
            models=data.get("models", []),
            reasoning=data.get("reasoning", "No reasoning provided."),
        )
