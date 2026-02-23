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

CSV_PATH = r'c:\pac\AGRICULTURE---Crop-Disease-Detection-System-AIC\data\processed\dataset_metadata.csv'
MODEL_DIR = Path(r'c:\pac\AGRICULTURE---Crop-Disease-Detection-System-AIC\models')
MODEL_PATH = MODEL_DIR / 'crop_disease_cnn.pth'
LABEL_PATH = MODEL_DIR / 'label_encoder_cnn.pkl'

# CNN Model
class CropDiseaseCNN(nn.Module):
    def __init__(self, num_classes):
        super(CropDiseaseCNN, self).__init__()
        self.conv1 = nn.Conv2d(3, 32, 3, padding=1)
        self.conv2 = nn.Conv2d(32, 64, 3, padding=1)
        self.conv3 = nn.Conv2d(64, 128, 3, padding=1)
        self.pool = nn.MaxPool2d(2, 2)
        self.fc1 = nn.Linear(128 * 8 * 8, 256)
        self.fc2 = nn.Linear(256, num_classes)
        self.dropout = nn.Dropout(0.5)
        self.relu = nn.ReLU()
        
    def forward(self, x):
        x = self.pool(self.relu(self.conv1(x)))
        x = self.pool(self.relu(self.conv2(x)))
        x = self.pool(self.relu(self.conv3(x)))
        x = x.view(-1, 128 * 8 * 8)
        x = self.dropout(self.relu(self.fc1(x)))
        x = self.fc2(x)
        return x

# Dataset
class CropDataset(Dataset):
    def __init__(self, image_paths, labels):
        self.image_paths = image_paths
        self.labels = labels
        
    def __len__(self):
        return len(self.image_paths)
    
    def __getitem__(self, idx):
        img = cv2.imread(self.image_paths[idx])
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (64, 64))
        img = img.transpose(2, 0, 1)  # HWC to CHW
        img = img / 255.0
        return torch.FloatTensor(img), self.labels[idx]

print("Loading data...")
df = pd.read_csv(CSV_PATH)
df = df[df['is_valid'] == True]
print(f"Using {len(df)} images")

# Prepare labels
y_labels = df['class_label'].values
y, labels = pd.factorize(y_labels)
num_classes = len(labels)
print(f"Classes: {num_classes}")

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    df['image_path'].values, y, test_size=0.2, random_state=42
)
print(f"Train: {len(X_train)}, Test: {len(X_test)}")

# Create datasets
train_dataset = CropDataset(X_train, y_train)
test_dataset = CropDataset(X_test, y_test)
train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=32, shuffle=False)

# Model
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"Using device: {device}")

model = CropDiseaseCNN(num_classes).to(device)
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Training
print("\nTraining CNN...")
epochs = 15
for epoch in range(epochs):
    model.train()
    running_loss = 0.0
    correct = 0
    total = 0
    
    for i, (images, labels_batch) in enumerate(train_loader):
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
        
        if (i + 1) % 100 == 0:
            print(f"Epoch [{epoch+1}/{epochs}], Step [{i+1}/{len(train_loader)}], "
                  f"Loss: {running_loss/100:.4f}, Acc: {100*correct/total:.2f}%")
            running_loss = 0.0

# Testing
print("\nEvaluating...")
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

accuracy = 100 * correct / total
print(f"\n{'='*50}")
print(f"CNN Test Accuracy: {accuracy:.2f}%")
print(f"{'='*50}")

# Save
print("\nSaving model...")
MODEL_DIR.mkdir(exist_ok=True)
torch.save(model.state_dict(), MODEL_PATH)
with open(LABEL_PATH, 'wb') as f:
    pickle.dump(labels, f)

print(f"\nModel saved to: {MODEL_PATH}")
print(f"Labels saved to: {LABEL_PATH}")
print("Done!")
