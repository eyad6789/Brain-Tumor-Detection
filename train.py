"""
Brain Tumor Detection — PyTorch Training Script
ResNet50 fine-tuned on Brain Tumor MRI Dataset (4 classes)
Classes: pituitary=0, notumor=1, meningioma=2, glioma=3

Optimizations vs original:
- Weight decay (L2 regularization) on Adam
- ReduceLROnPlateau LR scheduling
- Stronger data augmentation (ColorJitter, GaussianBlur, vertical flip)
- Label smoothing loss
- BatchNorm in custom head
- Saves learning_curves.png and confusion_matrix.png after training
"""

import os
import glob
import argparse
import csv
import copy

import cv2
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from torchvision import models, transforms
from PIL import Image

# ─── Config ───────────────────────────────────────────────────────────────────
CLASSES = {"pituitary": 0, "notumor": 1, "meningioma": 2, "glioma": 3}
CLASS_NAMES = ["Pituitary", "No Tumor", "Meningioma", "Glioma"]
IMG_SIZE = 224
BATCH_SIZE = 32
EPOCHS = 20            # higher ceiling — early stopping controls actual stopping
LR = 1e-4
WEIGHT_DECAY = 1e-4    # L2 regularization to fight overfitting
PATIENCE = 5
MODEL_SAVE_PATH = "model_class.pth"
LOG_PATH = "model_log.csv"

# ─── Dataset ──────────────────────────────────────────────────────────────────
class BrainTumorDataset(Dataset):
    def __init__(self, root_dir, transform=None):
        self.samples = []
        self.transform = transform
        for class_name, label in CLASSES.items():
            pattern = os.path.join(root_dir, class_name, "*.jpg")
            for path in glob.glob(pattern):
                self.samples.append((path, label))

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        path, label = self.samples[idx]
        img = cv2.imread(path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        if self.transform:
            img = self.transform(img)
        return img, label


# ─── Transforms (stronger augmentation to reduce overfitting) ─────────────────
train_transform = transforms.Compose([
    transforms.Resize((IMG_SIZE, IMG_SIZE)),
    transforms.RandomHorizontalFlip(),
    transforms.RandomVerticalFlip(),
    transforms.RandomRotation(15),
    transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.1, hue=0.05),
    transforms.GaussianBlur(kernel_size=3, sigma=(0.1, 1.0)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225]),
])

val_transform = transforms.Compose([
    transforms.Resize((IMG_SIZE, IMG_SIZE)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225]),
])


# ─── Model ────────────────────────────────────────────────────────────────────
def build_model(num_classes=4):
    model = models.resnet50(weights=models.ResNet50_Weights.IMAGENET1K_V1)

    # Freeze all layers first
    for param in model.parameters():
        param.requires_grad = False

    # Unfreeze layer3 and layer4
    for param in model.layer3.parameters():
        param.requires_grad = True
    for param in model.layer4.parameters():
        param.requires_grad = True

    # Replace classifier head (with BatchNorm for better regularization)
    in_features = model.fc.in_features
    model.fc = nn.Sequential(
        nn.Dropout(0.5),
        nn.Linear(in_features, 512),
        nn.BatchNorm1d(512),
        nn.ReLU(),
        nn.Dropout(0.3),
        nn.Linear(512, num_classes),
    )
    return model


