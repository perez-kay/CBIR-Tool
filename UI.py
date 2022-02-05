import streamlit as st
import json
import relevance_feedback as rf
import pandas as pd

with open('intensity_data.json') as f:
    intensity_data = json.load(f)

with open('color_code_data.json') as f:
    color_code_data = json.load(f)

normalized_matrix = pd.read_csv('normalized_matrix.csv', index_col=0).T

st.session_state.intensity = intensity_data
st.session_state.color_code = color_code_data
st.session_state.normalized_matrix = normalized_matrix

st.set_page_config(page_title='CBIR Tool')

def get_image_path(img_num):
    """
    Creates a file path for the given image number.

    Parameters
    ----------
    img_num : float
        The image number
    
    Returns
    -------
    str
        A valid file path for the image in the form of "images/<img_num>.jpg"
    """

    return "images/" + str(int(img_num)) + ".jpg"


# Create page title and introduction
st.title("Content-Based Image Retrieval Tool")
st.write("Welcome to the CBIR Tool! To view the images in the database, type a \
         number into the box below. Once you've selected an image, use the \
         drop down menu to choose a CBIR method. Then click \"Retrieve \
         Images\" to retrieve images based on the method you chose. \
         Your retrieval results will be displayed to the right.")

# Create 2 columns 
left_col, right_col = st.columns(2)

# Initialize results key in the session state
if 'results' not in st.session_state:
    st.session_state.results = -1

if 'page_number' not in st.session_state:
    st.session_state.page_number = 0

if 'relevant_imgs' not in st.session_state:
    st.session_state.relevant_imgs = set()

left_col , right_col = st.columns([5, 2])

with left_col:
    # Select an image and display it. Displays image 1 by default
    img_num = st.number_input("Select an image by typing a number between 1 - 100", min_value=1, max_value=100, step=1)
    img_path = get_image_path(img_num)
    st.image(image=img_path, use_column_width='always')

with right_col:
    # Set up the select box for the color codes
    methods = ['-', "Intensity", "Color-Code", "Intensity + Color-Code"]
    option = st.selectbox('Choose a method', methods)
    use_rf = st.checkbox('Use Relevance Feedback', key='use_rf')

    # Set up the run button
    run_checked = st.button("Retrieve Images")

# Display these items in the right columm
with st.container():
    # If the button has been pressed
    if run_checked:
        st.session_state.page_number = 0
        st.session_state.results = -1

        if option == '-':
            with left_col:
                st.error("Please select a method first.")
        else:
            # Fetch results based on mode chosen
            if option == "Intensity":
                results = st.session_state.intensity[img_path]
                st.session_state.relevant_imgs = set() # user chose a diff method, so reset rf results
            if option == "Color-Code":
                results = st.session_state.color_code[img_path]
                st.session_state.relevant_imgs = set() # user chose a diff method, so reset rf results
            if option == "Intensity + Color-Code":
                results = rf.calculate_no_bias_dist(st.session_state.normalized_matrix, rf.get_img_num(img_path))
            
            # Update session state so it remembers results
            st.session_state.results = results
    
    # If the results exist
    if st.session_state.results != -1:
        #Get the image paths for the results     
        img_results = [path for distance, path in st.session_state.results]
        
        
        N = 20 # number of entries per page

        # set up pageination
        last_page = len(img_results) // N
        prev, page_num, next = st.columns([3, 3, 1])

        if next.button('Next Page'):
            if (st.session_state.page_number + 1) > last_page:
                st.session_state.page_number = last_page
            else:
                st.session_state.page_number += 1

        if prev.button("Previous Page"):
            if (st.session_state.page_number - 1) < 0:
                st.session_state.page_number = 0
            else:
                st.session_state.page_number -= 1

        page_num.write("Page " + str(st.session_state.page_number + 1) + " of 5")

        start_idx = st.session_state.page_number * N
        end_idx = ((1 + st.session_state.page_number) * N)

        # display results in a grid
        while start_idx < end_idx:
            if end_idx == 100:
                end_idx -= 1
            for _ in range(end_idx):
                cols = st.columns(5)
                for col_num in range(5):
                    if start_idx < end_idx:
                        cols[col_num].image(img_results[start_idx], use_column_width='always', caption=img_results[start_idx])
                        if option == "Intensity + Color-Code" and use_rf:
                            checked = cols[col_num].checkbox('Relevant', key=img_results[start_idx])
                            if checked:
                                st.session_state.relevant_imgs.add(img_results[start_idx])
                            if img_results[start_idx] in st.session_state.relevant_imgs and not checked:
                                st.session_state.relevant_imgs.remove(img_results[start_idx])
                    start_idx += 1
        #print(st.session_state.relevant_imgs)
             



