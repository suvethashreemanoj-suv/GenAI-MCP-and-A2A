import json
import logging

from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events.event_queue import EventQueueLegacy
from a2a.server.tasks.task_updater import TaskUpdater
from a2a.types.a2a_pb2 import Part

from src.ml_agent.agent import MLAgent
from src.a2a.types import AgentCard, AgentResponse

logger = logging.getLogger(__name__)


class MLAgentExecutor(AgentExecutor):
    def __init__(self):
        self._agent: MLAgent | None = None

    def initialize(self):
        self._agent = MLAgent()

    @property
    def agent(self) -> MLAgent:
        if self._agent is None:
            raise RuntimeError("MLAgentExecutor not initialized. Call initialize() first.")
        return self._agent

    def get_card(self) -> AgentCard:
        return AgentCard(
            agent_name="ML_Research_Agent",
            primary_role="Specialized Researcher in Classical Machine Learning & Deep Learning Architectures",
            assigned_member="Member C (Machine Learning Specialist)",
            capabilities=[
                "Algorithm Recommendation",
                "Feature Engineering Advisory",
                "Experiment Design & Metric Planning",
                "Hyperparameter Optimization Logic",
            ],
            supported_tasks=[
                "Literature Review",
                "Research Paper Discovery (ArXiv)",
                "Research Gap Analysis",
                "Citation Generator",
            ],
            endpoint="/process",
        )

    def list_mcp_tools(self) -> list[dict]:
        from src.ml_agent.tools import TOOL_DEFINITIONS
        return TOOL_DEFINITIONS

    async def call_mcp_tool(self, tool_name: str, arguments: dict) -> str:
        from src.ml_agent.tools import TOOL_MAP

        if tool_name not in TOOL_MAP:
            raise ValueError(f"Tool '{tool_name}' not found")
        result = await TOOL_MAP[tool_name](**arguments)
        return str(result)

    async def execute(self, context: RequestContext, event_queue: EventQueueLegacy) -> None:
        query = context.get_user_input()
        task_id = context.task_id
        context_id = context.context_id

        updater = TaskUpdater(event_queue, task_id, context_id)

        try:
            await updater.start_work()

            result: AgentResponse = await self.agent.solve(query)

            response_text = json.dumps({
                "agent_name": result.agent_name,
                "recommendations": result.recommendations,
                "datasets": result.datasets,
                "models": result.models,
                "reasoning": result.reasoning,
            }, indent=2)

            agent_msg = updater.new_agent_message(
                parts=[Part(text=response_text)]
            )
            await updater.complete(message=agent_msg)

        except Exception as e:
            logger.exception("ML Agent execution failed")
            error_msg = updater.new_agent_message(
                parts=[Part(text=f"Error: {str(e)}")]
            )
            await updater.failed(message=error_msg)

    async def cancel(self, context: RequestContext, event_queue: EventQueueLegacy) -> None:
        updater = TaskUpdater(event_queue, context.task_id, context.context_id)
        await updater.cancel()
