"""
Brain Tumor Detection — PyTorch Training Script
ResNet50 fine-tuned on Brain Tumor MRI Dataset (4 classes)
Classes: pituitary=0, notumor=1, meningioma=2, glioma=3
"""

import os
import glob
import argparse
import csv
import copy

import cv2
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from torchvision import models, transforms
from PIL import Image

# ─── Config ───────────────────────────────────────────────────────────────────
CLASSES = {"pituitary": 0, "notumor": 1, "meningioma": 2, "glioma": 3}
IMG_SIZE = 224
BATCH_SIZE = 32
EPOCHS = 7
LR = 1e-4
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


# ─── Transforms ───────────────────────────────────────────────────────────────
train_transform = transforms.Compose([
    transforms.Resize((IMG_SIZE, IMG_SIZE)),
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(10),
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

    # Unfreeze layer3 and layer4 (mirrors unfreezing after layer 80 in TF ResNet50)
    for param in model.layer3.parameters():
        param.requires_grad = True
    for param in model.layer4.parameters():
        param.requires_grad = True

    # Replace classifier head
    in_features = model.fc.in_features
    model.fc = nn.Sequential(
        nn.Dropout(0.5),
        nn.Linear(in_features, 512),
        nn.ReLU(),
        nn.Dropout(0.3),
        nn.Dropout(0.3),
        nn.Linear(512, num_classes),
    )
    return model


# ─── Training Loop ────────────────────────────────────────────────────────────
def train(train_dir, test_dir):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")

    train_ds = BrainTumorDataset(train_dir, transform=train_transform)
    test_ds  = BrainTumorDataset(test_dir,  transform=val_transform)

    print(f"Train samples: {len(train_ds)} | Test samples: {len(test_ds)}")

    train_loader = DataLoader(train_ds, batch_size=BATCH_SIZE, shuffle=True,  num_workers=4, pin_memory=True)
    test_loader  = DataLoader(test_ds,  batch_size=BATCH_SIZE, shuffle=False, num_workers=4, pin_memory=True)

    model = build_model().to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(filter(lambda p: p.requires_grad, model.parameters()), lr=LR)

    best_val_acc = 0.0
    best_weights = None
    epochs_no_improve = 0

    with open(LOG_PATH, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["epoch", "train_loss", "train_acc", "val_loss", "val_acc"])

        for epoch in range(1, EPOCHS + 1):
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

            print(f"Epoch {epoch}/{EPOCHS}  "
                  f"train_loss={train_loss:.4f}  train_acc={train_acc:.4f}  "
                  f"val_loss={val_loss:.4f}  val_acc={val_acc:.4f}")

            writer.writerow([epoch, f"{train_loss:.4f}", f"{train_acc:.4f}",
                             f"{val_loss:.4f}", f"{val_acc:.4f}"])
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
