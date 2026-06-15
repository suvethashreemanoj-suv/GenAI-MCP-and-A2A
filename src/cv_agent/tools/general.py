import httpx
import xml.etree.ElementTree as ET


async def search_cv_papers(query: str, max_results: int = 3) -> str:
    base_url = "https://export.arxiv.org/api/query?"
    params = f"search_query=all:{query}+AND+cat:cs.CV&start=0&max_results={max_results}"

    async with httpx.AsyncClient(timeout=20.0, follow_redirects=True) as client:
        response = await client.get(base_url + params)
        if response.status_code != 200:
            return "Failed to fetch papers from ArXiv."

        root = ET.fromstring(response.text)
        ns = {"atom": "http://www.w3.org/2005/Atom"}
        papers = []
        for entry in root.findall("atom:entry", ns):
            title = entry.find("atom:title", ns).text.strip().replace("\n", " ")
            link = entry.find("atom:id", ns).text
            summary = entry.find("atom:summary", ns)
            abstract = summary.text.strip().replace("\n", " ")[:300] if summary is not None else ""
            papers.append(f"Title: {title}\nLink: {link}\nAbstract: {abstract}...")

        return "\n\n".join(papers) if papers else "No papers found."


async def analyze_cv_research_gap(topic: str) -> str:
    return (
        f"Research Gap for '{topic}': "
        "Current literature often lacks robust cross-domain generalization, "
        "efficient edge deployment, and standardized multimodal evaluation "
        "protocols combining vision with clinical or textual context."
    )


async def plan_cv_experiment(research_goal: str, task_type: str = "classification") -> str:
    metrics_map = {
        "classification": "Top-1/Top-5 Accuracy, F1-Score, Confusion Matrix",
        "detection": "mAP@0.5, mAP@0.5:0.95, FPS",
        "segmentation": "mIoU, Dice Coefficient, Boundary F1",
        "medical": "Dice, Hausdorff Distance, Sensitivity/Specificity",
        "video": "Top-1 Accuracy, mAP (temporal), Inference FPS",
        "vision_language": "CIDEr, BLEU, VQA Accuracy, Retrieval Recall@K",
    }
    metrics = metrics_map.get(task_type.lower(), "Task-specific metrics")

    return f"""
Research Goal: {research_goal}
Task Type: {task_type}
- Baseline: ResNet-50 (classification) or YOLOv8-n (detection) as sanity check.
- Data Split: Train/Val/Test (70/15/15) with stratification; use k-fold for small medical sets.
- Augmentation: Random flip, color jitter, MixUp/CutMix for classification; mosaic for detection.
- Primary Metrics: {metrics}
- Validation: Early stopping on val metric; report confidence intervals over 3 seeds.
- Error Analysis: Failure case gallery, per-class mAP/IoU breakdown, calibration plots.
"""
