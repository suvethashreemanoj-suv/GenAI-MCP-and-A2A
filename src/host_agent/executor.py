import json
import logging

from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events.event_queue import EventQueueLegacy
from a2a.server.tasks.task_updater import TaskUpdater
from a2a.types.a2a_pb2 import Part

from src.host_agent.agent import HostAgent

logger = logging.getLogger(__name__)


class HostAgentExecutor(AgentExecutor):
    def __init__(self):
        self._agent: HostAgent | None = None

    def initialize(self):
        self._agent = HostAgent()

    @property
    def agent(self) -> HostAgent:
        if self._agent is None:
            raise RuntimeError("HostAgentExecutor not initialized.")
        return self._agent

    async def execute(self, context: RequestContext, event_queue: EventQueueLegacy) -> None:
        query = context.get_user_input()
        task_id = context.task_id
        context_id = context.context_id

        updater = TaskUpdater(event_queue, task_id, context_id)

        try:
            await updater.start_work()
            result = await self.agent.orchestrate(query)

            agent_msg = updater.new_agent_message(parts=[Part(text=result)])
            await updater.complete(message=agent_msg)

        except Exception as e:
            logger.exception("Host Agent execution failed")
            error_msg = updater.new_agent_message(parts=[Part(text=f"Error: {str(e)}")])
            await updater.failed(message=error_msg)

    async def cancel(self, context: RequestContext, event_queue: EventQueueLegacy) -> None:
        updater = TaskUpdater(event_queue, context.task_id, context.context_id)
        await updater.cancel()
