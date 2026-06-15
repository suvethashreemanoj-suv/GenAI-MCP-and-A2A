from src.a2a.types import AgentCard, AgentResponse


def format_agent_card(card: AgentCard) -> str:
    caps = "\n".join(f"  - {c}" for c in card.capabilities)
    tasks = "\n".join(f"  - {t}" for t in card.supported_tasks)
    return (
        f"Agent: {card.agent_name}\n"
        f"Role: {card.primary_role}\n"
        f"Member: {card.assigned_member}\n"
        f"Capabilities:\n{caps}\n"
        f"Supported Tasks:\n{tasks}\n"
        f"Endpoint: {card.endpoint}"
    )


def validate_response(resp: AgentResponse) -> bool:
    return bool(resp.agent_name and resp.reasoning)


def merge_responses(responses: list[AgentResponse]) -> dict:
    merged = {
        "recommendations": [],
        "datasets": [],
        "models": [],
        "reasoning_parts": [],
    }
    for r in responses:
        merged["recommendations"].extend(r.recommendations)
        merged["datasets"].extend(r.datasets)
        merged["models"].extend(r.models)
        merged["reasoning_parts"].append(f"[{r.agent_name}]: {r.reasoning}")

    merged["recommendations"] = list(dict.fromkeys(merged["recommendations"]))
    merged["datasets"] = list(dict.fromkeys(merged["datasets"]))
    merged["models"] = list(dict.fromkeys(merged["models"]))
    merged["reasoning"] = "\n\n".join(merged["reasoning_parts"])
    del merged["reasoning_parts"]

    return merged
