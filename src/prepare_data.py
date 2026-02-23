import os
import pandas as pd
from pathlib import Path
import cv2

DATASET_PATH = Path(__file__).parent.parent / 'data' / 'raw' / 'PlantVillage'
OUTPUT_DIR = Path(__file__).parent.parent / 'data' / 'processed'
OUTPUT_CSV = OUTPUT_DIR / 'dataset_metadata.csv'

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

print("Creating dataset metadata...")
data = []

for class_folder in os.listdir(DATASET_PATH):
    class_path = DATASET_PATH / class_folder
    if not class_path.is_dir():
        continue
    
    parts = class_folder.split('___')
    if len(parts) == 2:
        crop = parts[0]
        disease = parts[1]
    else:
        parts = class_folder.split('_')
        crop = parts[0]
        disease = '_'.join(parts[1:])
    
    is_healthy = 'healthy' in disease.lower()
    
    for img_file in os.listdir(class_path):
        if img_file.lower().endswith(('.jpg', '.jpeg', '.png')):
            img_path = class_path / img_file
            
            try:
                img = cv2.imread(str(img_path))
                height, width = img.shape[:2] if img is not None else (0, 0)
                file_size = img_path.stat().st_size / 1024
            except:
                height, width, file_size = 0, 0, 0
            
            data.append({
                'image_path': str(img_path),
                'class_label': class_folder,
                'crop': crop,
                'disease': disease,
                'is_healthy': is_healthy,
                'width': width,
                'height': height,
                'file_size_kb': file_size
            })

df = pd.DataFrame(data)
df.to_csv(OUTPUT_CSV, index=False)

print(f"\n{'='*60}")
print(f"Dataset metadata created: {OUTPUT_CSV}")
print(f"{'='*60}")
print(f"Total images: {len(df):,}")
print(f"Classes: {df['class_label'].nunique()}")
print(f"Crops: {df['crop'].nunique()}")
print(f"Diseases: {df['disease'].nunique()}")
print(f"Healthy samples: {df['is_healthy'].sum():,}")
print(f"Diseased samples: {(~df['is_healthy']).sum():,}")
print(f"{'='*60}")
