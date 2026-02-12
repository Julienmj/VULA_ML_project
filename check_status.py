import os
from pathlib import Path

print("=" * 50)
print("PROJECT STATUS CHECK")
print("=" * 50)

base = Path(r'c:\Users\Administrator\Desktop\AIC')

# Check data
csv_path = base / 'data' / 'processed' / 'dataset_metadata.csv'
print(f"\n[OK] Data cleaned: {csv_path.exists()}")

# Check notebooks
eda_nb = base / 'notebooks' / '02_eda.ipynb'
model_nb = base / 'notebooks' / '03_model_training.ipynb'
print(f"[OK] EDA notebook: {eda_nb.exists()}")
print(f"[OK] Model training notebook: {model_nb.exists()}")

# Check model files
model_path = base / 'models' / 'crop_disease_model.pkl'
label_path = base / 'models' / 'label_encoder.pkl'
print(f"\n[{'OK' if model_path.exists() else 'PENDING'}] Model trained: {model_path.exists()}")
if not model_path.exists():
    print("   -> Run: python src\\train_model_sklearn.py")

# Check UI
ui_path = base / 'ui' / 'app.py'
print(f"\n[OK] UI created: {ui_path.exists()}")

print("\n" + "=" * 50)
print("NEXT STEPS:")
print("=" * 50)
if not model_path.exists():
    print("1. Train model: python src\\train_model_sklearn.py")
    print("2. Run UI: streamlit run ui\\app.py")
else:
    print("1. Run UI: streamlit run ui\\app.py")
    print("2. Upload an image and test predictions!")
print("=" * 50)
