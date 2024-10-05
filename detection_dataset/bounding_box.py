import base64
import mapbox_vector_tile
import matplotlib.pyplot as plt
from PIL import Image
import requests
import os
from dotenv import load_dotenv

def get_geometry(detections_url,traffic_signs):
    response = requests.get(detections_url)
    json_data = response.json()
    
    base64_strings = []
    detection_values=[]
    
    for detection in json_data['data']:
        if detection['value'] in traffic_signs:
            base64_string = detection['geometry']
            print(f"Value: {detection['value']}")
            print(f"base64_string: {base64_string}")
            base64_strings.append(base64_string)
            detection_values.append(detection['value'])
    
    return base64_strings,detection_values


def decode_geometry(base64_string):
    decoded_data = base64.decodebytes(base64_string.encode('utf-8'))
    detection_geometry = mapbox_vector_tile.decode(decoded_data)
    return detection_geometry   


def normalize_coordinate(coordinates,extent):
    normalized_coordinates = [[x / extent,1-( y / extent)] for x, y in coordinates]
    return normalized_coordinates

def get_bounding_box(pixel_coordinates):
    min_x = min(point[0] for point in pixel_coordinates)
    max_x = max(point[0] for point in pixel_coordinates)
    min_y = min(point[1] for point in pixel_coordinates)
    max_y = max(point[1] for point in pixel_coordinates)
    return [min_x,min_y,max_x,max_y]


def convert_to_yolo_format(bbox, class_id):
    x_min, y_min, x_max, y_max = bbox
    x_center = (x_min + x_max) / 2
    y_center = (y_min + y_max) / 2
    width = x_max - x_min
    height = y_max - y_min
    print(f"Yolo Annotation: {class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}")
    return f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}"


def process_detections(base64_strings,detection_values):
    all_yolo_annotations = []
    all_bboxes = []

    for base64_string, detection_value in zip(base64_strings, detection_values):
        detection_geometry = decode_geometry(base64_string)
        
        yolo_annotations = []
        bboxes = []
        
        for feature in detection_geometry['mpy-or']['features']:
            extent = detection_geometry['mpy-or']['extent']
            coordinates = feature['geometry']['coordinates'][0]
            normalized_coords = normalize_coordinate(coordinates, extent)
            
            bbox = get_bounding_box(normalized_coords)
            try:
                traffic_signs=get_traffic_signs()
                index = traffic_signs.index(detection_value)
                print(f"detection_value '{detection_value}' found at index: {index}")
            except ValueError:
                print(f"detection_value '{detection_value}' not found in traffic_signs.")
                index = -1 
                
            if index != 1:
                yolo_annotation = convert_to_yolo_format(bbox,index)
            
                yolo_annotations.append(yolo_annotation)
                bboxes.append(bbox)
        
        all_yolo_annotations.extend(yolo_annotations)
        all_bboxes.extend(bboxes)
    
    return all_yolo_annotations, all_bboxes


def visualize_annotations(image_path, bboxes):
    img = Image.open(image_path)
    fig, ax = plt.subplots()
    ax.imshow(img)

    for bbox in bboxes:
        x_min, y_min, x_max, y_max = bbox
        width = x_max - x_min
        height = y_max - y_min

        rect = plt.Rectangle(((x_min ) * img.width, (y_min ) * img.height), 
                             width * img.width, height * img.height, 
                             fill=False, edgecolor='red', linewidth=2)
        ax.add_patch(rect)

    plt.show()


def get_traffic_signs():
    filename='traffic_signs.txt'
    try:
        with open(filename) as f:
            return [line.strip() for line in f if line.strip()]
        
    except FileNotFoundError:
        print(f'File {filename} not found')
        return []


def run_bounding_box(image_ids):
    try:
        # image_ids = ['142058724553367']
        load_dotenv()
        access_token = os.getenv("ACCESS_TOKEN")

        for image_id in image_ids:
            detections_url = f"https://graph.mapillary.com/{image_id}/detections?access_token={access_token}&fields=geometry,value"
            traffic_signs = get_traffic_signs() 
        
            get_image_infos = get_geometry(detections_url,traffic_signs)
            base64_string,detection_value=get_image_infos
        
            image_path = f"my_images/{image_id}.jpg"
            
            file_name_with_extension = os.path.basename(image_path)
            file_name, _ = os.path.splitext(file_name_with_extension)
            
            os.makedirs("my_labels",exist_ok=True)
            label_file=os.path.join("my_labels",f'{file_name}.txt')
            
            yolo_annotations, bboxes = process_detections(base64_string,detection_value)
            
            print("YOLO format annotations:")
            
            with open(label_file, "w") as f:
                for annotation in yolo_annotations:
                    f.write(annotation + "\n")
            
            visualize_annotations(image_path, bboxes)

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    run_bounding_box(['26746176454973627'])
    





