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
Each histogram comparison is calculated using the Manhattan Distance formula as follows:

![Manhattan Distance formula](https://i.imgur.com/MQMUdVe.png)

Where $H_i(j)$
