from billboard_detection.billboard_detection import run_inference,detect_license_plate
from billboard_detection.billboard_crop import crop_image
from billboard_detection.billboard_text_extraction import billboard_text,entity_recognition
from billboard_detection.license_plate_blur import blur_image
from model.georeference import get_geolocation
import os 

def billboard_base():
    try:
        image_folder = 'billboard_detection/images'
        cropped_img_dir = 'billboard_detection/cropped_images'
        blur_img_dir = 'billboard_detection/blur_images'

        for image_file in os.listdir(image_folder):
            if image_file.lower().endswith(('.jpg', '.jpeg', '.png')):
                image_path = os.path.join(image_folder, image_file)
                latitude,longitude=get_geolocation(image_path)
                detection_coordinates,inference_image_path=run_inference(image_path,latitude,longitude)
                lp_detection_coordinates=detect_license_plate(image_path)

                # getting the coordinates from the model detection and passing it for cropping the image
                if detection_coordinates:
                    for detection in detection_coordinates:
                        coordinates=detection['coordinates']
                        cropped_img_save_dir=crop_image(image_path, cropped_img_dir,coordinates)

                        # extracting text from billboard
                        extracted_text=billboard_text(cropped_img_save_dir)

                        # classifying the extracted text
                        entity_recognition(extracted_text)
                
                if lp_detection_coordinates:
                    for lp_detection in lp_detection_coordinates:
                        lp_coordinates=lp_detection['coordinates']
                        blur_image(inference_image_path,blur_img_dir,lp_coordinates)

    except Exception as e:
        print(f"Error in running billboard detection: {e}")

    

if __name__ == "__main__":
    billboard_base()
    print("Billboard detection completed successfully")