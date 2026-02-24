import pandas as pd
import numpy as np
import cv2
import pickle
from pathlib import Path
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from sklearn.model_selection import train_test_split
from tqdm import tqdm
import random

CSV_PATH = Path(__file__).parent.parent / 'data' / 'processed' / 'dataset_metadata.csv'
MODEL_DIR = Path(__file__).parent.parent / 'models'
SPLITS_DIR = Path(__file__).parent.parent / 'data' / 'splits'
MODEL_PATH = MODEL_DIR / 'crop_disease_cnn.pth'
LABEL_PATH = MODEL_DIR / 'label_encoder.pkl'

class CropDiseaseCNN(nn.Module):
    def __init__(self, num_classes):
        super(CropDiseaseCNN, self).__init__()
        self.features = nn.Sequential(
            nn.Conv2d(3, 32, 3, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),
            
            nn.Conv2d(32, 64, 3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),
            
            nn.Conv2d(64, 128, 3, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),
            
            nn.Conv2d(128, 256, 3, padding=1),
            nn.BatchNorm2d(256),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),
        )
        
        self.classifier = nn.Sequential(
            nn.Dropout(0.5),
            nn.Linear(256 * 8 * 8, 512),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(512, num_classes)
        )
        
    def forward(self, x):
        x = self.features(x)
        x = x.view(x.size(0), -1)
        x = self.classifier(x)
        return x

class CropDataset(Dataset):
    def __init__(self, image_paths, labels, augment=False):
        self.image_paths = image_paths
        self.labels = labels
        self.augment = augment
        
    def __len__(self):
        return len(self.image_paths)
    
    def augment_image(self, img):
        if random.random() > 0.5:
            img = cv2.flip(img, 1)
        
        if random.random() > 0.5:
            angle = random.uniform(-15, 15)
            h, w = img.shape[:2]
            M = cv2.getRotationMatrix2D((w/2, h/2), angle, 1.0)
            img = cv2.warpAffine(img, M, (w, h))
        
        if random.random() > 0.5:
            brightness = random.uniform(0.8, 1.2)
            img = np.clip(img * brightness, 0, 255).astype(np.uint8)
        
        return img
    
    def __getitem__(self, idx):
        img = cv2.imread(self.image_paths[idx])
        if img is None:
            raise ValueError(f"Failed to load image: {self.image_paths[idx]}")
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (128, 128))
        
        if self.augment:
            img = self.augment_image(img)
        
        img = img.transpose(2, 0, 1)
        img = img / 255.0
        return torch.FloatTensor(img), self.labels[idx]

print("="*60)
print("CROP DISEASE DETECTION - CNN TRAINING")
print("="*60)

print("\nLoading dataset metadata...")
df = pd.read_csv(CSV_PATH)
print(f"Total images: {len(df):,}")

y_labels = df['class_label'].values
y, labels = pd.factorize(y_labels)
num_classes = len(labels)
print(f"Number of classes: {num_classes}")
print(f"\nClass distribution:")
for i, label in enumerate(labels):
    count = (y == i).sum()
    print(f"  {label}: {count:,} images")

X_train, X_test, y_train, y_test = train_test_split(
    df['image_path'].values, y, test_size=0.2, random_state=42, stratify=y
)
print(f"\nTrain: {len(X_train):,} | Test: {len(X_test):,}")

SPLITS_DIR.mkdir(exist_ok=True)
train_df = pd.DataFrame({'image_path': X_train, 'label': y_train})
test_df = pd.DataFrame({'image_path': X_test, 'label': y_test})
train_df.to_csv(SPLITS_DIR / 'train_split.csv', index=False)
test_df.to_csv(SPLITS_DIR / 'test_split.csv', index=False)
print(f"Saved train/test splits to {SPLITS_DIR}")

train_dataset = CropDataset(X_train, y_train, augment=True)
test_dataset = CropDataset(X_test, y_test, augment=False)
train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True, num_workers=0)
test_loader = DataLoader(test_dataset, batch_size=64, shuffle=False, num_workers=0)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"\nUsing device: {device}")

model = CropDiseaseCNN(num_classes).to(device)
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)
scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='max', factor=0.5, patience=3)

print(f"Model parameters: {sum(p.numel() for p in model.parameters()):,}")

print("\n" + "="*60)
print("TRAINING CNN MODEL")
print("="*60)

epochs = 25
best_acc = 0.0
train_losses = []
train_accs = []
test_accs = []

for epoch in range(epochs):
    model.train()
    running_loss = 0.0
    correct = 0
    total = 0
    
    pbar = tqdm(train_loader, desc=f"Epoch {epoch+1}/{epochs}")
    for images, labels_batch in pbar:
        images, labels_batch = images.to(device), labels_batch.to(device)
        
        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels_batch)
        loss.backward()
        optimizer.step()
        
        running_loss += loss.item()
        _, predicted = torch.max(outputs.data, 1)
        total += labels_batch.size(0)
        correct += (predicted == labels_batch).sum().item()
        
        pbar.set_postfix({'loss': f'{loss.item():.4f}', 'acc': f'{100*correct/total:.2f}%'})
    
    train_acc = 100 * correct / total
    avg_loss = running_loss / len(train_loader)
    train_losses.append(avg_loss)
    train_accs.append(train_acc)
    
    model.eval()
    correct = 0
    total = 0
    with torch.no_grad():
        for images, labels_batch in test_loader:
            images, labels_batch = images.to(device), labels_batch.to(device)
            outputs = model(images)
            _, predicted = torch.max(outputs.data, 1)
            total += labels_batch.size(0)
            correct += (predicted == labels_batch).sum().item()
    
    test_acc = 100 * correct / total
    test_accs.append(test_acc)
    
    scheduler.step(test_acc)
    
    print(f"Epoch {epoch+1}: Loss: {avg_loss:.4f} | Train Acc: {train_acc:.2f}% | Test Acc: {test_acc:.2f}%")
    
    if test_acc > best_acc:
        best_acc = test_acc
        MODEL_DIR.mkdir(exist_ok=True)
        torch.save(model.state_dict(), MODEL_PATH)
        print(f"Model saved (Best Acc: {best_acc:.2f}%)")

with open(LABEL_PATH, 'wb') as f:
    pickle.dump(labels, f)

history_df = pd.DataFrame({
    'epoch': range(1, epochs+1),
    'train_loss': train_losses,
    'train_acc': train_accs,
    'test_acc': test_accs
})
history_df.to_csv(SPLITS_DIR / 'training_history.csv', index=False)

print("\n" + "="*60)
print(f"TRAINING COMPLETE")
print(f"Best Test Accuracy: {best_acc:.2f}%")
print(f"Model saved: {MODEL_PATH}")
print(f"Labels saved: {LABEL_PATH}")
print(f"Training history: {SPLITS_DIR / 'training_history.csv'}")
print("="*60)
