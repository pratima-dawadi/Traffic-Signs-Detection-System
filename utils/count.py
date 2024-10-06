import os

label_dir = './total_dataset/labels'

class_count = {}

for label_file in os.listdir(label_dir):
    label_path = os.path.join(label_dir, label_file)
    
    with open(label_path, 'r') as file:
        for line in file:
            class_id = int(line.split()[0])
            
            if class_id in class_count:
                class_count[class_id] += 1
            else:
                class_count[class_id] = 1

for class_id, count in class_count.items():
    print(f'Class {class_id}: {count} images')
