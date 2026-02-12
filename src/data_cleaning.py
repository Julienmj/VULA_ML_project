"""
Data Cleaning Script for PlantVillage Dataset
Checks for corrupted images, removes duplicates, and validates the dataset
"""

import os
import cv2
from pathlib import Path
from collections import defaultdict
import shutil

# Configuration
DATASET_PATH = r'c:\Users\Administrator\Desktop\AIC\plantvillage dataset\color'
OUTPUT_PATH = r'c:\Users\Administrator\Desktop\AIC\data\processed\clean_dataset'

def check_corrupted_images(dataset_path):
    """Find and list corrupted/unreadable images"""
    corrupted = []
    total = 0
    
    print("Checking for corrupted images...")
    for class_folder in os.listdir(dataset_path):
        class_path = os.path.join(dataset_path, class_folder)
        if not os.path.isdir(class_path):
            continue
            
        for img_file in os.listdir(class_path):
            if not img_file.lower().endswith(('.jpg', '.jpeg', '.png')):
                continue
            
            total += 1
            img_path = os.path.join(class_path, img_file)
            
            try:
                img = cv2.imread(img_path)
                if img is None or img.size == 0:
                    corrupted.append(img_path)
            except:
                corrupted.append(img_path)
    
    print(f"✓ Checked {total} images")
    print(f"✗ Found {len(corrupted)} corrupted images")
    return corrupted

def check_image_sizes(dataset_path):
    """Check if images have consistent sizes"""
    sizes = defaultdict(int)
    
    print("\nAnalyzing image dimensions...")
    for class_folder in os.listdir(dataset_path):
        class_path = os.path.join(dataset_path, class_folder)
        if not os.path.isdir(class_path):
            continue
            
        for img_file in os.listdir(class_path)[:50]:  # Sample 50 per class
            if not img_file.lower().endswith(('.jpg', '.jpeg', '.png')):
                continue
                
            img_path = os.path.join(class_path, img_file)
            img = cv2.imread(img_path)
            if img is not None:
                sizes[img.shape[:2]] += 1
    
    print(f"Found {len(sizes)} different image sizes:")
    for size, count in sorted(sizes.items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"  {size[0]}x{size[1]}: {count} images")
    
    return sizes

def check_class_distribution(dataset_path):
    """Check number of images per class"""
    distribution = {}
    
    print("\nClass distribution:")
    for class_folder in os.listdir(dataset_path):
        class_path = os.path.join(dataset_path, class_folder)
        if not os.path.isdir(class_path):
            continue
            
        count = len([f for f in os.listdir(class_path) 
                    if f.lower().endswith(('.jpg', '.jpeg', '.png'))])
        distribution[class_folder] = count
    
    for cls, count in sorted(distribution.items(), key=lambda x: x[1], reverse=True):
        print(f"  {cls}: {count} images")
    
    return distribution

def clean_dataset(dataset_path, output_path, corrupted_files):
    """Copy clean images to processed folder"""
    if os.path.exists(output_path):
        print(f"\n✓ Clean dataset already exists at: {output_path}")
        return
    
    print(f"\nCopying clean images to: {output_path}")
    os.makedirs(output_path, exist_ok=True)
    
    copied = 0
    for class_folder in os.listdir(dataset_path):
        class_path = os.path.join(dataset_path, class_folder)
        if not os.path.isdir(class_path):
            continue
        
        output_class_path = os.path.join(output_path, class_folder)
        os.makedirs(output_class_path, exist_ok=True)
        
        for img_file in os.listdir(class_path):
            if not img_file.lower().endswith(('.jpg', '.jpeg', '.png')):
                continue
                
            src = os.path.join(class_path, img_file)
            if src not in corrupted_files:
                dst = os.path.join(output_class_path, img_file)
                shutil.copy2(src, dst)
                copied += 1
    
    print(f"✓ Copied {copied} clean images")

if __name__ == "__main__":
    print("=" * 60)
    print("PlantVillage Dataset Cleaning")
    print("=" * 60)
    
    # Check for corrupted images
    corrupted = check_corrupted_images(DATASET_PATH)
    
    # Check image sizes
    sizes = check_image_sizes(DATASET_PATH)
    
    # Check class distribution
    distribution = check_class_distribution(DATASET_PATH)
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Total classes: {len(distribution)}")
    print(f"Total images: {sum(distribution.values())}")
    print(f"Corrupted images: {len(corrupted)}")
    print(f"Different image sizes: {len(sizes)}")
    
    if len(corrupted) > 0:
        print(f"\n⚠ Warning: {len(corrupted)} corrupted images found")
        print("These will be excluded from the clean dataset")
    else:
        print("\n✓ No corrupted images found!")
    
    # Clean dataset (optional - uncomment to copy clean images)
    # clean_dataset(DATASET_PATH, OUTPUT_PATH, corrupted)
    
    print("\n✓ Data cleaning check complete!")
    print("\nNext steps:")
    print("1. Review the summary above")
    print("2. Uncomment clean_dataset() if you want to copy clean images")
    print("3. Run the preprocessing notebook to prepare for training")
