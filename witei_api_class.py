import os
import mimetypes
from urllib import response
import requests


class WiteiApi:
    token = '4a059a6ffe6d4e88b135b724adbd949e'
    endpoint_house_upload = 'https://witei.com/api/v1/houses/'
    endpoint_house_update = 'https://witei.com/api/v1/houses/{house_id}/'
    endpoint_photo_upload = 'https://witei.com/api/v1/houses/{house_id}/pictures/?'

    @staticmethod
    def store(data) -> requests:
        headers = {
            'Authorization': f'Bearer {WiteiApi.token}',
            'Content-Type':  'application/json'
        }

        response = requests.post(WiteiApi.endpoint_house_upload, data=data, headers=headers)

        return response

    @staticmethod
    def update(house_id, data) -> requests:
        headers = {
            'Authorization': f'Bearer {WiteiApi.token}',
            'Content-Type':  'application/json'
        }

        response = requests.put(WiteiApi.get_house_endpoint_formatted(house_id, WiteiApi.endpoint_house_update), data=data, headers=headers)

        return response

    @staticmethod
    def search(house_id) -> requests:
        #TODO
        response = ''
        headers = {
            'Authorization': f'Bearer {WiteiApi.token}',
            'Content-Type':  'application/json'
        }

        return response

    @staticmethod
    def upload_photo(house_id, file_path) -> requests:
        file_name = os.path.basename(file_path)
        file_mime = mimetypes.guess_type(file_path)[0]
        file = [('pic', (file_name, open(file_path, 'rb'), file_mime))]

        headers = {
            'Authorization': f'Bearer {WiteiApi.token}',
            'Content-Type': 'multipart/form-data'
        }

        response = requests.post(WiteiApi.get_house_endpoint_formatted(house_id, WiteiApi.endpoint_photo_upload), files=file, headers=headers)

        return response

    @staticmethod
    def get_house_endpoint_formatted(house_id, endpoint) -> str:
        return endpoint.replace('{house_id}', str(house_id))

