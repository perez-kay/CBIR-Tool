# Content-Based Image Retrieval Tool

## Project Description
The Content-Based Image Retrieval tool uses two different color histogram comparison methods to retrieve similar images based on a query image. 

## Demonstration
The app is able for demo use at: https://share.streamlit.io/perez-kay/cbir-tool/UI.py. Due to some necessary pre-calculations, the app may take a minute to load.

### How To Use
**Intensity or Color-Code (NO Relevance Feedback)**

1. Select an image by choosing a number between 1 - 100
    1. You can type this number into the text box or use the “+” and “-” buttons to
increment/decrement the number
2. Choose a CBIR method using the drop down menu next to the image.
3. Click “Retrieve Images” and wait for the results to appear below the query image.
4. Use the “Next Page” and “Previous Page” to view different pages of results.

**Intensity + Color-Code (Relevance Feedback available)**
1. Select an image by choosing a number between 1 - 100
    1. You can type this number into the text box or use the “+” and “-” buttons to
increment/decrement the number
2. Select “Intensity + Color Code” as your method.
3. Click “Retrieve Images” and wait for the results to appear at the bottom
4. Use the “Next Page” and “Previous Page” to view different pages of results.
5. To use Relevance Feedback, click the “Use Relevance Feedback” checkbox. Checkboxes will
appear under each image to allow you to choose relevant images.
    1. If you choose a checkbox on a different page, you might notice that the
checkboxes on the previous page are unchecked. Don’t worry, the app will still
remember the images you chose. This is a quirk of Streamlit.
6. To see the new results after selecting your images, click the “Retrieve Images” button
again. Make sure the “Intensity + Color Code” is still selected in the drop down menu.
7. You can repeat this process as many times as you want for a single image.
    1. The app will remember which relevant images you chose for your query image
until you select a new query image or change the CBIR method to “Intensity” or
“Color Code”.

## How It Works

### Intensity Method
The Intesity method transforms each 24-bit RGB pixel value into an 8-bit value using the following formula:

$$I=0.299R+0.587G+0.114B$$ 


The histogram bins selected for this method are listed as follows:

$$H_1: I \epsilon [0,10); H_2: I \epsilon [10,20); H_3: I \epsilon [20,30); ... H_{25}: I \epsilon [240,255];$$


### Color-Code Method
The Color-Code  method transforms the 24-bit RBG pixel value into a 6-bit color code. This color code is composed of the most significant 2 bits of each color channel. This is illustrated in the following figure:

![Color-Code method illustration](https://i.imgur.com/bD55xHP.png)

For this method, there are 64 histogram bins, with H1: 000000, H2: 000001, H3: 000010, ... H64: 1111111

### Histogram Comparison
Each histogram comparison is calculated using the Manhattan Distance formula. Let $H_i(j)$ denote the number of pixels in the $j^{th}$ bin for the $i^{th}$ image. The difference between the $i^{th}$ image and the $k^{th}$ image can be given by the following metric:

![Manhattan Distance formula](https://i.imgur.com/MQMUdVe.png)

where $M_i*N_i$ is the number of pixels im image $i$, and $M_k\*N_k$ is the number of pixels im image $k$. For the set of images included in this project, all have the same dimensions. Thus, the division is omitted in this implementation.

### Intensity + Color-Code Method (With Relevance Feedback)
This method combines the values computed with the Intensity and Color-Code methods. A feature matrix is created, where the rows of the matrix represent each image, and the columns are each image's set of features. There are 25 Intensity features and 64 Color-Code features, making a total of 89 features for each image.

The feature matrix is normalized using the Gaussian Normalization formula, described as follows:
$$\nu_k = \frac{\nu_k - \mu_k}{\sigma_k}$$

where, for an image $k$, $\nu_k$ is the feature, $\mu_k$ is the average of $k$'s features, and $\sigma_k$ is the standard deviation of $k$'s features.

The Relevance Feedback implementation used is a simplification of the implementation outlined in [this](https://ieeexplore.ieee.org/document/718510) paper.