import json
import re
from typing import Any, Optional

from openai import OpenAI

from src.a2a.types import AgentResponse
from src.cv_agent.tools import TOOL_MAP, TOOL_DEFINITIONS
from src.cv_agent.tools.specialized import find_datasets, recommend_models, search_benchmarks
from src.cv_agent.tools.general import (
    search_cv_papers,
    analyze_cv_research_gap,
    plan_cv_experiment,
)
from src.shared.config import (
    LLM_API_KEY,
    LLM_BASE_URL,
    MODEL_ID,
    OPENROUTER_SITE_URL,
    OPENROUTER_APP_NAME,
)


class CVAgent:
    def __init__(self):
        self._client = None
        self._model_id = None
        self.agent_name = "CV_Research_Agent"
        self.tools = TOOL_MAP
        self.tool_definitions = TOOL_DEFINITIONS

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

    def _infer_task_type(self, query: str) -> str:
        query_lower = query.lower()
        if any(k in query_lower for k in ("detect", "detection", "bbox", "yolo")):
            return "detection"
        if any(k in query_lower for k in ("segment", "mask", "semantic", "instance")):
            return "segmentation"
        if any(k in query_lower for k in ("x-ray", "xray", "medical", "mri", "ct", "pneumonia", "tumor")):
            return "medical"
        if any(k in query_lower for k in ("video", "action recognition", "temporal")):
            return "video"
        if any(k in query_lower for k in ("caption", "vqa", "vision-language", "vlm", "clip")):
            return "vision_language"
        return "classification"

    async def _safe_tool(self, label: str, coro) -> str:
        try:
            return await coro
        except Exception as e:
            print(f"[CVAgent] Tool '{label}' failed: {e}")
            return f"{label} unavailable: {e}"

    async def _gather_tool_context(self, query: str) -> dict[str, str]:
        task_type = self._infer_task_type(query)
        domain = "medical" if task_type == "medical" else "general"

        return {
            "datasets": await self._safe_tool(
                "find_datasets",
                find_datasets(task_type=task_type, domain=domain),
            ),
            "models": await self._safe_tool(
                "recommend_models",
                recommend_models(task_type=task_type, compute_budget="medium"),
            ),
            "benchmarks": await self._safe_tool(
                "search_benchmarks",
                search_benchmarks(task=task_type.replace("_", " "), max_results=5),
            ),
            "papers": await self._safe_tool("search_cv_papers", search_cv_papers(query)),
            "research_gap": await self._safe_tool(
                "analyze_cv_research_gap", analyze_cv_research_gap(query)
            ),
            "experiment_plan": await self._safe_tool(
                "plan_cv_experiment",
                plan_cv_experiment(query, task_type=task_type),
            ),
        }

    def _extract_message_content(self, message) -> str:
        content = message.content or ""
        if not content.strip():
            content = getattr(message, "reasoning_content", None) or ""
        return content.strip()

    def _clean_json_content(self, content: str) -> str:
        cleaned = content.strip()
        if cleaned.startswith("```"):
            cleaned = cleaned.split("\n", 1)[1] if "\n" in cleaned else cleaned[3:]
        if cleaned.endswith("```"):
            cleaned = cleaned.rsplit("\n", 1)[0] if "\n" in cleaned else cleaned[:-3]
        if cleaned.lower().startswith("json"):
            cleaned = cleaned[4:].lstrip()
        return cleaned.strip()

    def _is_meaningful_response(self, data: dict[str, Any]) -> bool:
        if not data:
            return False
        reasoning = (data.get("reasoning") or "").strip().lower()
        placeholder_phrases = {
            "",
            "no reasoning provided.",
            "no response generated.",
            "n/a",
            "none",
        }
        has_lists = any(data.get(k) for k in ("recommendations", "datasets", "models"))
        has_reasoning = reasoning not in placeholder_phrases and len(reasoning) > 20
        return has_lists or has_reasoning

    def _parse_json_response(self, content: str) -> dict[str, Any]:
        if not content:
            return {}

        candidates = [content, self._clean_json_content(content)]
        fence_match = re.search(r"```(?:json)?\s*([\s\S]*?)```", content, re.IGNORECASE)
        if fence_match:
            candidates.insert(0, fence_match.group(1).strip())

        for text in candidates:
            if not text:
                continue

            cleaned = self._clean_json_content(text)
            parse_attempts = [cleaned]

            start = cleaned.find("{")
            end = cleaned.rfind("}") + 1
            if start >= 0 and end > start:
                parse_attempts.append(cleaned[start:end])

            for attempt in parse_attempts:
                try:
                    data = json.loads(attempt.strip())
                    if isinstance(data, dict):
                        return data
                except json.JSONDecodeError:
                    continue

        return {
            "recommendations": [],
            "datasets": [],
            "models": [],
            "reasoning": content,
        }

    def _build_fallback_response(
        self, query: str, tool_context: dict[str, str], content: str = ""
    ) -> dict[str, Any]:
        model_hint = "a suitable CV model"
        if ":" in tool_context["models"]:
            model_hint = tool_context["models"].split(":")[-1].strip().split(",")[0]

        return {
            "recommendations": [
                f"Start with {model_hint} as a baseline",
                "Prepare train/validation/test splits with task-appropriate augmentations",
                "Evaluate using task-specific metrics and compare against SOTA benchmarks",
                "Run error analysis on failure cases before deployment",
            ],
            "datasets": self._extract_list_from_tool_output(tool_context["datasets"]),
            "models": self._extract_list_from_tool_output(tool_context["models"]),
            "reasoning": (
                f"Research analysis for: {query}\n\n"
                f"DATASETS:\n{tool_context['datasets']}\n\n"
                f"MODELS:\n{tool_context['models']}\n\n"
                f"BENCHMARKS:\n{tool_context['benchmarks']}\n\n"
                f"RESEARCH GAP:\n{tool_context['research_gap']}\n\n"
                f"EXPERIMENT PLAN:\n{tool_context['experiment_plan']}"
                + (f"\n\nLLM raw output:\n{content}" if content else "")
            ),
        }

    def _build_synthesis_prompt(self, tool_context: dict[str, str]) -> str:
        return f"""You are a Specialized Computer Vision Research Agent (Member A).

TOOL RESULTS (use these in your answer):
--- DATASETS ---
{tool_context['datasets']}

--- MODELS ---
{tool_context['models']}

--- BENCHMARKS ---
{tool_context['benchmarks']}

--- PAPERS ---
{tool_context['papers']}

--- RESEARCH GAP ---
{tool_context['research_gap']}

--- EXPERIMENT PLAN ---
{tool_context['experiment_plan']}

Analyze the user query using the tool results above.
You MUST return ONLY valid JSON (no markdown, no extra text) with this structure:
{{
  "recommendations": ["step-by-step implementation steps"],
  "datasets": ["dataset names from the tool results"],
  "models": ["model names from the tool results"],
  "reasoning": "A detailed technical report covering literature review, research gaps, datasets, models, and evaluation strategy"
}}"""

    async def _try_native_tool_calling(self, query: str) -> Optional[str]:
        messages = [
            {
                "role": "system",
                "content": (
                    "You are a Specialized Computer Vision Research Agent. "
                    "Use the provided tools to gather information, then respond."
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
        if not assistant_message.tool_calls:
            text = self._extract_message_content(assistant_message)
            return text if text else None

        messages.append(assistant_message)
        for tool_call in assistant_message.tool_calls:
            func_name = tool_call.function.name
            func_args = json.loads(tool_call.function.arguments or "{}")
            result = await self.tools[func_name](**func_args) if func_name in self.tools else f"Unknown tool: {func_name}"
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": str(result),
            })

        messages.append({
            "role": "user",
            "content": (
                "Using the tool results above, return ONLY valid JSON with keys: "
                "recommendations (list), datasets (list), models (list), reasoning (string)."
            ),
        })

        final_response = self.client.chat.completions.create(
            model=self.model_id,
            messages=messages,
        )
        return self._extract_message_content(final_response.choices[0].message)

    async def _synthesize_from_tools(self, query: str, tool_context: dict[str, str]) -> str:
        response = self.client.chat.completions.create(
            model=self.model_id,
            messages=[
                {"role": "system", "content": self._build_synthesis_prompt(tool_context)},
                {"role": "user", "content": query},
            ],
        )
        return self._extract_message_content(response.choices[0].message)

    async def solve(self, query: str) -> AgentResponse:
        tool_context = await self._gather_tool_context(query)
        content = await self._synthesize_from_tools(query, tool_context)

        if not content:
            try:
                content = await self._try_native_tool_calling(query)
            except Exception as e:
                print(f"[CVAgent] Native tool calling unavailable: {e}")

        data = self._parse_json_response(content or "")

        if not self._is_meaningful_response(data):
            data = self._build_fallback_response(query, tool_context, content or "")

        return AgentResponse(
            agent_name=self.agent_name,
            recommendations=data.get("recommendations") or [],
            datasets=data.get("datasets") or [],
            models=data.get("models") or [],
            reasoning=data.get("reasoning") or "Analysis completed using CV research tools.",
        )

    def _extract_list_from_tool_output(self, text: str, key: str = "name") -> list[str]:
        items = []
        for line in text.splitlines():
            line = line.strip()
            if line.startswith("- ") and not line.startswith("- Model:"):
                items.append(line[2:].split("\n")[0].strip())
            elif line.startswith("- Model:"):
                items.append(line.replace("- Model:", "").strip())
        return items[:8] if items else ["See reasoning for details"]
