#!/usr/bin/env python3
"""
Phase 34: Train MobileNetV3-based crop recognition classifier.

Trains a 12-class crop classifier using only commercially approved data.
Classes with insufficient data are documented as gaps.

Backbone: MobileNetV3 Large (ImageNet pretrained)
License: MobileNetV3 is part of PyTorch/torchvision, BSD-style license
Input: 224x224 RGB
Optimizer: Adam
Loss: CrossEntropyLoss
"""

import json
import os
import random
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, random_split
from torchvision import datasets, transforms
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    precision_score,
    recall_score,
    confusion_matrix,
    balanced_accuracy_score,
)
import onnx

# Reproducibility
SEED = 42
random.seed(SEED)
np.random.seed(SEED)
torch.manual_seed(SEED)
torch.cuda.manual_seed(SEED)
torch.backends.cudnn.deterministic = True
torch.backends.cudnn.benchmark = False

# Paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
TRAINING_DATA_DIR = PROJECT_ROOT / "training_data"
PROCESSED_DIR = TRAINING_DATA_DIR / "processed" / "crops"
MODELS_DIR = PROJECT_ROOT / "ml" / "models"
MODELS_DIR.mkdir(parents=True, exist_ok=True)
MANIFESTS_DIR = TRAINING_DATA_DIR / "manifests"

# Hyperparameters
BATCH_SIZE = 32
NUM_EPOCHS = 10
LEARNING_RATE = 0.001
WEIGHT_DECAY = 1e-5
INPUT_SIZE = 224
EARLY_STOPPING_PATIENCE = 3
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Phase 34 target classes
PHASE34_CLASSES = [
    "Tomato",
    "Pepper_sweet",
    "Eggplant",
    "Cucumber",
    "Summer_squash",
    "Bean",
    "Pea",
    "Corn",
    "Broccoli",
    "Lettuce",
    "Carrot",
    "Strawberry",
]


