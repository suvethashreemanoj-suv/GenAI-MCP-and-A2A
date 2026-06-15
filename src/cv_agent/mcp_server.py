from mcp.server.fastmcp import FastMCP
from src.cv_agent.tools.specialized import find_datasets, recommend_models, search_benchmarks
from src.cv_agent.tools.general import (
    search_cv_papers,
    analyze_cv_research_gap,
    plan_cv_experiment,
)

mcp = FastMCP("CV_Research_Specialist")

mcp.tool()(find_datasets)
mcp.tool()(recommend_models)
mcp.tool()(search_benchmarks)
mcp.tool()(search_cv_papers)
mcp.tool()(analyze_cv_research_gap)
mcp.tool()(plan_cv_experiment)


if __name__ == "__main__":
    mcp.run()
