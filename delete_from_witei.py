import requests
import os
import json
import math
from dotenv import load_dotenv

load_dotenv('.env.local')

headers = {
    'Authorization': f'Bearer {os.getenv("WITEI_TOKEN")}',
    'Content-Type':  'application/json'
}
response = requests.get('https://witei.com/api/v1/houses/', headers=headers)
result = response.json()
total_results = result['count']
result_per_pages = 50
num_pages = math.ceil(total_results/result_per_pages)

for page in range(0, num_pages):
    current_page = page + 1
    url = 'http://witei.com/api/v1/houses/?page=%s' % current_page
    response = requests.get(url, headers=headers)
    result = response.json()

    for house in result['results']:
        delete_url = 'https://witei.com/api/v1/houses/%s/' % house['id']
        delete_response = requests.delete(delete_url, headers=headers)