import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from src.shared.schema import AgentResponse
from src.ml_agent.mcp_server import (
    recommend_algorithms,
    advise_feature_engineering,
    suggest_hyperparameters,
    summarize_paper,
    analyze_research_gap,
    generate_citation,
    plan_experiment,
    search_ml_papers
)
import httpx

load_dotenv()

class MLAgent:
    def __init__(self):
        # Configuration for personal server
        self.model_id = os.getenv("MODEL_ID", "deepseek-chat")
        self.client = OpenAI(
            api_key=os.getenv("DEEPSEEK_API_KEY"),
            base_url=os.getenv("DEEPSEEK_BASE_URL", "https://apiv5.hareeshworks.in/v1")
        )
        self.agent_name = "ML_Research_Agent"

    async def solve(self, query: str) -> AgentResponse:

        papers = await search_ml_papers(query)
        gap_data = await analyze_research_gap(query)
        citation_example = await generate_citation(query)
        summary_data = await summarize_paper(query, papers[:200] if papers else "N/A")

        algo_suggestions = await recommend_algorithms(task_type="classification", data_size="medium")
        feature_strategy = await advise_feature_engineering(column_types=["numerical", "categorical", "datetime"])
        hp_guidelines = await suggest_hyperparameters("xgboost")

        experiment_plan = await plan_experiment(query)

        system_prompt = f"""
        You are a Specialized Machine Learning Research Agent.
        
        LITERATURE REVIEW CONTEXT:
        {papers}
        {summary_data}
        
        RESEARCH GAP & CITATION STYLE:
        {gap_data}
        {citation_example}

        ML TECHNICAL GUIDELINES:
        Algorithms: {algo_suggestions}
        Feature Engineering: {feature_strategy}
        Hyperparameters: {hp_guidelines}

        EXPERIMENT PLAN TEMPLATE:
        {experiment_plan}

        Instructions:
        Analyze the research query. You MUST provide a response that includes:
        - Literature Review (Summary of existing research)
        - Research Gaps (What is missing in current studies)
        - Datasets (Recommended data sources)
        - Models (Proposed ML architectures)
        - Evaluation Strategy (Metrics and validation plan)
        
        Return your answer in valid JSON format only.
        
        JSON Structure:
        {{
            "recommendations": ["step-by-step implementation list"],
            "datasets": ["list of datasets"],
            "models": ["list of models"],
            "reasoning": "A full report covering: Literature Review, Key Contributions, Limitations, and Evaluation Strategy"
        }}
        """

        response = self.client.chat.completions.create(
            model=self.model_id,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": query}
            ],
            response_format={"type": "json_object"}
        )

        try:
            content = response.choices[0].message.content
            data = json.loads(content)
        except Exception as e:
            print(f"Error parsing LLM response: {e}")
            data = {
                "recommendations": [],
                "datasets": [],
                "models": [],
                "reasoning": "Error processing research proposal."
            }

        return AgentResponse(
            agent_name=self.agent_name,
            recommendations=data.get("recommendations", []),
            datasets=data.get("datasets", []),
            models=data.get("models", []),
            reasoning=data.get("reasoning", "No reasoning provided.")
        )

if __name__ == "__main__":
    import asyncio
    agent = MLAgent()
    async def test():
        print(f"--- Starting Research for: 'predicting credit card fraud' ---")
        res = await agent.solve("I want to build a model for predicting credit card fraud.")
        print(f"\nFinal Report Summary:\n{res.reasoning}")
        print(f"\nDatasets Recommended: {res.datasets}")
        print(f"\nModels Recommended: {res.models}")
    asyncio.run(test())