# ─── Plotting helpers ─────────────────────────────────────────────────────────
def save_learning_curves(history):
    """Save train/val accuracy and loss curves to learning_curves.png."""
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        epochs = range(1, len(history["train_acc"]) + 1)

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))

        ax1.plot(epochs, history["train_acc"], "b-o", label="Train Accuracy")
        ax1.plot(epochs, history["val_acc"],   "r-o", label="Val Accuracy")
        ax1.set_title("Accuracy over Epochs")
        ax1.set_xlabel("Epoch")
        ax1.set_ylabel("Accuracy")
        ax1.legend()
        ax1.grid(True)

        ax2.plot(epochs, history["train_loss"], "b-o", label="Train Loss")
        ax2.plot(epochs, history["val_loss"],   "r-o", label="Val Loss")
        ax2.set_title("Loss over Epochs")
        ax2.set_xlabel("Epoch")
        ax2.set_ylabel("Loss")
        ax2.legend()
        ax2.grid(True)

        # Overfitting annotation
        final_gap = abs(history["train_acc"][-1] - history["val_acc"][-1])
        if final_gap > 0.02:
            fig.suptitle(
                f"Warning: Possible Overfitting (train/val gap = {final_gap*100:.1f}%)",
                color="red", fontsize=12
            )
        else:
            fig.suptitle(
                f"Good fit (train/val gap = {final_gap*100:.1f}%)",
                color="green", fontsize=12
            )

        plt.tight_layout()
        plt.savefig("learning_curves.png", dpi=120, bbox_inches="tight")
        plt.close()
        print("Saved learning_curves.png")
    except ImportError:
        print("matplotlib not installed — skipping learning curve plot.")


def save_confusion_matrix(model, loader, device):
    """Run inference on val set and save confusion_matrix.png + classification report."""
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        from sklearn.metrics import confusion_matrix, classification_report

        all_preds, all_labels = [], []
        model.eval()
        with torch.no_grad():
            for imgs, labels in loader:
                imgs = imgs.to(device)
                preds = model(imgs).argmax(dim=1).cpu().tolist()
                all_preds.extend(preds)
                all_labels.extend(labels.tolist())

        cm = confusion_matrix(all_labels, all_preds)
        report = classification_report(all_labels, all_preds, target_names=CLASS_NAMES)

        print("\nClassification Report:\n", report)

        fig, ax = plt.subplots(figsize=(6, 5))
        im = ax.imshow(cm, interpolation="nearest", cmap="Blues")
        ax.figure.colorbar(im, ax=ax)
        ax.set(
            xticks=range(4), yticks=range(4),
            xticklabels=CLASS_NAMES, yticklabels=CLASS_NAMES,
            title="Confusion Matrix",
            ylabel="True Label",
            xlabel="Predicted Label",
        )
        plt.setp(ax.get_xticklabels(), rotation=30, ha="right")
        thresh = cm.max() / 2.0
        for i in range(4):
            for j in range(4):
                ax.text(j, i, cm[i, j],
                        ha="center", va="center",
                        color="white" if cm[i, j] > thresh else "black")

        plt.tight_layout()
        plt.savefig("confusion_matrix.png", dpi=120, bbox_inches="tight")
        plt.close()
        print("Saved confusion_matrix.png")
    except ImportError:
        print("matplotlib/sklearn not installed — skipping confusion matrix.")


