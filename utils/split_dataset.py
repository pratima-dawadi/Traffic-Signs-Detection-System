import os
import random
import shutil

image_dir = 'split_dataset2'
label_dir = 'split_dataset2'
train_image_dir = 'split_dataset2/images/train'
val_image_dir = 'split_dataset2/images/val'
train_label_dir = 'split_dataset2/labels/train'
val_label_dir = 'split_dataset2/labels/val'

os.makedirs(train_image_dir, exist_ok=True)
os.makedirs(val_image_dir, exist_ok=True)
os.makedirs(train_label_dir, exist_ok=True)
os.makedirs(val_label_dir, exist_ok=True)

images = [f for f in os.listdir(image_dir) if f.endswith(('.jpg', '.png', '.jpeg'))]

random.shuffle(images)

split_ratio = 0.8
split_index = int(len(images) * split_ratio)

train_images = images[:split_index]
val_images = images[split_index:]

for img in train_images:
    shutil.move(os.path.join(image_dir, img), os.path.join(train_image_dir, img))
    
    label_file = img.replace('.jpg', '.txt').replace('.png', '.txt').replace('.jpeg', '.txt')
    if os.path.exists(os.path.join(label_dir, label_file)):
        shutil.move(os.path.join(label_dir, label_file), os.path.join(train_label_dir, label_file))

for img in val_images:
    shutil.move(os.path.join(image_dir, img), os.path.join(val_image_dir, img))
    
    label_file = img.replace('.jpg', '.txt').replace('.png', '.txt').replace('.jpeg', '.txt')
    if os.path.exists(os.path.join(label_dir, label_file)):
        shutil.move(os.path.join(label_dir, label_file), os.path.join(val_label_dir, label_file))

print(f"Training images: {len(train_images)}")
print(f"Validation images: {len(val_images)}")
