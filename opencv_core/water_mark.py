#!/usr/bin/env python3
import argparse
import os
from os.path import join
import cv2 as cv

RATIO_FOR_OFFSET = RATIO_FOR_LOGO = 0.15

def add_warter_mark(folder, logo):
    # Read all image files
    images = read_all_image_in_folder(folder)

    # Check exist logo URL. if it doesn't, use the TEEC logo
    cvLogo = get_logo_image(None)

    # Add logo to each image
    output_images = [(img[0] ,warter_mark_on_image(img, cvLogo)) for img in images]

    # Save all image to output folder
    save_warter_mark_images_in_output_folder(output_images, folder)

def read_all_image_in_folder(folder):
    images = []
    for root, _, files in os.walk(folder):
        files_in_folder = [(name ,join(root, name)) for name in files]
        images.extend(files_in_folder)
    
    images = [(img[0] ,cv.imread(img[1],1)) for img in images]
    return images

def get_logo_image(logo):
    logo_url = 'teec.jpg'
    if logo:
        logo_url = logo
    return cv.imread(logo_url,1)


def warter_mark_on_image(img, logo):
    cvImage = img[1]

    # get size of logo on image
    logo_size = get_size_of_logo_on_image(cvImage, logo)
    height_logo = logo_size[1]
    width_logo = logo_size[0]

    # resize logo
    resized_logo = cv.resize(logo,(width_logo,height_logo))

    # get off set of logo on image
    offset = get_offset_logo(cvImage, logo)
    x_offset = offset[0]
    y_offset = offset[1]

    # do ROI
    cvImage[y_offset:(y_offset + height_logo), x_offset:(x_offset + width_logo)] = resized_logo

    return cvImage

def get_size_of_logo_on_image(cvImage, logo):
    # get image size
    img_size = get_image_size(cvImage)

    # get size of the smallest direction: vertical or horizontal
    smalles_direction_size = img_size[0]
    if img_size[0] > img_size[1]:
        smalles_direction_size = img_size[1]

    # get size logo base on real logo size, direction size and ratio for logo
    crop_size = int(smalles_direction_size*RATIO_FOR_LOGO)
    return (crop_size, crop_size)

def get_offset_logo(image, logo):
    # get image size
    # img_size = get_image_size(image)

    # get off set of logo base on image size
    # with first verion, we take it from left - top of image 
    logo_size = get_size_of_logo_on_image(image, logo)

    return logo_size

def get_image_size(image):
    shape = image.shape
    return (shape[0], shape[1])

def save_warter_mark_images_in_output_folder(images, folder):
    # create output in folder
    dirname = 'output'
    output = join(folder, dirname)
    os.mkdir(output)

    for img in images:
        image_name = img[0]
        cvImage = img[1]
        full_output_name = join(output, image_name)
        print("Test output ", full_output_name)
        cv.imwrite(full_output_name, cvImage)

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("folder", help="The folder include all images you want to add warter mark.",
                        type=str)
    parser.add_argument("-w","--warter_mark", help="This is the image file that is warter mark you want.",
                        type=str)

    args = parser.parse_args()

    add_warter_mark(args.folder, args.warter_mark)

if __name__ == "__main__":
    main()