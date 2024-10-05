import json, os
import requests
from dotenv import load_dotenv

def get_map_feature_ids(json_file,traffic_signs):
    with open(json_file) as f:
        data = json.load(f)
    map_feature_ids = []
    for feature in data['features']:
        if feature['properties']['value'] in traffic_signs:
            map_feature_ids.append(feature['properties']['id'])

    return map_feature_ids

def get_traffic_signs(filename='traffic_signs.txt'):
    try:
        with open(filename) as f:
            return [line.strip() for line in f if line.strip()]
        
    except FileNotFoundError:
        print(f'File {filename} not found')
        return []    


def get_image_ids(map_feature_ids):
    load_dotenv()
    access_token = os.getenv("ACCESS_TOKEN")
    image_ids = []
    for map_feature_id in map_feature_ids:
        url = f"https://graph.mapillary.com/{map_feature_id}?access_token={access_token}&fields=images"
        response = requests.get(url)
        data = response.json()
        if 'images' in data and 'data' in data['images']:
            for image in data['images']['data']:
                print(image['id'])
                image_ids.append(image['id'])

    print(f"Total image ids: {len(image_ids)}")
    return image_ids

def main():
    try:
        traffic_signs = get_traffic_signs()
        print(traffic_signs)
        
        map_feature_ids=get_map_feature_ids('mydata.json',traffic_signs)
        image_ids=get_image_ids(map_feature_ids)
        return image_ids
    except Exception as e:
        print(f"An error occurred: {str(e)}")


if __name__ == '__main__':
    main()