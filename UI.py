import streamlit as st
import json
import relevance_feedback as rf
import pandas as pd

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

# Import intensity data
with open('intensity_data.json') as f:
    intensity_data = json.load(f)

# Import color code data
with open('color_code_data.json') as f:
    color_code_data = json.load(f)

# Import normalization matrix
normalized_matrix = pd.read_csv('normalized_matrix.csv', index_col=0).T

# Store these data so we only load them once
st.session_state.intensity = intensity_data
st.session_state.color_code = color_code_data
st.session_state.normalized_matrix = normalized_matrix

# Set page title
st.set_page_config(page_title='CBIR Tool')

# Create page title and introduction
st.title("Content-Based Image Retrieval Tool")
st.write("Welcome to the CBIR Tool! To view the images in the database, type a \
         number into the box below. Once you've selected an image, use the \
         drop down menu to choose a CBIR method. Then click \"Retrieve \
         Images\" to retrieve images based on the method you chose. \
         Your retrieval results will be displayed to the right.")

# Initialize values in session state to cache them on page reload
if 'results' not in st.session_state:
    st.session_state.results = -1

if 'page_number' not in st.session_state:
    st.session_state.page_number = 0

if 'relevant_imgs' not in st.session_state:
    st.session_state.relevant_imgs = set()

if 'curr_img_num' not in st.session_state:
        st.session_state.curr_img_num = -1

# Create 2 columns 
left_col , right_col = st.columns([5, 2])

# Display these items in the left column
with left_col:
    # Select an image and display it. Displays image 1 by default
    img_num = st.number_input("Type a number between 1 - 100 to select an image", \
                              min_value=1, max_value=100, step=1)
    img_path = get_image_path(img_num)
    st.image(image=img_path, use_column_width='always')
    if img_num != st.session_state.curr_img_num:
        keys_to_skip = ['intensty', 'color_code', 'normalized_matrix', \
                        'results', 'page_number', 'relevant_imgs', \
                        'curr_img_num']
        st.session_state.curr_img_num = img_num
        st.session_state.relevant_imgs = set()
        for key in st.session_state.keys():
            if key not in keys_to_skip:
                del st.session_state[key]
        st.session_state.results = -1
        

with right_col:
    # Set up the select box for the color codes
    methods = ['-', "Intensity", "Color-Code", "Intensity + Color-Code"]
    option = st.selectbox('Choose a method', methods)
    use_rf = st.checkbox('Use Relevance Feedback', key='use_rf')

    # Set up the run button
    run_checked = st.button("Retrieve Images")

# Display these items in a container
with st.container():
    # If the button has been pressed
    if run_checked:
        # Reset page number and clear results
        st.session_state.page_number = 0
        st.session_state.results = -1

        if option == '-':
            with left_col:
                st.error("Please select a method first.")
        
        # Get results based on chosen method
        else:
            if option == "Intensity":
                results = st.session_state.intensity[img_path]
                st.session_state.relevant_imgs = set() # clear RF choices upon method switch

            if option == "Color-Code":
                results = st.session_state.color_code[img_path]
                st.session_state.relevant_imgs = set() # clear RF choices upon method switch

            if option == "Intensity + Color-Code":
                if len(st.session_state.relevant_imgs) == 0: # if doing I + CC for the first time
                    results = rf.calculate_distance(st.session_state.normalized_matrix, \
                            st.session_state.curr_img_num, 1/89)
                else:
                    results = rf.calculate_updated_weight(st.session_state.relevant_imgs, \
                            st.session_state.normalized_matrix, \
                            st.session_state.curr_img_num)

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

        # Display results in a grid
        rel_img = set()
        while start_idx < end_idx:
            if end_idx == 100:
                end_idx -= 1
            for _ in range(end_idx):
                cols = st.columns(5)
                for col_num in range(5):
                    if start_idx < end_idx:
                        cols[col_num].image(img_results[start_idx], use_column_width='always', caption=img_results[start_idx])
                        # If using I + CC and RF, show a checkbox under images
                        if option == "Intensity + Color-Code" and use_rf:
                            checked = cols[col_num].checkbox('Relevant', key=img_results[start_idx])
                            if checked:
                                st.session_state.relevant_imgs.add(img_results[start_idx])
                            if img_results[start_idx] in st.session_state.relevant_imgs and not checked:
                                st.session_state.relevant_imgs.remove(img_results[start_idx])
                    start_idx += 1
             



