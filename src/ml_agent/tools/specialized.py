from typing import List


async def recommend_algorithms(task_type: str, data_size: str, interpretability_required: bool = False) -> str:
    if task_type == "classification":
        if interpretability_required:
            return "Logistic Regression, Decision Trees"
        return "XGBoost, LightGBM, Random Forest"
    elif task_type == "regression":
        if interpretability_required:
            return "Ridge/Lasso Regression"
        return "Gradient Boosting Regressor, CatBoost"
    elif task_type == "time_series":
        return "Prophet, ARIMA, or Temporal Fusion Transformers for large data."
    return "Standard Multi-layer Perceptron (MLP)"


async def suggest_hyperparameters(model_name: str) -> str:
    hp_map = {
        "xgboost": "{learning_rate: [0.01, 0.3], max_depth: [3, 10], n_estimators: [100, 1000]}",
        "random_forest": "{n_estimators: [100, 500], max_features: ['sqrt', 'log2'], min_samples_split: [2, 10]}",
        "svm": "{C: [0.1, 10], kernel: ['rbf', 'poly'], gamma: ['scale', 'auto']}",
    }
    return hp_map.get(model_name.lower(), "Standard Grid: learning_rate [0.001, 0.1], batch_size [16, 64]")


async def advise_feature_engineering(column_types: List[str]) -> str:
    suggestions = []
    for col in column_types:
        if col == "categorical":
            suggestions.append("One-Hot Encoding or Target Encoding")
        elif col == "numerical":
            suggestions.append("RobustScaler or Log Transformation (if skewed)")
        elif col == "datetime":
            suggestions.append("Extract Hour, Day of Week, and Month")
    return " | ".join(suggestions)


async def plan_experiment(research_goal: str) -> str:
    plan = f"""
    Research Goal: {research_goal}
    - Baseline: Simple Linear Model or Mean-Predictor.
    - Evaluation Strategy: 5-Fold Stratified Cross-Validation.
    - Primary Metrics: F1-Score (Macro) and AUC-ROC.
    - Error Analysis: Confusion Matrix and SHAP value inspection.
    """
    return plan
