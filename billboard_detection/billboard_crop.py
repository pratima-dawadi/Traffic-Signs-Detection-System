import os
from PIL import Image
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Users\Dell\AppData\Local\Tesseract-OCR\tesseract.exe'

def crop_image(image_path, cropped_img_dir,coordinates):
    try:
        os.makedirs(cropped_img_dir, exist_ok=True)
        img=Image.open(image_path)

        x1, y1, x2, y2 = coordinates

        width, height = img.size
        x1 = max(0, x1)
        y1 = max(0, y1)
        x2 = min(width, x2)
        y2 = min(height, y2)

        cropped_img = img.crop((x1, y1, x2, y2))

        filename = os.path.basename(image_path)
        base_name, ext = os.path.splitext(filename)
        output_filename = f"{base_name}_cropped_{x1}_{y1}{ext}" 
        output_path = os.path.join(cropped_img_dir, output_filename)
        
        cropped_img.save(output_path)
        return(output_path)

    except Exception as e:
        print(f"Error in cropping image: {e}")


if __name__ == "__main__":
    image_dir = '../collection_dataset/crop_image/images'
    cropped_img_dir = '../collection_dataset/crop_image/cropped_images'
    crop_image(image_dir, cropped_img_dir)
    print("Images cropped successfully")


