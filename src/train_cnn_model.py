import pandas as pd
import numpy as np
import cv2
import pickle
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

CSV_PATH = r'c:\pac\AGRICULTURE---Crop-Disease-Detection-System-AIC\data\processed\dataset_metadata.csv'
MODEL_DIR = Path(r'c:\pac\AGRICULTURE---Crop-Disease-Detection-System-AIC\models')
MODEL_PATH = MODEL_DIR / 'crop_disease_cnn_model.h5'
LABEL_PATH = MODEL_DIR / 'label_encoder.pkl'

print("Loading data...")
df = pd.read_csv(CSV_PATH)
df = df[df['is_valid'] == True]
print(f"Using all {len(df)} images")

print("\nLoading images...")
def load_image(path):
    img = cv2.imread(path)
    if img is None:
        return None
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (128, 128))
    return img / 255.0

X = []
y_labels = []
for idx, row in df.iterrows():
    img = load_image(row['image_path'])
    if img is not None:
        X.append(img)
        y_labels.append(row['class_label'])
    if len(X) % 1000 == 0:
        print(f"Loaded {len(X)} images...")

X = np.array(X)
y, labels = pd.factorize(y_labels)
y = keras.utils.to_categorical(y, len(labels))

print(f"\nTotal: {len(X)} images, {len(labels)} classes")

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print(f"Train: {len(X_train)}, Test: {len(X_test)}")

print("\nBuilding CNN model...")
model = keras.Sequential([
    layers.Conv2D(32, (3, 3), activation='relu', input_shape=(128, 128, 3)),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(128, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(128, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Flatten(),
    layers.Dropout(0.5),
    layers.Dense(512, activation='relu'),
    layers.Dropout(0.3),
    layers.Dense(len(labels), activation='softmax')
])

model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

print("\nTraining CNN model...")
history = model.fit(X_train, y_train, 
                    epochs=20, 
                    batch_size=32,
                    validation_split=0.2,
                    verbose=1)

print("\nEvaluating model...")
y_pred = model.predict(X_test)
y_pred_classes = np.argmax(y_pred, axis=1)
y_test_classes = np.argmax(y_test, axis=1)

acc = accuracy_score(y_test_classes, y_pred_classes)
print(f"\nTest Accuracy: {acc:.2%}")

print("\nSaving model...")
MODEL_DIR.mkdir(exist_ok=True)
model.save(MODEL_PATH)
with open(LABEL_PATH, 'wb') as f:
    pickle.dump(labels, f)

print(f"\nCNN Model saved to: {MODEL_PATH}")
print(f"Labels saved to: {LABEL_PATH}")
print("Done!")
