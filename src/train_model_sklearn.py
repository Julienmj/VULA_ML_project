import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import cv2
import pickle
from pathlib import Path

CSV_PATH = r'c:\Users\Administrator\Desktop\AIC\data\processed\dataset_metadata.csv'
MODEL_DIR = Path(r'c:\Users\Administrator\Desktop\AIC\models')
MODEL_PATH = MODEL_DIR / 'crop_disease_model.pkl'
LABEL_PATH = MODEL_DIR / 'label_encoder.pkl'

print("Loading data...")
df = pd.read_csv(CSV_PATH)
df = df[df['is_valid'] == True].sample(min(20000, len(df)), random_state=42)
print(f"Using {len(df)} images")

print("Loading and processing images...")
def load_image(path):
    img = cv2.imread(path)
    if img is None:
        return None
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (64, 64))
    return img.flatten() / 255.0

X = []
y_labels = []
for idx, row in df.iterrows():
    img = load_image(row['image_path'])
    if img is not None:
        X.append(img)
        y_labels.append(row['class_label'])
    if len(X) % 500 == 0:
        print(f"Loaded {len(X)} images...")

X = np.array(X)
y, labels = pd.factorize(y_labels)

print(f"\nTotal valid images: {len(X)}")
print(f"Number of classes: {len(labels)}")
print(f"Feature dimensions: {X.shape}")

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print(f"\nTrain: {len(X_train)}, Test: {len(X_test)}")

print("\nTraining Random Forest model...")
model = RandomForestClassifier(n_estimators=200, max_depth=30, random_state=42, n_jobs=-1, verbose=1)
model.fit(X_train, y_train)

print("\nEvaluating model...")
y_pred = model.predict(X_test)
acc = accuracy_score(y_test, y_pred)
print(f"\nTest Accuracy: {acc:.2%}")

print("\nSaving model...")
MODEL_DIR.mkdir(exist_ok=True)
with open(MODEL_PATH, 'wb') as f:
    pickle.dump(model, f)
with open(LABEL_PATH, 'wb') as f:
    pickle.dump(labels, f)

print(f"\nModel saved to: {MODEL_PATH}")
print(f"Labels saved to: {LABEL_PATH}")
print("Done!")
