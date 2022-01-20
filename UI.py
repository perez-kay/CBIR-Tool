import streamlit as st
from PIL import Image
import numpy as np
import os, cbir_methods, paginator

st.set_page_config(layout='wide', page_title='CBIR Tool')

def get_image_path(img_num):
    """
    Returns the image path for the given image number.
    """
    return "images/" + str(int(img_num)) + ".jpg"


st.title("Content-Based Image Retrieval")

left_col, right_col = st.columns(2)

with left_col:
    # select an image and display it. Displays image 1 by default
    img_num = st.number_input("Select an image by typing a number between 1 - 100", min_value=1, max_value=100, step=1)
    img_path = get_image_path(img_num)
    st.image(image=(img_path), use_column_width='always')


    methods = ['-', "Intensity", "Color-Code"]

    
    option = st.selectbox('Choose a method', methods)

with right_col:
    if option != '-':
        if option == "Intensity":
            with st.spinner('Fetching your results...'):
                results = cbir_methods.get_distance(img_path, cbir_methods.calculate_intensity)
            
        if option == "Color-Code":
            with st.spinner('Fetching your results...'):
                results = cbir_methods.get_distance(img_path, cbir_methods.calculate_color_code)

        img_results = [path for distance, path in results]
        img_iter = paginator.paginator('View Results', img_results, items_per_page=20, on_sidebar=False)
        indicies, imgs = map(list, zip(*img_iter))
        st.image(imgs, width=150, caption=imgs)



