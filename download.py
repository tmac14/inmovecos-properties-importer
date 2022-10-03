from bs4 import BeautifulSoup
import requests
import os
import filecmp
import shutil
import ntpath
import json
from util import *

# Inmoweb feed endpoint for create a XML file with all properties registered in the software for Inmovecos Real Estate
url = 'https://feed.inmoweb.es/?key=8028814628EC63EA8335E3766F1B75A8C7F09767'
document = requests.get(url)
soup = BeautifulSoup(document.content, 'xml')
houses = soup.findAll('propiedad')


def download() -> None:
    for house in houses:
        house_id = house.referencia.text.strip()
        folder_path = os.path.join('assets', house_id)
        datasheet_path = os.path.join(folder_path, 'datasheet.xml')
        datasheet_tmp_path = os.path.join(folder_path, 'datasheet.xml.tmp')
        datasheet_content = house.prettify('utf-8')

        if not os.path.isdir(folder_path):
            os.mkdir(folder_path)

        # Create or update house datasheet
        if not os.path.isfile(datasheet_path):
            with open(datasheet_path, 'wb') as f:
                f.write(datasheet_content)
        else:
            with open(datasheet_tmp_path, 'wb') as f:
                f.write(datasheet_content)
                
            if not filecmp.cmp(datasheet_path, datasheet_tmp_path):
                with open(datasheet_path, 'wb') as d:
                    d.write(datasheet_content)

            os.remove(datasheet_tmp_path)

        # Download house images
        images = house.findAll('imagen')
        current_photos = {}
        photos_registry_path = os.path.join(folder_path, 'photos_registry.json')
        old_photos = get_photos_registry(photos_registry_path)
        
        for image in images:
            image_url = image.attrs['url']
            # Open the url image, set stream to True, this will return the stream content.
            r = requests.get(image_url, stream=True)

            if 200 == r.status_code:
                # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
                r.raw.decode_content = True
                filename = image_url.split("/")[-1]
                filename_normalized = normalize_string(filename)
                photo_exists = True if old_photos and filename_normalized in old_photos else False
                filename_hashed = old_photos[filename_normalized] if photo_exists else get_unique_filename(filename_normalized)
                image_path = os.path.join(folder_path, filename_hashed)
                image_tmp_path = os.path.join(folder_path, filename_hashed + '.tmp')

                if not photo_exists:
                    with open(image_path, 'wb') as f:
                        shutil.copyfileobj(r.raw, f)
                else:
                    with open(image_tmp_path, 'wb') as f:
                        shutil.copyfileobj(r.raw, f)
                        
                    photo_is_equal = compare_images(image_path, image_tmp_path)

                    if not photo_is_equal:
                        with open(image_path, 'wb') as f:
                            shutil.copyfileobj(r.raw, f)

                    os.remove(image_tmp_path)
                
                current_photos[filename_normalized] = filename_hashed 

        # Store current photos registry
        with open(photos_registry_path, 'w') as f:
            f.write(json.dumps(current_photos, indent=2))

        # Update asset's pictures. Remove the photos that are no longer present.
        # Extract only the filename in the path. Compare it with the list of new photos 
        stored_photos = list(map(lambda p: ntpath.basename(p), get_all_asset_photos(folder_path)))

        for photo in stored_photos:
            if not photo in current_photos.values():
                photo_path = os.path.join(folder_path, photo)
                os.remove(photo_path)

def get_unique_filename(name):
    file_split = name.split('.')
    filename = "".join(file_split[:-1])
    file_type = file_split[-1]
    filename_hashed = get_unique_hash_from_string(filename)

    return "%s.%s" % (filename_hashed, file_type)

def get_photos_registry(path):
    result = None

    if os.path.isfile(path):
        with open(path, 'r') as f:
            result = json.load(f)
    
    return result


if __name__ == "__main__":
    download()
