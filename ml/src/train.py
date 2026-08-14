#!/usr/bin/env python3
"""
Transfer learning training pipeline for Soil & Supper plant classifier.
Uses PyTorch with pretrained ResNet18 for efficiency on GTX 1060.
"""

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
from pathlib import Path
import json
from datetime import datetime

PROCESSED_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "processed"
MODELS_DIR = Path(__file__).resolve().parent.parent.parent / "models"
MODELS_DIR.mkdir(parents=True, exist_ok=True)

BATCH_SIZE = 32
NUM_EPOCHS = 10
LEARNING_RATE = 0.001
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def get_data_loaders(data_dir: Path, batch_size: int = 32):
    """Create train/val/test dataloaders."""
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])

    train_dataset = datasets.ImageFolder(data_dir / "train", transform=transform)
    val_dataset = datasets.ImageFolder(data_dir / "val", transform=transform)
    test_dataset = datasets.ImageFolder(data_dir / "test", transform=transform)

    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)

    return train_loader, val_loader, test_loader, train_dataset.classes


def create_model(num_classes: int, device: torch.device) -> nn.Module:
    """Create pretrained ResNet18 model for transfer learning."""
    model = torch.hub.load("pytorch/vision", "resnet18", pretrained=True)
    model.fc = nn.Linear(model.fc.in_features, num_classes)
    return model.to(device)


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


def train(data_dir: Path, output_dir: Path):
    """Run full training pipeline."""
    print(f"Using device: {DEVICE}")

    train_loader, val_loader, test_loader, classes = get_data_loaders(data_dir, BATCH_SIZE)
    print(f"Classes: {classes}")
    print(f"Train samples: {len(train_loader.dataset)}")
    print(f"Val samples: {len(val_loader.dataset)}")
    print(f"Test samples: {len(test_loader.dataset)}")

    model = create_model(len(classes), DEVICE)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=LEARNING_RATE)

    best_val_acc = 0.0
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

        print(f"Epoch {epoch+1}/{NUM_EPOCHS}")
        print(f"  Train Loss: {train_loss:.4f}, Acc: {train_acc:.4f}")
        print(f"  Val Loss: {val_loss:.4f}, Acc: {val_acc:.4f}")

        if val_acc > best_val_acc:
            best_val_acc = val_acc
            torch.save(model.state_dict(), output_dir / "best_model.pth")
            print(f"  Saved best model (val_acc: {val_acc:.4f})")

    # Save final model and history
    torch.save(model.state_dict(), output_dir / "final_model.pth")

    with open(output_dir / "training_history.json", "w") as f:
        json.dump(history, f, indent=2)

    with open(output_dir / "classes.json", "w") as f:
        json.dump({"classes": classes, "num_classes": len(classes)}, f, indent=2)

    print(f"Training complete. Best val_acc: {best_val_acc:.4f}")
    print(f"Models saved to: {output_dir}")


if __name__ == "__main__":
    if not PROCESSED_DIR.exists():
        print(f"Processed data not found: {PROCESSED_DIR}")
        print("Run split.py first to generate train/val/test splits.")
        exit(1)

    train(PROCESSED_DIR, MODELS_DIR)
