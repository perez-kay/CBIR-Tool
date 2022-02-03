import streamlit as st
import cbir_methods, paginator, json

with open('intensity_data.json') as f:
    intensity_data = json.load(f)

with open('color_code_data.json') as f:
    color_code_data = json.load(f)

st.session_state.intensity = intensity_data
st.session_state.color_code = color_code_data

st.set_page_config(layout='wide', page_title='CBIR Tool')

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

# Display these items in the left column
with left_col:
    # Select an image and display it. Displays image 1 by default
    img_num = st.number_input("Select an image by typing a number between 1 - 100", min_value=1, max_value=100, step=1)
    img_path = get_image_path(img_num)
    st.image(image=(img_path), use_column_width='always')

    # Set up the select box for the color codes
    methods = ['-', "Intensity", "Color-Code"]
    option = st.selectbox('Choose a method', methods)

    # Set up the run button
    run_checked = st.button("Retrieve Images")

# Display these items in the right columm
with st.container():
    # If the button has been pressed
    if run_checked:
        if option == '-':
            with left_col:
                st.error("Please select a method first.")
        else:
            # Fetch results based on mode chosen
            if option == "Intensity":
                with st.spinner('Fetching your results...'):
                    #results = cbir_methods.get_distance(img_path, cbir_methods.calculate_intensity)
                    results = st.session_state.intensity[img_path]
            if option == "Color-Code":
                with st.spinner('Fetching your results...'):
                    #results = cbir_methods.get_distance(img_path, cbir_methods.calculate_color_code)
                    results = st.session_state.color_code[img_path]
            # Update session state so it remembers results
            st.session_state.results = results

    # If the results exist
    if st.session_state.results != -1:
        #Get the image paths for the results     
        img_results = [path for distance, path in st.session_state.results]
        # Create paginator to display results pages
        #img_iter = paginator.paginator('Retrieval Results', img_results, items_per_page=20, on_sidebar=False)
        #indicies, imgs = map(list, zip(*img_iter))
        #st.image(imgs, width=150, caption=imgs)

        # from itertools import cycle
        #while i < len(img_results):
        # cols = cycle(st.columns(5))
        # for idx, img_results in enumerate(img_results):
        #     next(cols).image(img_results, width=150, caption=img_results)

        i = 0
        while i < len(img_results):
            for _ in range(len(img_results)):
                cols = st.columns(5)
                for col_num in range(5):
                    if i < len(img_results):
                        cols[col_num].image(img_results[i], width=150, caption=img_results[i])
                        cols[col_num].checkbox('Relevant', key=img_results[i])
                    i += 1

        # Display image results
             



