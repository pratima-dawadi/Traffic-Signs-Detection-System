import cv2
import os
from PIL import Image

def blur_image(image_path, blur_img_dir,lp_coordinates):
    try:
        os.makedirs(blur_img_dir, exist_ok=True)
        image = cv2.imread(image_path)

        x1,y1,x2,y2 = lp_coordinates
        region_to_blur = image[y1:y2, x1:x2].copy()

                
        blurred_region = cv2.GaussianBlur(region_to_blur, (101, 101), 0)

        image[y1:y2, x1:x2] = blurred_region
        output_path = os.path.join(blur_img_dir, os.path.basename(image_path))
                
        cv2.imwrite(output_path, image)

    except Exception as e:
        print(f"Error in blurring image: {e}")

