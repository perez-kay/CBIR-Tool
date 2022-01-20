from select import select
from PIL import Image as img
import matplotlib.pyplot as plt
import numpy as np
import os
import streamlit as st

def get_intensity(vals):
    return (.299*vals[0]) + (.587*vals[1]) + (.114 * vals[2])


def calculate_intensity(img_path):
    """
    Calculates the intensity for each pixel of the given image.
    Returns, as a list, the histogram bins for each intensity.
    """
    pic = img.open(img_path)
    width, height = pic.size
    #pixels = list(pic.getdata())
    #pixels = np.array(pixels).reshape((width, height, 3))

    intensities = list()
    bins = list(range(0,250,10))
    bins.append(255)
    for i in range(width):
        for j in range(height):
            intensities.append(get_intensity(pic.getpixel((i,j))))
            
    hist, bin_edges = np.histogram(intensities, bins=bins)
    return (width*height, hist)



    
def calculate_color_code(img_path):
    pic = img.open(img_path)
    width, height = pic.size
    #pixels = list(pic.getdata())
    #pixels = np.array(pixels).reshape((width, height, 3)) 
    binaries = list()

    for i in range(width):
        for j in range(height):
            pixel_vals = pic.getpixel((i,j))
            r = format(pixel_vals[0], 'b').zfill(8)
            g = format(pixel_vals[1], 'b').zfill(8)
            b = format(pixel_vals[2], 'b').zfill(8)
            
            binary = r[0:2] + g[0:2] + b[0:2]
            decimal = int(binary, 2)
            binaries.append(decimal)
    hist, bin_edges = np.histogram(binaries, bins=64)
    
    return (width*height, hist)

def calculate_manhattan(img1, img2):
    if len(img1) != len(img2):
        print("Error, lengths don't match up")
        return -1
    
    result = 0
    for j in range(len(img1[1])):
        h_i = img1[1][j]
        h_k = img2[1][j]
        size_i = img1[0]
        size_k = img2[0]
        #if size_i == size_k:
         #   result += abs((h_i  - h_k))
        #else:

        result += abs((h_i / size_i) - (h_k / size_k))
    return result

#@st.cache
# def get_intensity_distance(selected_img):
#     selected_intensity = calculate_intensity(selected_img)
#     result = list()
#     for img in os.listdir("images/"):
#         if img == 'Thumbs.db':
#             continue
#         path = 'images/' + img
#         if path != selected_img:
#             intensity = calculate_intensity(path)
#             distance = calculate_manhattan(selected_intensity, intensity)
#             result.append((distance, path))
#     return sorted(result)

@st.cache(show_spinner=False)
def get_distance(selected_img, method):
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

img1 = calculate_color_code('images/1.jpg')
img2 = calculate_color_code('images/41.jpg')
img3 = calculate_color_code('images/24.jpg')
print(img1)
print(img3)
#print('The wrong img:', calculate_manhattan(img1, img2))

#print('The right img:', calculate_manhattan(img1, img3))



