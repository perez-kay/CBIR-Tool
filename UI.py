import streamlit as st
from PIL import Image
import cbir_methods, paginator

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
st.write("Welcome to the CBIR Tool! To view the images in the database, type a number into the box below. \
         Once you've selected an image, use the drop down menu to choose a CBIR method. \
         Then click \'Retrieve Images\' to retrieve images based on the method you chose. \
         Your retrieval results will be displayed to the right.")

# Create 2 columns 
left_col, right_col = st.columns(2)

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
with right_col:
    # If the button has been pressed
    if run_checked:
        if option == '-':
            with left_col:
                st.error("Please select a method first.")
        else:
            # Fetch results based on mode chosen
            if option == "Intensity":
                with st.spinner('Fetching your results...'):
                    results = cbir_methods.get_distance(img_path, cbir_methods.calculate_intensity)
            
            if option == "Color-Code":
                with st.spinner('Fetching your results...'):
                    results = cbir_methods.get_distance(img_path, cbir_methods.calculate_color_code)
            
            # Update session state so it remembers results
            st.session_state.results = results

    # If the results exist
    if st.session_state.results:
        #Get the image paths for the results     
        img_results = [path for distance, path in st.session_state.results]

        # Create paginator to display results pages
        img_iter = paginator.paginator('Retrieval Results', img_results, items_per_page=20, on_sidebar=False)
        indicies, imgs = map(list, zip(*img_iter))

        # Display image results
        st.image(imgs, width=150, caption=imgs)  



