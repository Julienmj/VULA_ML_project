import os
import pandas as pd
from pathlib import Path
import cv2

DATASET_PATH = r'c:\pac\AGRICULTURE---Crop-Disease-Detection-System-AIC\PlantVillagedataset\PlantVillage'
OUTPUT_DIR = Path(r'c:\pac\AGRICULTURE---Crop-Disease-Detection-System-AIC\data\processed')
OUTPUT_CSV = OUTPUT_DIR / 'dataset_metadata.csv'

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

print("Creating dataset metadata...")
data = []
for class_folder in os.listdir(DATASET_PATH):
    class_path = os.path.join(DATASET_PATH, class_folder)
    if not os.path.isdir(class_path):
        continue
    
    parts = class_folder.split('___')
    crop = parts[0] if len(parts) > 0 else "Unknown"
    disease = parts[1] if len(parts) > 1 else "healthy"
    is_healthy = 'healthy' in disease.lower()
    
    for img_file in os.listdir(class_path):
        if img_file.lower().endswith(('.jpg', '.jpeg', '.png')):
            img_path = os.path.join(class_path, img_file)
            
            try:
                img = cv2.imread(img_path)
                height, width = img.shape[:2] if img is not None else (0, 0)
                file_size = os.path.getsize(img_path) / 1024
            except:
                height, width, file_size = 0, 0, 0
            
            data.append({
                'image_path': img_path,
                'class_label': class_folder,
                'crop': crop,
                'disease': disease,
                'is_healthy': is_healthy,
                'is_valid': True,
                'width': width,
                'height': height,
                'file_size_kb': file_size 
            })

df = pd.DataFrame(data)
df.to_csv(OUTPUT_CSV, index=False)
print(f"Created {OUTPUT_CSV} with {len(df)} images")
print(f"Classes: {df['class_label'].nunique()}")
print(f"Crops: {df['crop'].nunique()}")
print(f"Diseases: {df['disease'].nunique()}")
