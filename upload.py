import json
import datetime

from house_class import House
from witei_api import WiteiApi
from util import *

#TODO: Rellenar todos los datos de la propiedad a subir en vaules. Logger
def upload():
    assets = get_all_assets('assets')
    for asset in assets:
        house_datasheet = os.path.join(asset, 'datasheet.xml')
        house = House(house_datasheet)
        values = {
            "kind": house.kind,
            "status": "available",
            "bedrooms": house.bedrooms,
            "bathrooms": house.bathrooms,
            "zip_code": house.zip_code,
            "identifier": house.reference,
            "area": house.areas[0],
            "street_number": 2,
            "title": house.default_desc['title'],
            "description": house.default_desc['desc']
        }
        values = json.dumps(values).encode('utf-8')

        witei_api = WiteiApi()

        #TODO: check when datasheet has been updated to prevent update properties with the same content
        if not witei_api.search(house.reference):
            response = witei_api.store(values)
        else:
            response = witei_api.update(house.reference, values)

        code = response.status_code
        data = response.json()

        if 201 != code:
            #TODO: handle errors
            print(data)
        else:
            print(f'Cargando la propiedad con referencia: {house.reference}')

            house_id = data['id']
            files = house.photos
            #TODO: add/remove/replace photos
            for photo in files:
                WiteiApi.upload_photo(house_id, photo)


if __name__ == "__main__":
    upload()
