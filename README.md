# Global Control for Tennis Ball Collector

**Introductıon**

For the Global Control we aimed to develop algorithm to detect balls in specific distance to create decide which way robot will go. After research we decided to use Raspberry Pi and Open CV Libraries to achieve this goal.

## 1. What is Raspberry Pi?

Raspberry Pi is a “pocket computer” which can be used with plugging a keyboard and monitor. It is more developed control card than Arduino and other cards. It can be used both as computer and processor. It supports various languages and do complex process faster. It is mostly referred as computer and in Color Detection we need faster process. Raspberry is more useful than computers because it can be stored in robot with its size.

  
Raspberry Pi is more powerful and effective than other cards. Its processor size can read live feed from camera; calculate and decide the output much faster than all other cards. Also due to it supports most of the languages we used Phyton for using OpenCV Librariesmostefficientway.

Raspberry Pi is more powerful and effective than other cards. Its processor size can read live feed from camera; calculate and decide the output much faster than all other cards. Also due to it supports most of the languages we used Phyton for using OpenCV Librariesmostefficientway.

## 2. Components used with Global Control 
**2. 1. Camera**

With the Raspberry Pi we use Logitech C525 Camera for live feed. We also obtained Raspberry Pi Camera, but 3rd party cameras are much efficient from many ways. But the main reason is that Logitech Camera has more Field of view than Raspberrycamera

This camera works with USB port and user decides the resolution of the camera in program. We created global variable for camera resolution and when user changes it will affect all code and continue with zero problem. Image Segmentation part also uses these variables
<![endif]-->

**2. 2. Differences with Raspberry Camera and C525**
| Features| Raspberry Camera |Logitech C525|
| :---: | :---: | :---: |
| **Connection**| CSI connector| USB Type-A USB 2.0|
| **Field of View**| 41.41 +/- 0.11 degrees| 62 degrees|
| **FPS**| 1080p30, 720p60 and 480p60/90|720p60|
| **Resolution**| 5 Megapixels| 8 Megapixels|
| | ![C525](https://i.ibb.co/3mvrW0S/Resim2-removebg-preview.png)| ![Raspberry Pi Camera](https://i.ibb.co/TMRxbWs/Resim1-removebg-preview.png)

## 3 Power Supply and External Control

Raspberry Pi can be charged easily with USB Type C cable. Due with that it can be connected to its power cable to ground electricity or it can be used with Power Bank or External Electric resource. External power use will be needed for our project because our robot will be on mobile while operating and collecting balls. Because of the robot will used as remote we should use and control it from remote also.

While using with this, Raspberry do not need extra keyboard or monitor to use so. With its own ability it can be used from remote with VNC Server. VNC server is built in feature in Raspberry Pi and with this it can easily via computer or mobile phone. Only needed feature is that both Raspberry Pi and computer should connect to same network.

## 4 Open CV Libraries

OpenCV is a open source computer vision library mainly developed for computer vision calculations in real time. It is originally developed by Intel. It is a multi-platform open source and free to use library under the Apache License. It also features GPU acceleration with real-time calculations.

Computer Visionary in this project works with color segmentation. OpenCV applies mask to color range and it gives output of desired object. It can also improvise as object detecting by machine learning but, in this project, this is not needed.

Camera sends image as pixels. Pixels are squares with color attached in. When we apply correct color order with pixels it will form image. Here is a example of different variations of Pixel density in one picture:

![enter image description here](https://i.ibb.co/pQJsFhH/Resim3.png)
<![endif]-->

Computer Visionary works with calculation of the pixels in one image. In color segmentation, user enters threshold of color and the program detect pixels with that color range. Also, Computer Vision with machine learning works withs same way. Computer creates algorithm with given example inputs and in the end, it develops detect system based on similarity.

## 5 Early Adaptations to Detect Balls

 **5.1 Seeing Balls from upper camera – declined.**

In early implementations Global part of the project was excluded from main robot and planned to communicate from outside with WIFI. In theory, camera will be on top with fixed tripod and will see all the area with balls.

![enter image description here](https://i.ibb.co/8Y8mwhm/Resim4.png)

With the X and Y coordinates, program will recalculate it as the coordinates for robot. This design cancelled in theory phase due to many reasons. Main reason was it needs very much effort to build this system anywhere and also robot must be work in every situation. With this design outdoor implementation will be not available and we think more effective way can be done.

**5.2  Work Inside of the Robot.**

In second way, all the global system will be held on the robot and it will be remote system completely. This will be more effective to be “start only” system but it brings new challenges. Computer Visionary should work with 3 dimension and should know area with most ball with less vision.

![enter image description here](https://i.ibb.co/gPymJcm/Resim5.jpg)

# **Chapter 2**

The purpose of the global control part is to separate the tennis balls that the robot sees around it from the environment, to recognize it with the help of OpenCV and to transmit the position it has determined accordingly to the Arduino. In doing so, the code must be fully accessible over the internet.

In this report all of the explanations are made in order of apperance in the code.

In the first stage of the report, the Python code, which is the backend part of the software, is explained.


## 2.1 Brief Explanations About Libraries

The software includes many functions and calculations. Using these calculations in a single program both tires the processor and complicates the program. To solve this, libraries are used in the software. OpenCV is an open source software library used in Computer Vision. OpenCV is supported by the Python language and also receives constant updates. With the libraries in it, it is possible to take the image from the camera, convert it to matrices and process it.

    1.	#importing libraries
    2.	#------------------OPENCV-----------------------
    3.	import cv2
    4.	#---------------NUMPY AND SERIAL----------------
    5.	import numpy as np
    6.	import serial
    7.	#---------------OTHER LIBRARIES-----------------
    8.	import time
    9.	from datetime import datetime
    10.	from threading import Thread
    11.	#---------------IMUTILS VIDEO LIBRARY-----------
    12.	from imutils.video import VideoStream
    13.	import imutils

Along with OpenCV, "numpy" is used for mathematical computation and matrix manipulation. This library allows to perform complex mathematical calculations instantly. In addition to libraries that perform time calculations, Imutils is preferred instead of OpenCV library for advanced video processing. Imutils is an addon for OpenCV which make basic image processing functions such as translation, rotation, resizing, skeletonization, displaying Matplotlib images, sorting contours, detecting edges etc. We use Imutils to capture camera image, and also resize and rotate it.

    14.	# If the Raspberry Pi camera will not be used, 
    15.	# use the src=0 command below. 
    16.	# So you can also use USB cameras.
    
    17.	cap = VideoStream(usePiCamera = 1).start()

## 2.2 Detecting the image :

Color recognition system is used to detect the tennis balls in the image. The color recognition system uses HSV values to process the image by abstracting it out of the color ranges we have defined, and accordingly marks the parts that need to be recognized with the masking method. Raspberry Pi Camera started and defined as “cap” to use in code with that variable. 

![enter image description here](https://i.ibb.co/f4TjZLD/Resim8.png)
