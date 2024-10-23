import cv2
import os
from PIL import Image

def blur_image(image_dir, output_dir):
    try:
        os.makedirs(output_dir, exist_ok=True)

        for filename in os.listdir(image_dir):
            if filename.endswith(('.jpg')):

                image_path = os.path.join(image_dir, filename)
                output_path = os.path.join(output_dir, filename)

                img=Image.open(image_path)
                image_width, image_height = img.size

                image = cv2.imread(image_path)

                labels_path=image_path.replace('images', 'labels').replace('.jpg', '.txt')

                blur_x,blur_y,blur_width,blur_height = get_coordinates(labels_path,image_width,image_height)
                print(f"blur_x: {blur_x}, blur_y: {blur_y}, blur_width: {blur_width}, blur_height: {blur_height}")

                # roi = image[blur_y:blur_y+blur_height, blur_x:blur_x+blur_width]
                # blur_image = cv2.GaussianBlur(roi,(101,101),0)
                
                # image[blur_y:blur_y+blur_height, blur_x:blur_x+blur_width] = blur_image

                # # start_point = (blur_x, blur_y)
                # # end_point = (blur_x+blur_width, blur_y+blur_height)

                # # blur_image=cv2.rectangle(image,start_point, end_point, (0, 0, 0), -1)
                
                region_to_blur = image[blur_y:blur_y+blur_height, blur_x:blur_x+blur_width].copy()
                
                blurred_region = cv2.GaussianBlur(region_to_blur, (101, 101), 0)
                
                image[blur_y:blur_y+blur_height, blur_x:blur_x+blur_width] = blurred_region
                
                cv2.imwrite(output_path, image)

    except Exception as e:
        print(f"Error in blurring image: {e}")

def get_coordinates(labels_path, img_width, img_height):
    with open(labels_path, 'r') as file:
        for line in file:
            class_id, x_center, y_center, width, height = line.split()
            print(f"splitted line: {class_id}, {x_center}, {y_center}, {width}, {height}")
            if class_id=='0':
                print(f"got the coordinates as x: {x_center}, y: {y_center}, width: {width}, height: {height}")
                x=(float(x_center) - float(width) / 2) * img_width
                y=(float(y_center) - float(height) / 2) * img_height
                width=float(width) * img_width
                height=float(height) * img_height
                print(f"got the coordinates after normalization as x: {x}, y: {y}, width: {width}, height: {height}")
                return int(x), int(y), int(width), int(height)
    print("No coordinates found")
    return 0, 0, 0, 0

if __name__ == "__main__":
    image_dir = '../collection_dataset/crop_image/images'
    output_dir = '../collection_dataset/crop_image/blurred_image'
    blur_image(image_dir, output_dir)
    print("Image blurred successfully")