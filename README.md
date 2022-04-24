# CVSeniorProject
## Computer Vision Senior Project
#### by [Russell Schiesser](https://github.com/Schiesh) and [Garrett Sparks](https://github.com/CheekCheeks)
---
## Abstract
We decided to develop a solution to finding the locations of empty parking spots by analyzing an aerial picture or video of a parking lot through the means of artificial intelligence programming, specifically through computer vision. The characteristics for our solution shall include highlighting full parking spots as red and empty spots as green along with determining how many spots are available for guests and staff. Depending on our decision of input, whether it will be an image or video, we will provide a more extensive user interface when it comes to passing in multiple images of parking lots. We may find analyzing a video frame by frame for empty spots to be more intuitive to a real world problem than scanning through random parking lots. The client should also be able to easily configure the program for their parking lot. We are going to achieve this through a GUI and allow the user access to easy to use tools for configuration. For the means of developing the A.I. program, we determined that we should use Python as our main programming language along with using the open source computer vision library, OpenCV. We also determined that we will create a user interface by using Python's Tkinter library.

## Requirements
* Provide means for the user to map out their parking lot
    * Provide tools such as lines and rectangles to determine what are parking spots
* Determining which parking spots are full or empty
    * Display outline of parking spot green if empty
    * Display outline of parking spot red if full

## Setup
Either create a new environment for python by using Anaconda or by any other means. By using the ***pip*** command in either your environment console through Anaconda or in your main console where the path to python on your machine is set to, download the required dependencies below. The numpy library is also required for the program to work and it comes pachaged with ***opencv-python***. After you have an enviornment with the dependencies installed you can then run our program ***main.py*** on your system. There are instruction on the GUI to help with using the software.
## Dependencies
- OpenCV
```
pip intall opencv-Python
```
- cvzone
```
pip install cvzone
```


## Our Progress
### **Example 1**
![example](/resources/example.png)
