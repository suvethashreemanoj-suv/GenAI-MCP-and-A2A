from mcp.server.fastmcp import FastMCP
from src.ml_agent.tools.specialized import (
    recommend_algorithms,
    suggest_hyperparameters,
    advise_feature_engineering,
    plan_experiment,
)
from src.ml_agent.tools.general import (
    search_ml_papers,
    summarize_paper,
    analyze_research_gap,
    generate_citation,
    list_datasets,
)

mcp = FastMCP("ML_Research_Specialist")

mcp.tool()(recommend_algorithms)
mcp.tool()(suggest_hyperparameters)
mcp.tool()(advise_feature_engineering)
mcp.tool()(plan_experiment)
mcp.tool()(search_ml_papers)
mcp.tool()(summarize_paper)
mcp.tool()(analyze_research_gap)
mcp.tool()(generate_citation)
mcp.tool()(list_datasets)


if __name__ == "__main__":
    mcp.run()
