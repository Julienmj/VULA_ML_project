import pickle
import pandas as pd
from pathlib import Path

CSV_PATH = Path(__file__).parent.parent / 'data' / 'processed' / 'dataset_metadata.csv'
LABEL_PATH = Path(__file__).parent.parent / 'models' / 'label_encoder.pkl'

df = pd.read_csv(CSV_PATH)
y_labels = df['class_label'].values
y, labels = pd.factorize(y_labels)

LABEL_PATH.parent.mkdir(exist_ok=True)
with open(LABEL_PATH, 'wb') as f:
    pickle.dump(labels, f)

print(f"✓ Label encoder created: {LABEL_PATH}")
print(f"✓ {len(labels)} classes saved")
