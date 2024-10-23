import os
from PIL import Image
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Users\Dell\AppData\Local\Tesseract-OCR\tesseract.exe'

def crop_image(image_dir, cropped_img_dir):
    try:
        os.makedirs(cropped_img_dir, exist_ok=True)
      
        for filename in os.listdir(image_dir):
            if filename.endswith(('.jpg')):
                image_path=os.path.join(image_dir, filename)
                img=Image.open(image_path)
                print(f"image_path: {image_path}")

                labels_path=image_path.replace('images', 'labels').replace('.jpg', '.txt')

                print(f"labels_path: {labels_path}")

                image_width, image_height = img.size

                x, y, width, height=get_coordinates(labels_path, image_width, image_height)
                cropped_img=img.crop((x, y, x + width, y + height))

                output_path=os.path.join(cropped_img_dir, filename)
                extract_text(output_path)
                cropped_img.save(output_path)
    except Exception as e:
        print(f"Error in cropping image: {e}")

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
    return 0, 0, 0, 0\
    

def extract_text(image_path):
    try:
        img=Image.open(image_path)
        text=pytesseract.image_to_string(img)
        print(f"Extracted text: {text}")

    except Exception as e:
        print(f"Error in extracting text: {e}")
        return None

if __name__ == "__main__":
    image_dir = '../collection_dataset/crop_image/images'
    cropped_img_dir = '../collection_dataset/crop_image/cropped_images'
    crop_image(image_dir, cropped_img_dir)
    print("Images cropped successfully")


