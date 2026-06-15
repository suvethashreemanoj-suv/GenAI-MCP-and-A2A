import asyncio
from src.host_agent.agent import HostAgent


async def main():
    print("=" * 60)
    print("Host Orchestrator — Multi-Agent Research Assistant")
    print("=" * 60)

    query = input("\nEnter your research query: ").strip()
    if not query:
        print("No query entered. Exiting.")
        return

    host = HostAgent()
    await host.discover_agents()
    result = await host.orchestrate(query)

    print("\n" + "=" * 60)
    print("RESEARCH PROPOSAL")
    print("=" * 60)
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
