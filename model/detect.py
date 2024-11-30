import torch
import cv2
import numpy as np
import os
import sys
import pathlib

from georeference import get_geolocation, get_location_name

sys.path.append('yolov5')
from models.common import DetectMultiBackend
from utils.general import check_img_size, non_max_suppression, scale_boxes
from utils.torch_utils import select_device
from utils.augmentations import letterbox

temp = pathlib.PosixPath
pathlib.PosixPath = pathlib.WindowsPath

device = select_device('')
model = DetectMultiBackend('weights/best_20epochs.pt', device=device, dnn=False, data=None, fp16=False)
stride, names, pt = model.stride, model.names, model.pt
imgsz = check_img_size((640, 640), s=stride)

class_names = model.names if hasattr(model, 'names') else [
    'regulatory--no-parking--g2', 'warning--pedestrians-crossing--g5', 'regulatory--no-entry--g1',
    'regulatory--no-right-turn--g1', 'regulatory--no-left-turn--g2', 'regulatory--no-horn--g1',
    'regulatory--no-stopping--g1', 'information--pedestrians-crossing--g1'
]

# class_names = model.names if hasattr(model, 'names') else [
#     'object--sign-store'
# ]

output_folder = 'inference_images'
os.makedirs(output_folder, exist_ok=True)

def run_inference(image_path,latitude=None,longitude=None):
    latitude, longitude = get_geolocation(image_path, latitude, longitude)
    img0 = cv2.imread(image_path)
    img = letterbox(img0, imgsz, stride=stride, auto=pt)[0]
    img = img.transpose((2, 0, 1))[::-1]
    img = np.ascontiguousarray(img)
    img = torch.from_numpy(img).to(device)
    img = img.float()
    img /= 255.0
    if len(img.shape) == 3:
        img = img[None]

    pred = model(img, augment=False, visualize=False)
    pred = non_max_suppression(pred, conf_thres=0.50, iou_thres=0.45, classes=None, agnostic=False, max_det=1000)

    for i, det in enumerate(pred):
        if len(det):
            det[:, :4] = scale_boxes(img.shape[2:], det[:, :4], img0.shape).round()

            for *xyxy, conf, cls in reversed(det):
                c = int(cls)
                label = f'{class_names[c]} {conf:.2f}'
                plot_one_box(xyxy, img0, label=label, color=(0, 255, 0), line_thickness=3)

        if latitude is not None and longitude is not None:
            geo_label = f'Lat: {latitude:.6f}, Lon: {longitude:.6f}'
            get_location_name(latitude, longitude)

            t_size = cv2.getTextSize(geo_label, cv2.FONT_HERSHEY_SIMPLEX, 1.5, 2)[0]
            text_x, text_y = 10, 50
            cv2.rectangle(img0, (text_x, text_y - t_size[1] - 5), (text_x + t_size[0], text_y + 5), (0, 0, 0), -1)
            cv2.putText(img0, geo_label, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 2)

    output_image_path = os.path.join(output_folder, os.path.basename(image_path))
    cv2.imwrite(output_image_path, img0)

    resized_img = cv2.resize(img0, (800, 600))
    cv2.imshow("Traffic Sign Detection", resized_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def plot_one_box(x, img, color=(128, 128, 128), label=None, line_thickness=3):
    tl = line_thickness or round(0.002 * (img.shape[0] + img.shape[1]) / 2) + 1
    c1, c2 = (int(x[0]), int(x[1])), (int(x[2]), int(x[3]))
    cv2.rectangle(img, c1, c2, color, thickness=tl, lineType=cv2.LINE_AA)

    if label:
        tf = max(tl - 1, 1)
        font_scale=1
        t_size = cv2.getTextSize(label, 0, fontScale=font_scale, thickness=tf)[0]
        
        text_x = c1[0]
        text_y = c1[1] - 2
        
        if text_x + t_size[0] > img.shape[1]:
            text_x = img.shape[1] - t_size[0] - 10

        if text_y < 0:
            text_y = c1[1] + t_size[1] + 5

        cv2.rectangle(img, (text_x, text_y - t_size[1]), (text_x + t_size[0], text_y + 5), (0, 0, 0, 150), -1)
        cv2.putText(img, label, (text_x, text_y), 0,font_scale, (255, 255, 255), thickness=tf, lineType=cv2.LINE_AA)

image_folder = 'images'
for image_file in os.listdir(image_folder):
    if image_file.lower().endswith(('.jpg', '.jpeg', '.png')):
        image_path = os.path.join(image_folder, image_file)
        run_inference(image_path,27.736002037944854,85.33569845164817)
