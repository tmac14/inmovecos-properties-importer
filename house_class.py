import os
from bs4 import BeautifulSoup
from dictionary import *
from util import get_all_asset_photos


class House:
    def __init__(self, datasheet):
        with open(datasheet, 'r', encoding='UTF-8') as file:
            house_data = BeautifulSoup(file, 'xml')

            self.reference = house_data.referencia.text.strip()
            self.kind = family[house_data.familia.text.strip()]
            self.bedrooms = int(house_data.dormitorios.text.strip()) if house_data.dormitorios.text.strip() else 1
            self.single_bedrooms = 1
            self.double_bedrooms = 1
            self.bathrooms = int(house_data.banos.text.strip()) if house_data.banos.text.strip() else 1
            self.toilets = int(house_data.aseos.text.strip()) if house_data.aseos.text.strip() else 0
            self.area_terrain = float(house_data.superficies.parcela.text.strip()) \
                if house_data.superficies.parcela.text.strip() else 1
            self.area_built = float(house_data.superficies.construida.text.strip()) \
                if house_data.superficies.construida.text.strip() else 1
            self.area_util = float(house_data.superficies.habitable.text.strip()) \
                if house_data.superficies.habitable.text.strip() else 1
            self.areas = self.generate_areas(self.area_terrain, self.area_built, self.area_util)
            self.country = countries[house_data.localizacion.pais.text.strip()]
            self.region = house_data.localizacion.provincia.text.strip()
            self.city = house_data.localizacion.poblacion.text.strip()
            self.zone = house_data.localizacion.zona.text.strip()
            if (house_data.localizacion.longitud):
                self.longitude = float(house_data.localizacion.longitud.text.strip()) \
                if house_data.localizacion.longitud.text.strip() else 0
            if (house_data.localizacion.latitud):
                self.latitude = float(house_data.localizacion.latitud.text.strip()) \
                if house_data.localizacion.latitud.text.strip() else 0
            self.address = ''
            self.zip_code = house_data.localizacion.cp.text.strip()
            descriptions = house_data.find('descripciones')
            # Generate default title and description of the property
            self.default_desc = self.generate_default_desc(descriptions)
            # Generate multilanguage title and description information of the property
            self.multi_desc = self.generate_multi_desc(descriptions)
            self.transaction_method = buyop[house_data.operacion.text.strip()]
            if (house_data.precio.text):
                self.price = float(house_data.precio.text.strip())
            self.photos = get_all_asset_photos(os.path.join('assets', self.reference))

    def generate_areas(self, area_terrain, area_built, area_util) -> list:
        if not area_util:
            area_util = area_built - 1 if area_built else area_terrain - 1 if area_terrain else 1

        area_built = area_built if area_built else area_util + 1
        area_terrain = area_terrain if area_terrain else area_built + 1

        return [area_terrain, area_built, area_util]


    def generate_default_desc(self, descs) -> dict:
        if descs.find('descripcion', idioma='es'):
            desc = descs.find('descripcion', idioma='es')
        else:
            desc = descs.findChild()

        return {
            'title': desc.titulo.text.strip(),
            'desc': desc.descripcion.text if desc.descipcion else 'No description'
        }

    def generate_multi_desc(self, descs) -> dict:
        descs_by_langs = {}

        for desc in descs.findAll('descripcion'):
            if not desc.attrs:
                continue

            key_name = "description_" + desc.attrs['idioma']
            descs_by_langs[key_name] = desc.descripcion.text.strip()

        return descs_by_langs

