import os
import imghdr
import cv2
import numpy
import string
import random
import hashlib
import re
from unicodedata import normalize

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

def compare_files(base_file, compare_file):
    with open(base_file, 'r', encoding='UTF-8') as fb, open(compare_file, 'r', encoding='UTF-8') as fc:
        base_file_line = fb.readline()
        compare_file_line = fc.readline()
        files_are_equals = True

        while base_file_line != '' or compare_file_line != '':
            base_file_line = base_file_line.rstrip()
            compare_file_line = compare_file_line.rstrip()
            
            if base_file_line != compare_file_line:
                print("Base Line: %s\nCompare Line: %s" % (base_file_line, compare_file_line))
                files_are_equals = False
                break

            base_file_line = fb.readline()
            compare_file_line = fc.readline()

        return files_are_equals

def compare_images(base_file, compare_file):
    base_file = cv2.imread(base_file)
    compare_file = cv2.imread(compare_file)
    diff = cv2.subtract(base_file, compare_file)
    result = not numpy.any(diff)

    return result == True

def get_unique_hash_from_string(s):
    letters = string.ascii_lowercase
    random_str = ''.join(random.choice(letters) for i in range(15))
    s = (s + random_str).encode() 
    random_hash = hashlib.md5(s)

    return random_hash.hexdigest()

def normalize_string(value):
    s = re.sub(
        r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", 
        normalize( "NFD", value)
    )
    s = s.lower().replace('ñ', 'n')

    return s