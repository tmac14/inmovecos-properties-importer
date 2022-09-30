from bs4 import BeautifulSoup
import requests
import os
import filecmp
import shutil
import ntpath
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
        datasheet_temp_path = os.path.join(folder_path, 'datasheet.xml.tmp')
        datasheet_content = house.prettify('utf-8')

        if not os.path.isdir(folder_path):
            os.mkdir(folder_path)

        # Create or update house datasheet
        if not os.path.isfile(datasheet_path):
            with open(datasheet_path, 'wb') as f:
                f.write(datasheet_content)
        else:
            with open(datasheet_temp_path, 'wb') as f:
                f.write(datasheet_content)
                
            if not filecmp.cmp(datasheet_path, datasheet_temp_path):
                with open(datasheet_path, 'wb') as d:
                    d.write(datasheet_content)

            os.remove(datasheet_temp_path)

        # Download house images
        images = house.findAll('imagen')
        current_photos = []
        
        for image in images:
            image_url = image.attrs['url']
            filename = normalize_filename(image_url.split("/")[-1])
            image_path = os.path.join(folder_path, filename)
            image_temp_path = os.path.join(folder_path, filename + '.tmp')

            # Open the url image, set stream to True, this will return the stream content.
            r = requests.get(image_url, stream=True)

            if r.status_code == 200:
                # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
                r.raw.decode_content = True
                photo_exists = os.path.isfile(image_path)

                if not photo_exists:
                    with open(image_path, 'wb') as f:
                        shutil.copyfileobj(r.raw, f)
                else:
                    with open(image_temp_path, 'wb') as f:
                        shutil.copyfileobj(r.raw, f)
                    
                    photo_is_equal = compare_images(image_path, image_temp_path)

                    if not photo_is_equal:
                        with open(image_path, 'wb') as f:
                            shutil.copyfileobj(r.raw, f)

                    os.remove(image_temp_path)
                
                current_photos.append(filename)

        # Update asset's pictures. Remove the photos that are no longer present.
        # Extract only the filename in the path. Compare it with the list of new photos 
        path_photos = list(map(lambda p: ntpath.basename(p), get_all_asset_photos(folder_path)))

        for photo in path_photos:
            if photo not in current_photos:
                photo_path = os.path.join(folder_path, photo)
                os.remove(photo_path)

def normalize_filename(name):
    file_split = name.split('.')
    file_name = "".join(file_split[:-1])
    file_type = file_split[-1]
    file_name_normalized = normalize_string(file_name)

    return "%s.%s" % (file_name_normalized, file_type)


if __name__ == "__main__":
    download()
