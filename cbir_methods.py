from PIL import Image as img
import numpy as np
import os, json
#import streamlit as st

def get_intensity(vals):
    """
    Calculates the intesity for the given RGB values.

    Parameters
    ----------
    vals : tuple
        The RGB values, in RGB order

    Returns
    -------
    float
        The intensity value
    """

    return (.299*vals[0]) + (.587*vals[1]) + (.114 * vals[2])


def calculate_intensity(img_path):
    """
    Calculates the intensity for each pixel of the given image and creates
    a histogram.
    
    Parameters
    ----------
    img_path : str
        The file path for the image
    
    Returns
    -------
    tuple
        The first value contains the image size, second value contains the
        intensity histogram
    """

    pic = img.open(img_path)
    width, height = pic.size
    intensities = list()
    bins = list(range(0,250,10))
    bins.append(255)

    for i in range(width):
        for j in range(height):
            intensities.append(get_intensity(pic.getpixel((i,j))))

    hist, bin_edges = np.histogram(intensities, bins=bins)
    return (width*height, hist)

    
def calculate_color_code(img_path):
    """
    Calculates the color-code for each pixel of the given image and creates
    a histogram.
    
    Parameters
    ----------
    img_path : str
        The file path for the image
    
    Returns
    -------
    tuple
        The first value contains the image size, second value contains the
        intensity histogram
    """

    pic = img.open(img_path)
    width, height = pic.size
    decimals = list()

    for i in range(width):
        for j in range(height):
            pixel_vals = pic.getpixel((i,j))
            r = format(pixel_vals[0], 'b').zfill(8)
            g = format(pixel_vals[1], 'b').zfill(8)
            b = format(pixel_vals[2], 'b').zfill(8)
            
            binary = r[0:2] + g[0:2] + b[0:2]
            decimal = int(binary, 2)
            decimals.append(decimal)

    hist, bin_edges = np.histogram(decimals, bins=64)
    return (width*height, hist)

def calculate_manhattan(img1, img2):
    """
    Calculates the Manhattan Distance between the two given lists. The lists
    must be of the same length.

    Parameters
    ----------
    img1 : list
        The histogram for the first image
    img2 : list
        The histogram for the second image

    Returns
    -------
    float:
        The calculated Manhattan Distance
    
    """

    if len(img1) != len(img2):
        print("Error, lengths don't match up")
        return -1
    
    result = 0
    for j in range(len(img1[1])):
        h_i = img1[1][j]
        h_k = img2[1][j]
        size_i = img1[0]
        size_k = img2[0]
        result += abs((h_i / size_i) - (h_k / size_k))
    return result

def get_distance(selected_img, method):
    """
    Calcuates the Manhattan Distance between the selected image and all other
    images in the "images/" directory based on the chosen CBIR method.

    Parameters
    ----------
    selected_img : str
        The file path of the selected image
    method : function
        The chosen CBIR method (either calculate_intensity or calculate_color_code)
    
    Returns
    -------
    list
        A sorted list of tuples containing all of the distances. The first
        value in each tuple is the distance. The second is the image path.
        The list is sorted in ascending order based on distance.
    """

    selected = method(selected_img)
    result = list()
    for img in os.listdir("images/"):
        if img == 'Thumbs.db':
            continue
        path = 'images/' + img
        if path != selected_img:
            retrieved = method(path)
            distance = calculate_manhattan(selected, retrieved)
            result.append((distance, path))
    return sorted(result)

def intensity_data_to_json():
    """
    Computes the Manhattan Distance between every image in the 'images/'
    folder using the Intensity method. Stores all of this data in JSON file.
    """
    intensity_data = dict()
    for img in os.listdir("images/"):
        if img == 'Thumbs.db':
            continue
        path = 'images/' + img
        result = get_distance(path, calculate_intensity)
        intensity_data[path] = result

    with open('intensity_data.json', 'w') as file:
        json.dump(intensity_data, file)

def color_code_data_to_json():
    """
    Computes the Manhattan Distance between every image in the 'images/'
    folder using the Color-code method. Stores all of this data in
    JSON file.
    """
    color_code_data = dict()
    for img in os.listdir("images/"):
        if img == 'Thumbs.db':
            continue
        path = 'images/' + img
        result = get_distance(path, calculate_color_code)
        color_code_data[path] = result

    with open('color_code_data.json', 'w') as file:
        json.dump(color_code_data, file)

