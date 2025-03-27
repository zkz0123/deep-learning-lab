import os
import shutil
import random
from glob import glob

# Path to the original dataset
raw_root = "C:/Users/zkz01/Desktop/cw/icubworld/part2_cropped"

# Output path for the reorganized dataset
output_root = "C:/Users/zkz01/Desktop/cw/dataset1"

# Overall total
total_images = 0

# Iterate over each class
for class_name in os.listdir(raw_root):
    class_path = os.path.join(raw_root, class_name)
    if not os.path.isdir(class_path):
        continue
    print(f"Processing class: {class_name}")
    
    # Create corresponding class directory in the output path
    output_class_dir = os.path.join(output_root, class_name)
    os.makedirs(output_class_dir, exist_ok=True)
    
    # Counter for this class
    class_total = 0

    # All object instances in this class
    instances = sorted([
        inst for inst in os.listdir(class_path)
        if os.path.isdir(os.path.join(class_path, inst))
    ])

    for instance in instances:
        instance_path = os.path.join(class_path, instance)

        # Only process the transformation folder named 'mix' (case-insensitive)
        transformations = [
            t for t in os.listdir(instance_path)
            if os.path.isdir(os.path.join(instance_path, t)) and t.lower() == 'mix'
        ]
        if not transformations:
            continue  # skip if 'mix' not found

        mix_trans = transformations[0]
        trans_path = os.path.join(instance_path, mix_trans)

        # Iterate over all recording days
        days = sorted([
            d for d in os.listdir(trans_path)
            if os.path.isdir(os.path.join(trans_path, d))
        ])

        for day in days:
            day_path = os.path.join(trans_path, day, "left")
            if not os.path.isdir(day_path):
                continue
            
            # Get all image files and randomly select
            image_files = glob(os.path.join(day_path, "*.jpg"))
            if not image_files:
                continue
            selected_images = random.sample(image_files, min(50, len(image_files)))

            for img_file in selected_images:
                basename = f"{instance}_{mix_trans}_{day}_{os.path.basename(img_file)}"
                dst_path = os.path.join(output_class_dir, basename)
                shutil.copy(img_file, dst_path)
                class_total += 1
                total_images += 1

    print(f"{class_total} images")

print(f"\nTotal images copied: {total_images}")
