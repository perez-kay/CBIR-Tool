# Content-Based Image Retrieval Tool
## Project Description
The Content-Based Image Retrieval tool uses two different color histogram comparison methods to retrieve similar images based on a query image. 
### Intensity Method
The Intesity method transforms each 24-bit RGB pixel value into an 8-bit value using the following formula:

![equation](https://latex.codecogs.com/svg.image?I&space;=&space;0.299R&space;&plus;&space;0.587G&space;&plus;&space;0.114B)


The histogram bins selected for this method are listed as follows:

![equation](https://latex.codecogs.com/svg.image?H_1:&space;I&space;\epsilon&space;[0,10\);&space;H_2:&space;I&space;\epsilon&space;[10,20\);&space;H_3:&space;I&space;\epsilon&space;[20,30\)&space;...&space;H_{25}:&space;I&space;\epsilon&space;[240,&space;255];)

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