# ─── Training Loop ────────────────────────────────────────────────────────────
def train(train_dir, test_dir):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")

    train_ds = BrainTumorDataset(train_dir, transform=train_transform)
    test_ds  = BrainTumorDataset(test_dir,  transform=val_transform)

    print(f"Train samples: {len(train_ds)} | Test samples: {len(test_ds)}")

    train_loader = DataLoader(train_ds, batch_size=BATCH_SIZE, shuffle=True,
                              num_workers=4, pin_memory=True)
    test_loader  = DataLoader(test_ds,  batch_size=BATCH_SIZE, shuffle=False,
                              num_workers=4, pin_memory=True)

    model = build_model().to(device)

    # Label smoothing reduces overconfidence and overfitting
    criterion = nn.CrossEntropyLoss(label_smoothing=0.1)

    # Weight decay = L2 regularization on all trainable parameters
    optimizer = optim.Adam(
        filter(lambda p: p.requires_grad, model.parameters()),
        lr=LR,
        weight_decay=WEIGHT_DECAY,
    )

    # Reduce LR when val loss plateaus
    scheduler = optim.lr_scheduler.ReduceLROnPlateau(
        optimizer, mode="min", factor=0.5, patience=2, verbose=True
    )

    best_val_acc = 0.0
    best_weights = None
    epochs_no_improve = 0

    history = {"train_loss": [], "train_acc": [], "val_loss": [], "val_acc": []}

    with open(LOG_PATH, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["epoch", "train_loss", "train_acc", "val_loss", "val_acc", "lr"])

        for epoch in range(1, EPOCHS + 1):
            current_lr = optimizer.param_groups[0]["lr"]

            # Train
            model.train()
            train_loss, train_correct, train_total = 0.0, 0, 0
            for imgs, labels in train_loader:
                imgs, labels = imgs.to(device), labels.to(device)
                optimizer.zero_grad()
                outputs = model(imgs)
                loss = criterion(outputs, labels)
                loss.backward()
                optimizer.step()
                train_loss += loss.item() * imgs.size(0)
                train_correct += (outputs.argmax(1) == labels).sum().item()
                train_total += imgs.size(0)

            train_loss /= train_total
            train_acc   = train_correct / train_total

            # Validate
            model.eval()
            val_loss, val_correct, val_total = 0.0, 0, 0
            with torch.no_grad():
                for imgs, labels in test_loader:
                    imgs, labels = imgs.to(device), labels.to(device)
                    outputs = model(imgs)
                    loss = criterion(outputs, labels)
                    val_loss += loss.item() * imgs.size(0)
                    val_correct += (outputs.argmax(1) == labels).sum().item()
                    val_total += imgs.size(0)

            val_loss /= val_total
            val_acc   = val_correct / val_total

            # LR scheduling based on val loss
            scheduler.step(val_loss)

            gap = abs(train_acc - val_acc)
            print(
                f"Epoch {epoch}/{EPOCHS}  "
                f"train_loss={train_loss:.4f}  train_acc={train_acc:.4f}  "
                f"val_loss={val_loss:.4f}  val_acc={val_acc:.4f}  "
                f"gap={gap*100:.2f}%  lr={current_lr:.2e}"
            )

            history["train_loss"].append(train_loss)
            history["train_acc"].append(train_acc)
            history["val_loss"].append(val_loss)
            history["val_acc"].append(val_acc)

            writer.writerow([epoch, f"{train_loss:.4f}", f"{train_acc:.4f}",
                             f"{val_loss:.4f}", f"{val_acc:.4f}", f"{current_lr:.2e}"])
            f.flush()

            # Checkpoint
            if val_acc > best_val_acc:
                best_val_acc = val_acc
                best_weights = copy.deepcopy(model.state_dict())
                torch.save(best_weights, MODEL_SAVE_PATH)
                print(f"  --> Saved best model (val_acc={best_val_acc:.4f})")
                epochs_no_improve = 0
            else:
                epochs_no_improve += 1
                print(f"  --> No improvement ({epochs_no_improve}/{PATIENCE})")
                if epochs_no_improve >= PATIENCE:
                    print("Early stopping triggered.")
                    break

    print(f"\nTraining complete. Best val_acc: {best_val_acc:.4f}")
    print(f"Model saved to: {MODEL_SAVE_PATH}")
    print(f"Log saved to:   {LOG_PATH}")

    # Overfitting summary
    final_train = history["train_acc"][-1]
    final_val   = history["val_acc"][-1]
    gap = abs(final_train - final_val)
    print(f"\nOverfitting check — train/val accuracy gap: {gap*100:.2f}%")
    if gap < 0.005:
        print("  No overfitting detected.")
    elif gap < 0.02:
        print("  Mild overfitting — model generalizes well.")
    elif gap < 0.05:
        print("  Moderate overfitting — consider more augmentation or weight decay.")
    else:
        print("  Severe overfitting — increase regularization significantly.")

    # Restore best weights for evaluation/plotting
    model.load_state_dict(best_weights)

    save_learning_curves(history)
    save_confusion_matrix(model, test_loader, device)


# ─── Entry Point ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Brain Tumor Detection — Training")
    parser.add_argument("--train_dir", type=str, default="dataset/Training",
                        help="Path to Training directory")
    parser.add_argument("--test_dir",  type=str, default="dataset/Testing",
                        help="Path to Testing directory")
    args = parser.parse_args()

    if not os.path.isdir(args.train_dir):
        raise FileNotFoundError(f"Training directory not found: {args.train_dir}")
    if not os.path.isdir(args.test_dir):
        raise FileNotFoundError(f"Testing directory not found: {args.test_dir}")

    train(args.train_dir, args.test_dir)
