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

SPECIALIZED_TOOLS = [
    recommend_algorithms,
    suggest_hyperparameters,
    advise_feature_engineering,
    plan_experiment,
]

GENERAL_TOOLS = [
    search_ml_papers,
    summarize_paper,
    analyze_research_gap,
    generate_citation,
    list_datasets,
]

ALL_TOOLS = SPECIALIZED_TOOLS + GENERAL_TOOLS

TOOL_MAP = {fn.__name__: fn for fn in ALL_TOOLS}

TOOL_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "recommend_algorithms",
            "description": "Suggest ML algorithms for a given task type and data size",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_type": {"type": "string", "description": "classification, regression, or time_series"},
                    "data_size": {"type": "string", "description": "small, medium, or large"},
                    "interpretability_required": {"type": "boolean", "description": "Whether model must be interpretable"},
                },
                "required": ["task_type", "data_size"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "suggest_hyperparameters",
            "description": "Provide tuning ranges for a given model",
            "parameters": {
                "type": "object",
                "properties": {
                    "model_name": {"type": "string", "description": "xgboost, random_forest, svm, etc."},
                },
                "required": ["model_name"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "advise_feature_engineering",
            "description": "Recommend data transformations for given column types",
            "parameters": {
                "type": "object",
                "properties": {
                    "column_types": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of column types: numerical, categorical, datetime",
                    },
                },
                "required": ["column_types"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "plan_experiment",
            "description": "Generate a structured experiment plan with validation strategy and metrics",
            "parameters": {
                "type": "object",
                "properties": {
                    "research_goal": {"type": "string", "description": "The research objective to plan for"},
                },
                "required": ["research_goal"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search_ml_papers",
            "description": "Search ArXiv for ML research papers",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query for papers"},
                    "max_results": {"type": "integer", "description": "Maximum number of results"},
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "summarize_paper",
            "description": "Summarize a research paper given its title and abstract",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "Paper title"},
                    "abstract": {"type": "string", "description": "Paper abstract"},
                },
                "required": ["title", "abstract"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "analyze_research_gap",
            "description": "Identify gaps in current research for a given topic",
            "parameters": {
                "type": "object",
                "properties": {
                    "topic": {"type": "string", "description": "Research topic to analyze"},
                },
                "required": ["topic"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "generate_citation",
            "description": "Generate a formatted citation for a paper",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "Paper title"},
                    "authors": {"type": "string", "description": "Author names"},
                    "year": {"type": "string", "description": "Publication year"},
                },
                "required": ["title"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_datasets",
            "description": "Recommend datasets for a given task type and domain",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_type": {"type": "string", "description": "classification, regression, clustering"},
                    "domain": {"type": "string", "description": "general, medical, finance, nlp, time_series"},
                },
                "required": ["task_type"],
            },
        },
    },
]
