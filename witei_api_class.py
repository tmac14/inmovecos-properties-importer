import os
import mimetypes
import requests
from dotenv import load_dotenv

load_dotenv('.env.local')

class WiteiApi:
    @staticmethod
    def store(data) -> requests:
        headers = {
            'Authorization': f'Bearer {os.getenv("WITEI_TOKEN")}',
            'Content-Type':  'application/json'
        }

        response = requests.post(os.getenv("ENDPOINT_HOUSE_UPLOAD"), data=data, headers=headers)

        return response

    @staticmethod
    def update(house_id, data) -> requests:
        headers = {
            'Authorization': f'Bearer {os.getenv("WITEI_TOKEN")}',
            'Content-Type':  'application/json'
        }

        response = requests.put(WiteiApi.get_house_endpoint_formatted(house_id, os.getenv("ENDPOINT_HOUSE_UPDATE")), data=data, headers=headers)
   
        return response

    @staticmethod
    def search_by_id(house_id) -> int or bool:
        headers = {
            'Authorization': f'Bearer {os.getenv("WITEI_TOKEN")}',
            'Content-Type':  'application/json'
        }

        response = requests.get(WiteiApi.get_house_endpoint_formatted(house_id, os.getenv("ENDPOINT_HOUSE_SEARCH_BY_ID")), headers=headers)
        
        if 200 == response.status_code:
            data = response.json()
            
            if data['count']:
                return data['results'][0]['id']

        return False

    @staticmethod
    def upload_photo(house_id, file_path) -> requests:
        file_name = os.path.basename(file_path)
        file_mime = mimetypes.guess_type(file_path)[0]
        file = [('pic', (file_name, open(file_path, 'rb'), file_mime))]

        headers = {
            'Authorization': f'Bearer {os.getenv("WITEI_TOKEN")}'
        }
        
        response = requests.post(WiteiApi.get_house_endpoint_formatted(house_id, os.getenv("ENDPOINT_PICTURE_UPLOAD")), files=file, headers=headers)
        
        return response

    @staticmethod
    def get_house_endpoint_formatted(house_id, endpoint) -> str:
        return endpoint.replace('{house_id}', str(house_id))

