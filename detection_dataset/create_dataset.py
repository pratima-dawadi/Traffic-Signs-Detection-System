from get_image_ids import get_map_feature_ids, get_image_ids, get_traffic_signs
from download_image import get_image_url,download_image
from bounding_box import  get_traffic_signs,get_geometry,process_detections
from dotenv import load_dotenv


import os

def main():
    load_dotenv()
    try:
        traffic_signs=get_traffic_signs()
        map_feature_ids=get_map_feature_ids('mydata.json',traffic_signs)
        image_ids=get_image_ids(map_feature_ids)
        access_token = os.getenv("ACCESS_TOKEN")

        for index,image_id in enumerate(image_ids):
            # for downloading images
            print(f"Processing image {index + 1} of {len(image_ids)}: {image_id}")
            api_url = f'https://graph.mapillary.com/{image_id}?access_token={access_token}&fields=height,width,thumb_original_url'        
            requested_url=get_image_url(api_url)
            image_path = f"dataset/{image_id}.jpg"
            download_image(requested_url, image_path)

            # for bounding box
            detections_url = f"https://graph.mapillary.com/{image_id}/detections?access_token=MLY|8762874607096127|eb796795adeb3076d55fe53a03756e35&fields=geometry,value"
            traffic_signs = get_traffic_signs() 
        
            base64_string,detection_value=get_geometry(detections_url,traffic_signs)
                   
            file_name_with_extension = os.path.basename(image_path)
            file_name, _ = os.path.splitext(file_name_with_extension)
            
            label_file=os.path.join("dataset",f'{file_name}.txt')
            
            yolo_annotations, bboxes = process_detections(base64_string,detection_value)
                        
            with open(label_file, "w") as f:
                for annotation in yolo_annotations:
                    f.write(annotation + "\n")     

    except Exception as e:
        print(f"An error occurred: {str(e)}")


if __name__ == '__main__':
    main()