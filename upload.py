import json
from house_class import House
from witei_api_class import WiteiApi
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
        house_internal_id = witei_api.search_by_id(house.reference)

        if not house_internal_id:
            response = witei_api.store(values)
            data = response.json()
            house_internal_id = data['id']
            action = 'Cargando'
        else:
            response = witei_api.update(house_internal_id, values)
            action = 'Actualizando'

        code = response.status_code

        if code not in [200, 201]:
            #TODO: handle errors
            print(code)
        else:
            print(f'{action} la propiedad con referencia: {house.reference} ({house_internal_id})')

            files = house.photos
            
            #TODO: add/remove/replace photos
            for photo in files:
                WiteiApi.upload_photo(house_internal_id, photo)


if __name__ == "__main__":
    upload()
