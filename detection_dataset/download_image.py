import requests, os
from dotenv import load_dotenv

def get_image_url(api_url):
    response = requests.get(api_url)
    image_data = response.json()
    image_url = image_data['thumb_original_url']
    return image_url

def download_image(url, filename):
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        with open(filename, 'wb') as file:
            file.write(response.content)
        
        print(f"Image successfully downloaded: {filename}")
    
    except Exception as e:
        print(f"An error occurred: {e}")


def main():
    try:
        load_dotenv()
        access_token = os.getenv("ACCESS_TOKEN")
        image_ids = ['477306593503728', '532278331102701', '147107937426847', '395154942435870', '292807716336713','3776981739096254']
        for image_id in image_ids:
            print(image_id)
            api_url = f'https://graph.mapillary.com/{image_id}?access_token={access_token}&fields=height,width,thumb_original_url'        
            requested_url=get_image_url(api_url)
            print(requested_url)
            file_path = f"{image_id}.jpg"
            download_image(requested_url, file_path)

    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == '__main__':
    main()