def get_transforms():
    """Get training and validation transforms."""
    train_transform = transforms.Compose([
        transforms.Resize((INPUT_SIZE, INPUT_SIZE)),
        transforms.RandomHorizontalFlip(p=0.5),
        transforms.RandomRotation(15),
        transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])

    val_transform = transforms.Compose([
        transforms.Resize((INPUT_SIZE, INPUT_SIZE)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])

    return train_transform, val_transform


def load_datasets():
    """Load crop datasets from processed directory."""
    train_transform, val_transform = get_transforms()

    # Only include classes that have images
    train_dir = PROCESSED_DIR / "train"
    valid_class_names = [d.name for d in train_dir.iterdir() if d.is_dir() and any(d.rglob("*"))]
    valid_class_names.sort()

    print(f"Classes with data: {valid_class_names}")

    # Load full dataset from train directory (we'll re-split)
    full_dataset = datasets.ImageFolder(
        PROCESSED_DIR / "train",
        transform=train_transform,
        # Only include valid classes
        is_valid_file=lambda x: Path(x).parent.name in valid_class_names,
    )

    # Filter dataset to only include valid classes
    # ImageFolder doesn't support filtering by class name directly,
    # so we need to filter the samples
    filtered_samples = []
    filtered_classes = set()
    for path, class_idx in full_dataset.samples:
        class_name = full_dataset.classes[class_idx]
        if class_name in valid_class_names:
            filtered_samples.append((path, class_idx))
            filtered_classes.add(class_name)

    # Update dataset with filtered samples
    full_dataset.samples = filtered_samples
    full_dataset.targets = [s[1] for s in filtered_samples]

    # Get class names from the dataset
    class_names = [c for c in full_dataset.classes if c in valid_class_names]
    print(f"Training classes: {class_names}")
    print(f"Total images: {len(full_dataset)}")

    # Check which Phase 34 classes are missing
    missing_classes = [cls for cls in PHASE34_CLASSES if cls not in class_names]
    if missing_classes:
        print(f"WARNING: Missing classes with no data: {missing_classes}")

    # Split into train and val (80/20 within the train split)
    train_size = int(0.8 * len(full_dataset))
    val_size = len(full_dataset) - train_size
    train_dataset, val_dataset = random_split(
        full_dataset, [train_size, val_size], generator=torch.Generator().manual_seed(SEED)
    )

    # Load test dataset
    test_dataset = datasets.ImageFolder(
        PROCESSED_DIR / "test",
        transform=val_transform,
    )

    # Filter test dataset too
    test_filtered = [(p, c) for p, c in test_dataset.samples if test_dataset.classes[c] in valid_class_names]
    test_dataset.samples = test_filtered
    test_dataset.targets = [s[1] for s in test_filtered]

    print(f"Train: {len(train_dataset)}, Val: {val_size}, Test: {len(test_dataset)}")

    return train_dataset, val_dataset, test_dataset, class_names


def create_model(num_classes: int) -> nn.Module:
    """Create MobileNetV3 Large model for crop classification."""
    model = torch.hub.load("pytorch/vision", "mobilenet_v3_large", pretrained=True)
    # Replace the classifier head
    model.classifier[3] = nn.Linear(model.classifier[3].in_features, num_classes)
    return model


def train_epoch(model, dataloader, criterion, optimizer, device):
    """Train for one epoch."""
    model.train()
    running_loss = 0.0
    correct = 0
    total = 0

    for images, labels in dataloader:
        images, labels = images.to(device), labels.to(device)
        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        running_loss += loss.item() * images.size(0)
        _, predicted = torch.max(outputs.data, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()

    epoch_loss = running_loss / total
    epoch_acc = correct / total
    return epoch_loss, epoch_acc


def validate(model, dataloader, criterion, device):
    """Validate model."""
    model.eval()
    running_loss = 0.0
    correct = 0
    total = 0

    with torch.no_grad():
        for images, labels in dataloader:
            images, labels = images.to(device), labels.to(device)
            outputs = model(images)
            loss = criterion(outputs, labels)

            running_loss += loss.item() * images.size(0)
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()

    epoch_loss = running_loss / total
    epoch_acc = correct / total
    return epoch_loss, epoch_acc


def evaluate_model(model, dataloader, device, class_names):
    """Full evaluation with all required metrics."""
    model.eval()
    all_preds = []
    all_labels = []

    with torch.no_grad():
        for images, labels in dataloader:
            images = images.to(device)
            outputs = model(images)
            _, predicted = torch.max(outputs.data, 1)
            all_preds.extend(predicted.cpu().numpy())
            all_labels.extend(labels.numpy())

    all_preds = np.array(all_preds)
    all_labels = np.array(all_labels)

    # Metrics
    accuracy = accuracy_score(all_labels, all_preds)
    macro_f1 = f1_score(all_labels, all_preds, average="macro", zero_division=0)
    weighted_f1 = f1_score(all_labels, all_preds, average="weighted", zero_division=0)
    balanced_acc = balanced_accuracy_score(all_labels, all_preds)

    # Per-class metrics
    per_class_precision = precision_score(all_labels, all_preds, average=None, zero_division=0)
    per_class_recall = recall_score(all_labels, all_preds, average=None, zero_division=0)
    per_class_f1 = f1_score(all_labels, all_preds, average=None, zero_division=0)

    # Confusion matrix
    cm = confusion_matrix(all_labels, all_preds)

    return {
        "accuracy": float(accuracy),
        "macro_f1": float(macro_f1),
        "weighted_f1": float(weighted_f1),
        "balanced_accuracy": float(balanced_acc),
        "per_class_precision": per_class_precision.tolist(),
        "per_class_recall": per_class_recall.tolist(),
        "per_class_f1": per_class_f1.tolist(),
        "confusion_matrix": cm.tolist(),
        "class_names": class_names,
    }


def export_to_onnx(model, input_size, device, export_path):
    """Export model to ONNX format."""
    model.eval()
    dummy_input = torch.randn(1, 3, input_size, input_size).to(device)
    torch.onnx.export(
        model,
        dummy_input,
        export_path,
        export_params=True,
        opset_version=17,
        do_constant_folding=True,
        input_names=["input"],
        output_names=["output"],
        dynamic_axes={"input": {0: "batch_size"}, "output": {0: "batch_size"}},
    )
    print(f"ONNX model exported: {export_path}")

    # Verify ONNX model
    onnx_model = onnx.load(export_path)
    onnx.checker.check_model(onnx_model)
    print("ONNX model verified successfully")


def train():
    """Main training function."""
    print("=" * 60)
    print("PHASE 34: CROP RECOGNITION MODEL TRAINING")
    print("=" * 60)
    print(f"Device: {DEVICE}")
    print(f"Backbone: MobileNetV3 Large (ImageNet pretrained)")
    print(f"Input size: {INPUT_SIZE}x{INPUT_SIZE}")
    print(f"Batch size: {BATCH_SIZE}")
    print(f"Learning rate: {LEARNING_RATE}")
    print(f"Epochs: {NUM_EPOCHS}")
    print(f"Seed: {SEED}")
    print("=" * 60)

    # Load datasets
    train_dataset, val_dataset, test_dataset, class_names = load_datasets()
    num_classes = len(class_names)

    # Create data loaders
    train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True, num_workers=0)
    val_loader = DataLoader(val_dataset, batch_size=BATCH_SIZE, shuffle=False, num_workers=0)
    test_loader = DataLoader(test_dataset, batch_size=BATCH_SIZE, shuffle=False, num_workers=0)

    # Create model
    model = create_model(num_classes)
    model = model.to(DEVICE)

    # Loss and optimizer
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=LEARNING_RATE, weight_decay=WEIGHT_DECAY)

    # Training loop
    best_val_acc = 0.0
    patience_counter = 0
    history = []

    for epoch in range(NUM_EPOCHS):
        train_loss, train_acc = train_epoch(model, train_loader, criterion, optimizer, DEVICE)
        val_loss, val_acc = validate(model, val_loader, criterion, DEVICE)

        history.append({
            "epoch": epoch + 1,
            "train_loss": train_loss,
            "train_acc": train_acc,
            "val_loss": val_loss,
            "val_acc": val_acc,
        })

        print(f"Epoch {epoch+1:2d}/{NUM_EPOCHS} | "
              f"Train Loss: {train_loss:.4f} Acc: {train_acc:.4f} | "
              f"Val Loss: {val_loss:.4f} Acc: {val_acc:.4f}")

        # Early stopping
        if val_acc > best_val_acc:
            best_val_acc = val_acc
            patience_counter = 0
            torch.save(model.state_dict(), MODELS_DIR / "crop_model_best.pth")
            print(f"  -> Saved best model (val_acc: {val_acc:.4f})")
        else:
            patience_counter += 1
            if patience_counter >= EARLY_STOPPING_PATIENCE:
                print(f"Early stopping triggered at epoch {epoch+1}")
                break

    # Load best model
    model.load_state_dict(torch.load(MODELS_DIR / "crop_model_best.pth", weights_only=True))

    # Final evaluation on test set
    print("\n" + "=" * 60)
    print("EVALUATION ON TEST SET")
    print("=" * 60)

    test_metrics = evaluate_model(model, test_loader, DEVICE, class_names)

    print(f"Accuracy:            {test_metrics['accuracy']:.4f}")
    print(f"Macro F1:            {test_metrics['macro_f1']:.4f}")
    print(f"Weighted F1:         {test_metrics['weighted_f1']:.4f}")
    print(f"Balanced Accuracy:   {test_metrics['balanced_accuracy']:.4f}")
    print("\nPer-class metrics:")
    print(f"{'Class':<20} {'Precision':>10} {'Recall':>10} {'F1':>10}")
    print("-" * 52)
    for i, cls in enumerate(class_names):
        print(f"{cls:<20} {test_metrics['per_class_precision'][i]:>10.4f} "
              f"{test_metrics['per_class_recall'][i]:>10.4f} {test_metrics['per_class_f1'][i]:>10.4f}")

    print("\nConfusion Matrix:")
    print("Rows: true, Cols: predicted")
    header = "          " + "  ".join(f"{c[:8]:>8}" for c in class_names)
    print(header)
    for i, row in enumerate(test_metrics["confusion_matrix"]):
        row_str = "  ".join(f"{v:>8}" for v in row)
        print(f"{class_names[i][:8]:>8}  {row_str}")

    # Export to ONNX
    print("\n" + "=" * 60)
    print("EXPORTING TO ONNX")
    print("=" * 60)
    onnx_path = MODELS_DIR / "crop_model.onnx"
    export_to_onnx(model, INPUT_SIZE, DEVICE, onnx_path)

    # Save results
    results = {
        "model_name": "MobileNetV3 Large",
        "backbone": "mobilenet_v3_large",
        "pretrained_weights": "ImageNet",
        "license": "BSD-style (PyTorch/torchvision)",
        "input_size": INPUT_SIZE,
        "num_classes": num_classes,
        "classes": class_names,
        "batch_size": BATCH_SIZE,
        "learning_rate": LEARNING_RATE,
        "epochs_trained": len(history),
        "best_val_acc": best_val_acc,
        "optimizer": "Adam",
        "loss": "CrossEntropyLoss",
        "seed": SEED,
        "device": str(DEVICE),
        "train_samples": len(train_dataset),
        "val_samples": len(val_dataset),
        "test_samples": len(test_dataset),
        "test_metrics": test_metrics,
        "training_history": history,
        "missing_classes": [cls for cls in PHASE34_CLASSES if cls not in class_names],
    }

    results_path = MODELS_DIR / "crop_model_results.json"
    with open(results_path, "w") as f:
        json.dump(results, f, indent=2, default=str)
    print(f"\nResults saved: {results_path}")

    # Save classes mapping
    classes_info = {
        "phase34_classes": PHASE34_CLASSES,
        "trained_classes": class_names,
        "missing_classes": [cls for cls in PHASE34_CLASSES if cls not in class_names],
        "class_to_idx": {cls: i for i, cls in enumerate(class_names)},
    }
    classes_path = MODELS_DIR / "crop_classes.json"
    with open(classes_path, "w") as f:
        json.dump(classes_info, f, indent=2)
    print(f"Classes info saved: {classes_path}")

    print("\n" + "=" * 60)
    print("TRAINING COMPLETE")
    print("=" * 60)

    return model, results


if __name__ == "__main__":
    train()
