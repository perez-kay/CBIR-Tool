# Content-Based Image Retrieval Tool
## Project Description
The Content-Based Image Retrieval tool uses two different color histogram comparison methods to retrieve similar images based on a query image. 
### Intensity Method
The Intesity method transforms each 24-bit RGB pixel value into an 8-bit value using the following formula:
```math
I = 0.299R + 0.587G + 0.114B
```
The histogram bins selected for this method are listed as follows:
```math
H_1: I \epsilon [0,10); H_2: I \epsilon [10,20); H_3: I \epsilon [20,30) ... H_25: I \epsilon [240, 255];
```

