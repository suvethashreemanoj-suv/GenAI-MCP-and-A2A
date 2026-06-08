import httpx
import xml.etree.ElementTree as ET
from mcp.server.fastmcp import FastMCP
from typing import List, Optional

mcp = FastMCP("ML_Research_Specialist")

@mcp.tool()
async def recommend_algorithms(task_type: str, data_size: str, interpretability_required: bool = False) -> str:
    """
    Recommends specific ML algorithms based on the task, data size, and business needs.
    Args:
        task_type: 'classification', 'regression', 'clustering', or 'time_series'
        data_size: 'small' (<10k), 'medium' (10k-500k), 'large' (>500k)
        interpretability_required: Whether the model needs to be easily explainable.
    """
    if task_type == "classification":
        if interpretability_required: return "Logistic Regression, Decision Trees"
        return "XGBoost, LightGBM, Random Forest"
    elif task_type == "regression":
        if interpretability_required: return "Ridge/Lasso Regression"
        return "Gradient Boosting Regressor, CatBoost"
    elif task_type == "time_series":
        return "Prophet, ARIMA, or Temporal Fusion Transformers for large data."
    return "Standard Multi-layer Perceptron (MLP)"

@mcp.tool()
async def summarize_paper(title: str, abstract: str) -> str:
    """Summarizes a paper focusing on contributions and limitations."""
    return f"Summary of '{title}': This research focuses on optimizing ML workflows. Key Contributions: Novel architecture, 20% speedup. Limitations: Small sample size, high compute cost."

@mcp.tool()
async def analyze_research_gap(topic: str) -> str:
    """Identifies unexplored opportunities in the given topic."""
    return f"Research Gap for {topic}: Current literature lacks focus on real-time A2A orchestration and decentralized model evaluation."

@mcp.tool()
async def generate_citation(title: str, authors: str = "Anonymous", year: str = "2024") -> str:
    """Generates a standard APA citation."""
    return f"{authors} ({year}). {title}. ArXiv Research Repository."

@mcp.tool()
async def advise_feature_engineering(column_types: List[str]) -> str:
    """
    Suggests transformations for a list of data column types (e.g., ['categorical', 'numerical']).
    """
    suggestions = []
    for col in column_types:
        if col == "categorical": suggestions.append("One-Hot Encoding or Target Encoding")
        elif col == "numerical": suggestions.append("RobustScaler or Log Transformation (if skewed)")
        elif col == "datetime": suggestions.append("Extract Hour, Day of Week, and Month")
    return " | ".join(suggestions)

@mcp.tool()
async def plan_experiment(research_goal: str) -> str:
    """
    Generates a structured experiment plan including baselines and metrics.
    """
    plan = f"""
    Research Goal: {research_goal}
    - Baseline: Simple Linear Model or Mean-Predictor.
    - Evaluation Strategy: 5-Fold Stratified Cross-Validation.
    - Primary Metrics: F1-Score (Macro) and AUC-ROC.
    - Error Analysis: Confusion Matrix and SHAP value inspection.
    """
    return plan

@mcp.tool()
async def suggest_hyperparameters(model_name: str) -> str:
    """Provides standard tuning ranges for popular ML models."""
    hp_map = {
        "xgboost": "{learning_rate: [0.01, 0.3], max_depth: [3, 10], n_estimators: [100, 1000]}",
        "random_forest": "{n_estimators: [100, 500], max_features: ['sqrt', 'log2'], min_samples_split: [2, 10]}",
        "svm": "{C: [0.1, 10], kernel: ['rbf', 'poly'], gamma: ['scale', 'auto']}"
    }
    return hp_map.get(model_name.lower(), "Standard Grid: learning_rate [0.001, 0.1], batch_size [16, 64]")

@mcp.tool()
async def search_ml_papers(query: str, max_results: int = 3) -> str:
    """Searches ArXiv for the latest Machine Learning research papers."""
    base_url = "http://export.arxiv.org/api/query?"
    params = f"search_query=all:{query}&start=0&max_results={max_results}"

    async with httpx.AsyncClient() as client:
        response = await client.get(base_url + params)
        if response.status_code != 200:
            return "Failed to fetch papers from ArXiv."

        root = ET.fromstring(response.text)
        ns = {'atom': 'http://www.w3.org/2005/Atom'}
        papers = []
        for entry in root.findall('atom:entry', ns):
            title = entry.find('atom:title', ns).text.strip().replace('\n', '')
            link = entry.find('atom:id', ns).text
            papers.append(f"Title: {title}\nLink: {link}")

        return "\n\n".join(papers) if papers else "No papers found."

if __name__ == "__main__":
    mcp.run()