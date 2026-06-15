from src.cv_agent.tools.specialized import find_datasets, recommend_models, search_benchmarks
from src.cv_agent.tools.general import (
    search_cv_papers,
    analyze_cv_research_gap,
    plan_cv_experiment,
)

SPECIALIZED_TOOLS = [find_datasets, recommend_models, search_benchmarks]
GENERAL_TOOLS = [search_cv_papers, analyze_cv_research_gap, plan_cv_experiment]
ALL_TOOLS = SPECIALIZED_TOOLS + GENERAL_TOOLS
TOOL_MAP = {fn.__name__: fn for fn in ALL_TOOLS}

TOOL_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "find_datasets",
            "description": "Dataset Finder: recommend CV datasets (COCO, ImageNet, medical, etc.)",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_type": {
                        "type": "string",
                        "description": "classification, detection, segmentation, medical, video, or vision_language",
                    },
                    "domain": {"type": "string", "description": "general, fine_grained, or medical"},
                    "keyword": {"type": "string", "description": "Optional filter e.g. COCO, chest"},
                },
                "required": ["task_type"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "recommend_models",
            "description": "Model Recommender: suggest CNNs, ViTs, or segmentation models",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_type": {"type": "string", "description": "CV task type"},
                    "compute_budget": {"type": "string", "description": "low, medium, or high"},
                    "real_time_required": {"type": "boolean", "description": "Whether low latency is needed"},
                },
                "required": ["task_type"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search_benchmarks",
            "description": "Benchmark Search: identify SOTA models on standard CV leaderboards",
            "parameters": {
                "type": "object",
                "properties": {
                    "task": {"type": "string", "description": "e.g. object detection, semantic segmentation"},
                    "dataset": {"type": "string", "description": "Optional dataset filter e.g. COCO"},
                    "max_results": {"type": "integer", "description": "Number of SOTA entries"},
                },
                "required": ["task"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search_cv_papers",
            "description": "Search ArXiv cs.CV for recent computer vision papers",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query"},
                    "max_results": {"type": "integer", "description": "Maximum number of results"},
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "analyze_cv_research_gap",
            "description": "Identify research gaps in a computer vision topic",
            "parameters": {
                "type": "object",
                "properties": {
                    "topic": {"type": "string", "description": "Research topic"},
                },
                "required": ["topic"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "plan_cv_experiment",
            "description": "Generate a structured CV experiment plan with metrics and validation",
            "parameters": {
                "type": "object",
                "properties": {
                    "research_goal": {"type": "string", "description": "Research objective"},
                    "task_type": {"type": "string", "description": "CV task type"},
                },
                "required": ["research_goal"],
            },
        },
    },
]
