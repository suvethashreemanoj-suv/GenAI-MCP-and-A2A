from typing import Optional

from src.cv_agent.tools.data import CV_DATASETS, CV_SOTA_BENCHMARKS


def _format_dataset_entry(entry: dict) -> str:
    return (
        f"- {entry['name']}\n"
        f"  Size: {entry['size']}\n"
        f"  URL: {entry['url']}\n"
        f"  Notes: {entry['notes']}"
    )


def _normalize_task_key(task: str) -> str:
    task_lower = task.lower().strip()
    aliases = {
        "detection": "object detection",
        "classification": "image classification",
        "segmentation": "semantic segmentation",
        "medical": "medical imaging",
        "video": "video action recognition",
        "vision_language": "vision language",
        "vlm": "vision language",
    }
    return aliases.get(task_lower, task_lower)


def _search_curated_benchmarks(
    task: str, dataset: Optional[str], max_results: int
) -> Optional[str]:
    task_key = _normalize_task_key(task)
    entries = CV_SOTA_BENCHMARKS.get(task_key, [])

    if not entries:
        for key, values in CV_SOTA_BENCHMARKS.items():
            if task_key in key or key in task_key:
                entries = values
                break

    if dataset:
        dataset_lower = dataset.lower()
        filtered = [e for e in entries if dataset_lower in e["dataset"].lower()]
        if filtered:
            entries = filtered

    if not entries:
        return None

    lines = []
    for entry in entries[:max_results]:
        lines.append(
            f"- Model: {entry['model']}\n"
            f"  Dataset: {entry['dataset']}\n"
            f"  Metrics: {entry['metrics']}"
        )

    header = f"SOTA benchmarks for '{task_key}'"
    if dataset:
        header += f" on {dataset}"
    return header + " (curated leaderboard snapshot):\n\n" + "\n\n".join(lines)


async def find_datasets(
    task_type: str,
    domain: str = "general",
    keyword: Optional[str] = None,
) -> str:
    task_type = task_type.lower().strip()
    domain = domain.lower().strip()

    task_data = CV_DATASETS.get(task_type)
    if not task_data:
        available = ", ".join(CV_DATASETS.keys())
        return f"Unknown task_type '{task_type}'. Available: {available}"

    entries = task_data.get(domain, [])
    if not entries and domain != "general":
        entries = task_data.get("general", [])

    if keyword:
        keyword_lower = keyword.lower()
        entries = [
            e
            for e in entries
            if keyword_lower in e["name"].lower()
            or keyword_lower in e["notes"].lower()
        ]

    if not entries:
        return f"No datasets found for task='{task_type}', domain='{domain}', keyword='{keyword}'."

    header = f"Datasets for {task_type} ({domain}):\n"
    return header + "\n\n".join(_format_dataset_entry(e) for e in entries)


async def recommend_models(
    task_type: str,
    compute_budget: str = "medium",
    real_time_required: bool = False,
) -> str:
    task_type = task_type.lower().strip()
    compute_budget = compute_budget.lower().strip()

    recommendations = {
        "classification": {
            "low": "MobileNetV3, EfficientNet-Lite, RegNetY-400MF",
            "medium": "ResNet-50, ConvNeXt-T, DeiT-S, ViT-B/16",
            "high": "ConvNeXt-L, Swin-B, ViT-L/16, EVA-02",
        },
        "detection": {
            "low": "YOLOv8-n/s, SSD-MobileNet, RT-DETR-R18",
            "medium": "Faster R-CNN (ResNet-50), YOLOv8-m/l, DETR, DINO",
            "high": "Cascade R-CNN, YOLOv8-x, Co-DINO, Grounding DINO",
        },
        "segmentation": {
            "low": "DeepLabV3+ (MobileNet), U-Net (lightweight encoder)",
            "medium": "U-Net, DeepLabV3+, SegFormer-B, Mask R-CNN",
            "high": "Mask2Former, Segment Anything Model (SAM), Swin-Transformer segmentation",
        },
        "medical": {
            "low": "U-Net (small), Attention U-Net lite",
            "medium": "U-Net++, nnU-Net, TransUNet, MedSAM",
            "high": "nnU-Net (self-configuring), Swin-UNETR, 3D U-Net for volumetric MRI/CT",
        },
        "video": {
            "low": "MobileNetV2 + TSM, X3D-S",
            "medium": "SlowFast, I3D, Video Swin-T, TimeSformer",
            "high": "VideoMAE, MViTv2, InternVideo2",
        },
        "vision_language": {
            "low": "CLIP ViT-B/32, SigLIP base",
            "medium": "CLIP ViT-L/14, BLIP-2, LLaVA-1.5",
            "high": "GPT-4V-class APIs, LLaVA-NeXT, InternVL2, Florence-2",
        },
    }

    task_recs = recommendations.get(task_type)
    if not task_recs:
        available = ", ".join(recommendations.keys())
        return f"Unknown task_type '{task_type}'. Available: {available}"

    models = task_recs.get(compute_budget, task_recs["medium"])
    latency_note = (
        " Prioritize distilled or TensorRT-optimized variants for real-time deployment."
        if real_time_required
        else ""
    )
    return (
        f"Recommended models for {task_type} (compute: {compute_budget}): {models}."
        f"{latency_note}"
    )


async def search_benchmarks(
    task: str,
    dataset: Optional[str] = None,
    max_results: int = 5,
) -> str:
    from src.cv_agent.tools.general import search_cv_papers

    curated = _search_curated_benchmarks(task, dataset, max_results)
    if curated:
        papers = await search_cv_papers(
            f"state of the art {task} {dataset or ''}", max_results=2
        )
        if papers and papers != "No papers found.":
            return curated + "\n\nRecent papers:\n" + papers
        return curated

    query = f"state of the art {task}"
    if dataset:
        query += f" {dataset}"
    return await search_cv_papers(query, max_results=max_results)
