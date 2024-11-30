import cv2
from ultralytics import YOLO
import numpy as np

def initialize_model():
    model = YOLO('billboard_detection/face_best.pt')
    return model

def detect_faces(image_path, model, confidence_threshold=0.5):
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("Could not read the image")
    
    results = model(image)[0]
    
    detected_faces = []
    
    for detection in results.boxes.data.tolist():
        x1, y1, x2, y2, confidence, class_id = detection

        
        
        if confidence > confidence_threshold:
            x1, y1, x2, y2 = map(int, [x1, y1, x2, y2])
            
            face_info = {
                'bbox': (x1, y1, x2, y2),
                'confidence': confidence
            }
            detected_faces.append(face_info)
            
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
            
            label = f'Face: {confidence:.2f}'
            cv2.putText(image, label, (x1, y1 - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    
    return image, detected_faces

def main():
    model = initialize_model()
    
    # For image detection
    image_path = 'billboard_detection/face.jpg'
    annotated_image, faces = detect_faces(image_path, model)
    cv2.imshow('Face Detection', annotated_image)
    cv2.waitKey(0)

if __name__ == "__main__":
    main()