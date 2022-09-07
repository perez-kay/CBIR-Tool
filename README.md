# Content-Based Image Retrieval Tool
## Project Description
The Content-Based Image Retrieval tool uses two different color histogram comparison methods to retrieve similar images based on a query image. 
### Intensity Method
The Intesity method transforms each 24-bit RGB pixel value into an 8-bit value using the following formula:

![equation](https://latex.codecogs.com/svg.image?I&space;=&space;0.299R&space;&plus;&space;0.587G&space;&plus;&space;0.114B)


The histogram bins selected for this method are listed as follows:

![equation](https://latex.codecogs.com/svg.image?H_1:&space;I&space;\epsilon&space;[0,10\);&space;H_2:&space;I&space;\epsilon&space;[10,20\);&space;H_3:&space;I&space;\epsilon&space;[20,30\)&space;...&space;H_25:&space;I&space;\epsilon&space;[240,&space;255];)

