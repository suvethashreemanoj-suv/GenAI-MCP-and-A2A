CV_DATASETS = {
    "classification": {
        "general": [
            {
                "name": "ImageNet",
                "size": "1.2M images, 1000 classes",
                "url": "https://www.image-net.org/",
                "notes": "Standard benchmark for image classification and pre-training.",
            },
            {
                "name": "CIFAR-10 / CIFAR-100",
                "size": "60K images",
                "url": "https://www.cs.toronto.edu/~kriz/cifar.html",
                "notes": "Small-scale classification for rapid prototyping.",
            },
        ],
        "fine_grained": [
            {
                "name": "Stanford Cars",
                "size": "16K images, 196 classes",
                "url": "https://ai.stanford.edu/~jkrause/cars/car_dataset.html",
                "notes": "Fine-grained vehicle classification.",
            },
        ],
    },
    "detection": {
        "general": [
            {
                "name": "COCO (Common Objects in Context)",
                "size": "330K images, 80 object categories",
                "url": "https://cocodataset.org/",
                "notes": "Primary benchmark for object detection, instance segmentation, and keypoints.",
            },
            {
                "name": "Open Images V7",
                "size": "9M images, 600 box-level classes",
                "url": "https://storage.googleapis.com/openimages/web/index.html",
                "notes": "Large-scale detection with diverse real-world scenes.",
            },
            {
                "name": "Pascal VOC",
                "size": "20 object classes",
                "url": "http://host.robots.ox.ac.uk/pascal/VOC/",
                "notes": "Classic detection benchmark; useful for legacy comparisons.",
            },
        ],
    },
    "segmentation": {
        "general": [
            {
                "name": "ADE20K",
                "size": "25K scenes, 150 semantic categories",
                "url": "https://groups.csail.mit.edu/vision/datasets/ADE20K/",
                "notes": "Scene parsing and semantic segmentation.",
            },
            {
                "name": "Cityscapes",
                "size": "5K fine-annotated urban scenes",
                "url": "https://www.cityscapes-dataset.com/",
                "notes": "Autonomous driving semantic segmentation benchmark.",
            },
        ],
        "medical": [
            {
                "name": "ISIC (Skin Lesion)",
                "size": "Varies by challenge year",
                "url": "https://challenge.isic-archive.com/",
                "notes": "Dermatology segmentation and classification.",
            },
        ],
    },
    "medical": {
        "general": [
            {
                "name": "ChestX-ray14 (NIH)",
                "size": "112K frontal chest X-rays",
                "url": "https://nihcc.app.box.com/v/ChestXray-NIHCC",
                "notes": "Multi-label thoracic disease classification.",
            },
            {
                "name": "MIMIC-CXR",
                "size": "377K chest radiographs",
                "url": "https://physionet.org/content/mimic-cxr/",
                "notes": "Large clinical chest X-ray corpus with reports.",
            },
            {
                "name": "BRATS (Brain Tumor Segmentation)",
                "size": "Multi-modal MRI volumes",
                "url": "https://www.synapse.org/brats",
                "notes": "3D brain tumor segmentation challenge.",
            },
            {
                "name": "CheXpert",
                "size": "224K chest radiographs",
                "url": "https://stanfordmlgroup.github.io/competitions/chexpert/",
                "notes": "Uncertainty-labeled chest X-ray benchmark from Stanford.",
            },
        ],
    },
    "video": {
        "general": [
            {
                "name": "Kinetics-700",
                "size": "650K video clips, 700 action classes",
                "url": "https://deepmind.google/datasets/kinetics/",
                "notes": "Large-scale action recognition benchmark.",
            },
            {
                "name": "UCF-101",
                "size": "13K clips, 101 action classes",
                "url": "https://www.crcv.ucf.edu/data/UCF101.php",
                "notes": "Classic action recognition dataset.",
            },
            {
                "name": "ActivityNet",
                "size": "20K untrimmed videos",
                "url": "http://activity-net.org/",
                "notes": "Temporal action localization and recognition.",
            },
        ],
    },
    "vision_language": {
        "general": [
            {
                "name": "COCO Captions",
                "size": "330K images with 5 captions each",
                "url": "https://cocodataset.org/#captions-2015",
                "notes": "Image captioning and VLM pre-training.",
            },
            {
                "name": "Visual Genome",
                "size": "108K images with dense annotations",
                "url": "https://homes.cs.washington.edu/~ranjay/visualgenome/",
                "notes": "Scene graphs, region descriptions, and VQA.",
            },
            {
                "name": "LAION-5B",
                "size": "5.85B image-text pairs",
                "url": "https://laion.ai/blog/laion-5b/",
                "notes": "Web-scale dataset for CLIP-style pre-training.",
            },
        ],
    },
}

CV_SOTA_BENCHMARKS = {
    "image classification": [
        {"model": "EVA-02-L", "dataset": "ImageNet-1K", "metrics": "Top-1: 90.0%"},
        {"model": "ConvNeXt V2-H", "dataset": "ImageNet-1K", "metrics": "Top-1: 88.9%"},
        {"model": "ViT-G/14 (SAM)", "dataset": "ImageNet-1K", "metrics": "Top-1: 88.5%"},
    ],
    "object detection": [
        {"model": "Co-DINO", "dataset": "COCO", "metrics": "mAP: 66.0%"},
        {"model": "YOLOv8-x", "dataset": "COCO", "metrics": "mAP@0.5:0.95: 53.9%"},
        {"model": "DINO", "dataset": "COCO", "metrics": "mAP: 63.3%"},
        {"model": "Grounding DINO", "dataset": "COCO", "metrics": "Zero-shot mAP: 52.5%"},
    ],
    "semantic segmentation": [
        {"model": "Mask2Former (Swin-L)", "dataset": "ADE20K", "metrics": "mIoU: 57.7%"},
        {"model": "SegFormer-B5", "dataset": "ADE20K", "metrics": "mIoU: 51.0%"},
        {"model": "Mask2Former", "dataset": "Cityscapes", "metrics": "mIoU: 83.3%"},
    ],
    "instance segmentation": [
        {"model": "Mask DINO", "dataset": "COCO", "metrics": "mAP: 54.5%"},
        {"model": "Cascade Mask R-CNN", "dataset": "COCO", "metrics": "mAP: 46.3%"},
    ],
    "medical imaging": [
        {"model": "nnU-Net", "dataset": "BRATS", "metrics": "Dice: ~0.91 (ensemble)"},
        {"model": "CheXpert DenseNet-121", "dataset": "CheXpert", "metrics": "AUC: 0.89 (avg)"},
        {"model": "TransUNet", "dataset": "Synapse Multi-Organ", "metrics": "Mean Dice: 77.5%"},
    ],
    "video action recognition": [
        {"model": "VideoMAE V2", "dataset": "Kinetics-400", "metrics": "Top-1: 90.0%"},
        {"model": "MViTv2-L", "dataset": "Kinetics-400", "metrics": "Top-1: 87.8%"},
        {"model": "TimeSformer-L", "dataset": "Kinetics-400", "metrics": "Top-1: 80.7%"},
    ],
    "vision language": [
        {"model": "LLaVA-1.5-13B", "dataset": "VQA v2", "metrics": "Accuracy: 80.0%"},
        {"model": "CLIP ViT-L/14", "dataset": "ImageNet Zero-Shot", "metrics": "Top-1: 75.5%"},
        {"model": "BLIP-2", "dataset": "COCO Caption", "metrics": "CIDEr: 144.5"},
    ],
}

