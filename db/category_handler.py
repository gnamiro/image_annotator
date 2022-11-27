import os
import sys
from pathlib import Path
from shutil import copyfile



images_folder = Path('./react-image-annotate/public/images/images')
categories_folder = Path('./react-image-annotate/public/images/categories')


def create_categories(labels):
    if not os.path.exists(categories_folder):
        os.makedirs(categories_folder)
        
    cat_lists = os.listdir(categories_folder)
    for label in labels:
        if label not in cat_lists:
            os.makedirs(categories_folder / label)
    
    print(os.listdir(categories_folder))

def add_image_folder(label, image_name):
    try:
        if image_name not in os.listdir(categories_folder / label):
            copyfile(images_folder / image_name, categories_folder / label / image_name)
    except:
        print('error in augmenting image ' + image_name + ' to category ' + label)    
    return

def remove_image_folder(label, image_name):
    try: 
        if image_name in os.listdir(categories_folder / label):
            os.remove(categories_folder / label / image_name)
    except:
        print('nothing there')    
    return