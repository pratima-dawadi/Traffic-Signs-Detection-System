from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from geopy.geocoders import Nominatim
from dotenv import load_dotenv
import requests,os

def get_geolocation(image_path, default_latitude=27.708621, default_longitude=85.357363):
    img = Image.open(image_path)
    exif_data = img._getexif() or {}
    latitude = None
    longitude = None

    for tag, value in exif_data.items():
        if TAGS.get(tag) == 'GPSInfo':
            for key in value:
                if GPSTAGS.get(key) == 'GPSLatitude':
                    latitude = value[key]
                elif GPSTAGS.get(key) == 'GPSLongitude':
                    longitude = value[key]

    if latitude and longitude:
        lat = convert_to_degrees(latitude)
        lon = convert_to_degrees(longitude)
        return lat, lon
    else:
        return default_latitude, default_longitude

def convert_to_degrees(value):
    d = float(value[0])
    m = float(value[1])
    s = float(value[2])
    return d + (m / 60.0) + (s / 3600.0)

def get_location_name(latitude, longitude):
    geolocator = Nominatim(user_agent="traffic_sign_detector")
    location = geolocator.reverse((latitude, longitude), exactly_one=True)
    # print(f"Location: {location.address}")
    return location.address if location else "Location not found"


def get_geolocation_by_imageid(image_id):
    load_dotenv()
    access_token = os.getenv('ACCESS_TOKEN')
    url=f'https://graph.mapillary.com/{image_id}?access_token={access_token}&fields=id,computed_geometry,detections.value'
    response = requests.get(url)
    geo_location=response.json()['computed_geometry']['coordinates']
    return geo_location


if __name__ == '__main__':
    image_id="110132805133035"
    get_geolocation_by_imageid(image_id)

