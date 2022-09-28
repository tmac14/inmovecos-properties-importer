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
                
                if not filecmp.cmp(datasheet_path, datasheet_temp_path, shallow=False):
                    print("%s: property data has changed, new datasheet saved!" % house_id)

                    with open(datasheet_path, 'wb') as d:
                        d.write(datasheet_content)

            os.remove(datasheet_temp_path)

        # Download house images
        images = house.findAll('imagen')
        current_photos = []

        for image in images:
            imageUrl = image.attrs['url']
            filename = imageUrl.split("/")[-1]
            imagePath = os.path.join(folder_path, filename)

            # Open the url image, set stream to True, this will return the stream content.
            r = requests.get(imageUrl, stream=True)

            if r.status_code == 200:
                # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
                r.raw.decode_content = True
                photo_exists = os.path.isfile(imagePath)
                photo_is_equal = compare_file_bytes(imagePath, r.raw)

                if not photo_exists or not photo_is_equal:
                    if not photo_exists:
                        print("%s: property has a new photo, saved as %s" % (house_id, filename))
                    elif not photo_is_equal:
                        print("%s: photo with same name (%s) has found but it has changed, updating..." % (house_id, filename))

                    with open(imagePath, 'wb') as f:
                        shutil.copyfileobj(r.raw, f)
                        current_photos.append(filename)

        # Update asset's pictures. Remove the photos that are no longer present.
        # Extract only the filename in the path. Compare it with the list of new photos 
        path_photos = list(map(lambda p: ntpath.basename(p), get_all_asset_photos(folder_path)))

        for photo in path_photos:
            if photo not in current_photos:
                print ("%s: %s is no longer present, removing..." % (house_id, photo))

                photo_path = os.path.join(folder_path, photo)
                os.remove(photo_path)

if __name__ == "__main__":
    download()
