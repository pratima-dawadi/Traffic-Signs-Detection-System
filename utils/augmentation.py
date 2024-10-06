import os
import cv2
import numpy as np
import albumentations as A

image_dir = './total_dataset/images'
label_dir = './total_dataset/labels'
dest_image_dir = './augmented/images'
dest_label_dir = './augmented/labels'

os.makedirs(dest_image_dir, exist_ok=True)
os.makedirs(dest_label_dir, exist_ok=True)

def read_labels(label_path):
    boxes = []
    with open(label_path, 'r') as file:
        for line in file:
            parts = line.strip().split()
            class_id = int(parts[0])
            x_center, y_center, width, height = map(float, parts[1:5])
            boxes.append((class_id, x_center, y_center, width, height))
    return boxes

def write_labels(label_path, boxes):
    with open(label_path, 'w') as file:
        for box in boxes:
            file.write(f"{box[0]} {box[1]} {box[2]} {box[3]} {box[4]}\n")

# Aumentation Functions

def augment_brightness_contrast(image, bboxes):
    return A.RandomBrightnessContrast(p=1)(image=image, bboxes=bboxes)

def augment_saturation(image, bboxes):
    return A.HueSaturationValue(p=1)(image=image, bboxes=bboxes)

# def augment_blur(image, bboxes):
#     return A.Blur(blur_limit=3, p=1)(image=image, bboxes=bboxes)

# Target class ID for augmentation
target_class_id = 6

for label_file in os.listdir(label_dir):
    if label_file.endswith('.txt'):
        label_path = os.path.join(label_dir, label_file)
        image_file = label_file.replace('.txt', '.jpg')
        image_path = os.path.join(image_dir, image_file)

        if os.path.exists(image_path):
            image = cv2.imread(image_path)
            boxes = read_labels(label_path)

            filtered_boxes = [box for box in boxes if box[0] == target_class_id]

            if filtered_boxes:
                bboxes = np.array([box[1:] for box in filtered_boxes])
                class_labels = [box[0] for box in filtered_boxes]

                augmentations = [
                    (augment_brightness_contrast, "brightness_contrast"),
                    (augment_saturation, "saturation"),
                    # (augment_blur, "blur")
                ]

                for i, (augment_func, name) in enumerate(augmentations, start=1):
                    augmented = augment_func(image, bboxes)
                    augmented_image = augmented['image']
                    augmented_bboxes = augmented['bboxes']

                    augmented_image_name = f"{image_file.replace('.jpg', '')}_aug{i}.jpg"
                    augmented_image_path = os.path.join(dest_image_dir, augmented_image_name)
                    cv2.imwrite(augmented_image_path, augmented_image)

                    augmented_boxes = [(class_labels[j], *augmented_bboxes[j]) for j in range(len(augmented_bboxes))]

                    augmented_label_path = os.path.join(dest_label_dir, label_file.replace('.txt', f'_aug{i}.txt'))
                    write_labels(augmented_label_path, augmented_boxes)

                    print(f"Augmented image and label saved for {augmented_image_name}.")
            else:
                print(f"No bounding boxes found for target class {target_class_id} in {label_file}.")
        else:
            print(f"Image {image_file} not found, skipping.")

print("Data augmentation completed.")
