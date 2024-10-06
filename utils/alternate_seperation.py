import os
import shutil

image_dir = './parking/images'
label_dir = './parking/labels'
dest_image_dir = './total_dataset/images'
dest_label_dir = './total_dataset/labels'

os.makedirs(dest_image_dir, exist_ok=True)
os.makedirs(dest_label_dir, exist_ok=True)

target_class_id = 0

images_found_count=0
for label_file in os.listdir(label_dir):
    if label_file.endswith('.txt'):
        label_path = os.path.join(label_dir, label_file)

        try:
            with open(label_path, 'r') as file:
                found_target_class = False
                for line in file:
                    class_id = int(line.split()[0])

                    if class_id == target_class_id:
                        found_target_class = True
                        images_found_count+=1
                        image_file = label_file.replace('.txt', '.jpg')
                        image_path = os.path.join(image_dir, image_file)
                        break

            if found_target_class and images_found_count %2 == 0:
                if os.path.exists(image_path):
                    shutil.move(image_path, os.path.join(dest_image_dir, image_file))
                    shutil.move(label_path, os.path.join(dest_label_dir, label_file))
                    print(f"Moved {image_file} and {label_file}.")
                else:
                    print(f"Image file {image_file} not found, skipping.")


            if not found_target_class:
                print(f"No target class {target_class_id} found in {label_file}.")

        except Exception as e:
            print(f"Error processing {label_file}: {e}")

print("Images and labels have been moved.")