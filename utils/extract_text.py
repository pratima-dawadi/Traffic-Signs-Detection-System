import pytesseract
from PIL import Image
import cv2
import numpy as np

pytesseract.pytesseract.tesseract_cmd = r'C:\Users\Dell\AppData\Local\Tesseract-OCR\tesseract.exe'

def extract_text(image_path):
    try:
        # img=Image.open(image_path)
        # text=pytesseract.image_to_string(img)
        # print(f"Extracted text: {text}")
        image = cv2.imread(image_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        sharpen_kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
        sharpen = cv2.filter2D(gray, -1, sharpen_kernel)
        thresh = cv2.threshold(sharpen, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

        data = pytesseract.image_to_string(thresh, lang='eng', config='--psm 6')
        print(data)

        cv2.imshow('sharpen', sharpen)
        cv2.imshow('thresh', thresh)
        cv2.waitKey()

    except Exception as e:
        print(f"Error in extracting text: {e}")
        return None
    

if __name__ == "__main__":
    image_path = '../collection_dataset/crop_image/unnamed.png'
    extract_text(image_path)