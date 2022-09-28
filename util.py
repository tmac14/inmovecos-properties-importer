from lzma import FILTER_LZMA2
import os
import imghdr
from PIL import Image, ImageChops

def get_all_assets(asset_path):
    folders_path = []
    for name in os.listdir(asset_path):
        folder_path = os.path.join(asset_path, name)
        if os.path.isdir(folder_path):
            folders_path.append(folder_path)

    return folders_path

def get_all_asset_photos(asset_path):
    photos = []
    for name in os.listdir(asset_path):
        photo_path = os.path.join(asset_path, name)
        if imghdr.what(photo_path):
            photos.append(photo_path)

    return photos


def compare_image_pixels(base_image, compare_image):
    """
    Calculates the bounding box of the non-zero regions in the image.
    :param base_image: target image to find
    :param compare_image: set of images containing the target image
    :return The bounding box is returned as a 4-tuple defining the 
            left, upper, rightm and lower pixel coordinate. If the image
            is completly empty, this method returns None.
    """
    # Returns the absolute value of the pixel-by-pixel
    # difference between two images.

    diff = ImageChops.difference(base_image, compare_image)
    if diff.getbbox():
        return False
    else:
        return True

def compare_file_bytes(base_file, compare_file):
    with open(base_file, 'rb') as f:
         return f.read() == compare_file
