import httpx
import xml.etree.ElementTree as ET


async def search_ml_papers(query: str, max_results: int = 3) -> str:
    base_url = "http://export.arxiv.org/api/query?"
    params = f"search_query=all:{query}&start=0&max_results={max_results}"

    async with httpx.AsyncClient() as client:
        response = await client.get(base_url + params)
        if response.status_code != 200:
            return "Failed to fetch papers from ArXiv."

        root = ET.fromstring(response.text)
        ns = {"atom": "http://www.w3.org/2005/Atom"}
        papers = []
        for entry in root.findall("atom:entry", ns):
            title = entry.find("atom:title", ns).text.strip().replace("\n", "")
            link = entry.find("atom:id", ns).text
            papers.append(f"Title: {title}\nLink: {link}")

        return "\n\n".join(papers) if papers else "No papers found."


async def summarize_paper(title: str, abstract: str) -> str:
    return f"Summary of '{title}': This research focuses on optimizing ML workflows. Key Contributions: Novel architecture, 20% speedup. Limitations: Small sample size, high compute cost."


async def analyze_research_gap(topic: str) -> str:
    return f"Research Gap for {topic}: Current literature lacks focus on real-time A2A orchestration and decentralized model evaluation."


async def generate_citation(title: str, authors: str = "Anonymous", year: str = "2024") -> str:
    return f"{authors} ({year}). {title}. ArXiv Research Repository."


async def list_datasets(task_type: str, domain: str = "general") -> str:
    datasets = {
        "classification": {
            "general": "UCI Machine Learning Repository, Kaggle Datasets, OpenML",
            "medical": "MIMIC-III, ChestX-ray14, ISIC Skin Lesion",
            "finance": "Credit Card Fraud Dataset (Kaggle), Lending Club, Yahoo Finance",
            "nlp": "IMDB Reviews, SST-2, AG News, Yelp Reviews",
        },
        "regression": {
            "general": "Boston Housing, California Housing, Auto MPG",
            "time_series": "Air Quality (UCI), Traffic Volume (Kaggle), Energy Consumption",
        },
        "clustering": {
            "general": "Iris, Wine, MNIST (for embedding clustering)",
        },
    }
    task_map = datasets.get(task_type, {})
    return task_map.get(domain, task_map.get("general", "Kaggle Datasets, UCI ML Repository, Papers With Code Datasets"))
