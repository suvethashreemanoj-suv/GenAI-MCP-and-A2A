import asyncio
from src.cv_agent.agent import CVAgent


async def main():
    print("=" * 60)
    print("CV Research Agent — 6 Specialized Tools")
    print("=" * 60)

    query = input("\nEnter your query: ").strip()
    if not query:
        print("No query entered. Exiting.")
        return

    agent = CVAgent()
    result = await agent.solve(query)

    print("\n" + "=" * 60)
    print(f"Agent: {result.agent_name}")
    print("=" * 60)
    print("\nRecommendations:")
    for r in result.recommendations:
        print(f"  - {r}")
    print("\nDatasets:")
    for d in result.datasets:
        print(f"  - {d}")
    print("\nModels:")
    for m in result.models:
        print(f"  - {m}")
    print(f"\nReasoning:\n{result.reasoning}")


if __name__ == "__main__":
    asyncio.run(main())
