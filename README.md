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

## 2.3 What is HSV?

HSV is a color profile. It is located like RGB, but it is included in the names Hue, Saturation and Value. Color values are entered between 0 and 255. In image processing, HSV values are included as upper and lower HSV and represent a range of colors. Parts other than this color range are not taken into account and color recognition is done accordingly. 

    18.	# Initalize first values of HSV. 
    19.	# This will be default vairables on startup.
    20.	lh = 10
    21.	ls = 90
    22.	lv = 151
    23.	uh = 40
    24.	us = 161
    25.	uv = 255


## 2.4 Serial Communication:

In this project, Raspberry Pi and Arduino were used together. The position definition is made by processing the image taken in the global code of the project and the determined position is sent to Arduino. To achieve this, linear Serial communication must be used. To start the serial communication, our serial name is set on the 28th line and “ser” is used as a variable. In addition, Arduino's connection type, Baud value and timeout value are also written on the same line.

The Serial.flush() command should be used to wait for the ongoing serial communication to complete.

    26.	# Starting serial communication between Arduino and RPi. 
    27.	# 9600 Baud with 1ms timeout is used.
    28.	ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
    29.	ser.flush()

## 2.5 Flask Programming

The program used must be completely remotely controllable. To do this, a local connection network had to be established. With the Flask library, it is possible to write HTML-based web applications. For this reason, by defining the Flask library, the program was divided into two different parts as frontend (HTML Code) and backend (Python code). In this library, which allows control between localhost, ie 0.0.0.0 network, and devices connected to the same internet, various functions have been prepared for remote data acquisition.

    30.	# Importing Flask Libraries to Server Side Programming
    31.	from flask import Flask, Response
    32.	from flask import render_template
    33.	from flask import request, redirect

After defining the Flask libraries, it is necessary to create a new Flask application. The Flask application used in this program is identified by the app name. In the “App” application, the homepage is primarily defined. With the "render_template()" command used here, the index.html file written in HTML language in the Raspberry Pi is called. Thanks to this, when logging in to the defined IP address, the index.html page will be seen first.

The @app.route command shows how the defined function can be called. The data contained in it also has an equivalent in the HTML frontend code and allows two-way communication.

    34.	# Defining app name of our Flask. We use app for easier use. 
    35.	# You can change it.
    36.	app = Flask(__name__)
    37.	# Main Page of the program. It is stored in templates folder. 
    38.	@app.route('/')
    39.	def index():
    40.	return render_template("index.html")

After the homepage is defined, the response functions of the two images to be published in the web application are written. With these functions, images are instantly transferred to the website within the limits we set. After opening this port, it is added to the HTML section where it is desired to be in the design of the site. It should be noted that the backend in the Python part does not affect the appearance of the site, so the order of the data gateways to be written is not important.

Two different gateways should be created to run two different visual sources smoothly in data migrations. If it is tried to be done through a single pass, the image will flicker. The flickering problem is a problem that occurs when the binary and normal image are sent sequentially in the same location.

For this reason, two different functions, video_feed1() and video_feed2(), have been defined in the program.

    41.	# Streaming Processed Image and BW Binary as Video Feed.
    42.	@app.route('/video_feed1')
    43.	def video_feed1():
    44.	return Response(main(), mimetype='multipart/x-mixed-replace; boundary=frame1')
    45.	@app.route('/video_feed2')
    46.	def video_feed2():
    47.	return Response(main(), mimetype='multipart/x-mixed-replace; boundary=frame2')

## 2.6 Handling HSV Values from User

In this project, a system has been designed in which HSV values can be obtained from the user continuously. HTTP communication protocol is used with the benefit of Flask software. The POST method was used together with the function written in the backend, and the data received from the user was written instead of the HSV values, thanks to the global variables. The reason for using np.float32() is that, as can be seen below, most functions in computer vision systems use float32 and in some cases uint8.
After the function is finished, the system redirects itself to the homepage with the redirect('/') command.

    48.	# Input form for changing HSV values via Webpage.
    49.	@app.route('/handle_data', methods=['POST'])
    50.	def handle_data():
    51.	global lh
    52.	global ls
    53.	global lv
    54.	global uh
    55.	global us
    56.	global uv
    57.	lh = np.float32(request.form['lH'])
    58.	ls = np.float32(request.form['lS'])
    59.	lv = np.float32(request.form['lV'])
    60.	uh = np.float32(request.form['uH'])
    61.	us = np.float32(request.form['uS'])
    62.	uv = np.float32(request.form['uV'])
    63.	return redirect('/')

The program also allows the user to select the desired resolution. Since the entire algorithm is written on variables and the formulas created by these variables instead of fixed numbers, the end user can resize the system losslessly and instantly by entering resolutions such as 1080p/480p/360p via the web application. The main purpose of introducing this feature is to decrease the frames per second (FPS) as the resolution increases while working in computer vision. This decrease, which is especially effective in the use of Median Filter, can be solved by changing the resolution.

At the same time, it is aimed to provide as much control to the user as possible. While using the application, the user is requested to use it with the usage habits that he/she has discovered, not through the predetermined demo.

As its working principle, it replaces the data it receives from the site with the predefined res with the POST method, and it can do this unlimitedly as new data is sent. Unlike HSV entries, this data uses int32 encoding.

    64.	# Resolution input from Webpage
    65.	@app.route('/resolution', methods = ['POST'])
    66.	def resolution():
    67.	global res
    68.	res = np.int32(request.form['RES'])
    69.	return redirect('/')

In addition, one of the efforts to improve the recognition algorithm in the program is the Tolerance setting. This opportunity is also given to the user. With the tolerance setting, the user can select the minimum object diameter that the robot will detect in mixed images, except for the extra filters. With this feature, the color dirt that can affect the environment can be prevented by reducing the perception diameter of the robot.

The working principle is the same as the resolution setting.

    70.	# Tolerance input from Webpage
    71.	@app.route('/tolerance', methods = ['POST'])
    72.	def tolerance():
    73.	global MIN_RAD
    74.	MIN_RAD = np.int32(request.form['TOL'])
    75.	return redirect('/')

There are multiple buttons in the frontend of the program. These can change predefined mode selections, filter preference and Arduino Serial communication boolean response. In the backend code, it is explained how the data coming from these buttons will work. As a working principle, the buttons send the value on them as a string. In addition, the appropriate comparison and boolean code is written in the backend code and operations are performed according to different possibilities.

First, the function that enables the start of data communication was written to the Arduino. The default value of this function is defined as False. Thus, data flow is not provided to the Arduino when the user does not want it. However, this function has been added to prevent the Arduino from starting unintentionally.

    76.	# Button script for start and stop for Arduino Data.
    77.	@app.route('/button2', methods = ['POST'])
    78.	def button2():
    79.	global arddata
    80.	if request.method == 'POST':
    81.  		if request.form.get('senddata') == 'START':
    82.       	arddata = True
    83.   	if request.form.get('stopdata') == 'STOP':
    84.	    	arddata = False
    85.	return redirect('/')

At second, the function written for filter selection can be seen. This function, which is a simple true/false loop, replaces a boolean declaration to be used later in the code. In addition, under the filter selection, a POST method is defined that gives the value of the median filter, like the tolerance data above. Gaussian blur is left as default with performance consideration for the filter preference.

    82.	filter_sel = False
    83.	median_val = 5
    84.	# Filter Selection
    85.	@app.route('/buttonfilter', methods = ['POST'])
    86.	def buttonfilter():
    87.	global filter_sel
    88.	if request.method == 'POST':
    89.	if request.form.get('medianfilter') == 'MEDIAN':
    90.	filter_sel = True
    91.	if request.form.get('gaussfilter') == 'GAUSS':
    92.	filter_sel = False
    93.	return redirect('/')
    94.	# Take Median Value from user
    95.	@app.route('/medianval', methods = ['POST'])
    96.	def medianval():
    97.	global median_val
    98.	median_val = np.uint32(request.form['MED'])
    99.	return redirect('/')


## 2.7 Main Code

The main part of the code is devoted to image acquisition and processing. Position analysis and interface drawings that can create density in the code are written as separate functions. With the cap.read() command, the image is continuously saved into a variable as data.
The resolution that can be changed by the user in the web application is provided here with the imutils.resize() command. In this command, only the width is set and the height is adjusted with the fixed formula below.

    100.	# ---------------Capture Camera Frame-----------------
    101.	frame = cap.read()

The resolution that can be changed by the user in the web application is provided here with the imutils.resize() command. In this command, only the width is set and the height is adjusted with the 16:9 ratio.

    102.	frame = imutils.resize(frame, width = res)

Since the camera used by Raspberry Pi broadcasts the image rotated 180 degrees, the imutils.rotate_bound() command was used to resolve this error.

    103.	frame = imutils.rotate_bound(frame, 180)
    104.	img=frame

After these changes are made, the converted frame is re-saved with the name of the img variable to avoid confusion.
After these processes are done, a picture filter is applied to reduce the noise on the first image and improve color recognition. In this section, two different filters are left to the user's preference.

Gaussian Blur is a method used to soften the image. In this method, Gaussian kernel is used instead of box filter. This is done with the cv.GaussianBlur() function. We must specify the width and height of the core, which must be positive and odd. We should also specify the standard deviation in the X and Y directions, sigmaX and sigmaY, respectively. If only sigmaX is specified, sigmaY is considered the same as sigmaX. If both are given as zero, it is calculated from the kernel size. Gaussian blur is very effective at removing Gaussian noise from an image.

    105.	if filter_sel == False:
    106.	   img_filter = cv2.GaussianBlur(img.copy(), (3, 3), 0)

The medianBlur() command takes the median of all pixels under the kernel area and replaces the center with these median values. It is very effective against the salt and pepper noise in this image. It has been added to clean up small dotted noises that occur in code and be more effective in high light.

    107.	if filter_sel == True:
    108.	   medval=(np.uint8(median_val))
    109.	   img_filter = cv2.medianBlur(img.copy(), medval)

 
The color format of the image taken from the camera is RGB. However, the color recognition system in the program is made with HSV color code. For this reason, the image from the camera should be converted to HSV format. To do this, the cvtColor() command is used.

    110.	# Convert image from BGR to HSV
    111.	hsv = cv2.cvtColor(img_filter, cv2.COLOR_BGR2HSV)

After converting to HSV code, HSV values are stored in two separate arrays, upper and lower. Here the system works with float32. Since the program receives data from outside, the data type is redefined as float32 in the array.

    112.	l_blue = np.array([lh,ls,lv],dtype=np.float32)
    113.	u_blue = np.array([uh,us,uv],dtype=np.float32)

After the colors are placed in the array, the HSV image is processed with the specified color ranges with the inRange() command. With this command, the colors in the color range are redrawn as white and the other colors as black. Thus, the bitmap version of the image is extracted.

    114.	# Set pixels to white if in color range, others to black (binary bitmap)
    115.	img_binary = cv2.inRange(hsv, l_blue, u_blue)

To make the bitmap more distinct, the white areas are enlarged a little more than normal with the dilate() command. Thus, the stability of the recognition algorithm is increased.

    116.	# Dilate image to make white blobs larger
    117.	img_binary = cv2.dilate(img_binary, None, iterations = 1)

By making a copy of the bitmap image, the contour of the white areas in it is extracted and calculated as an array. If any white region is defined, the size of this array will be greater than 0.

    118.	# Find center of object using contours instead of blob detection.
    119.	img_contours = img_binary.copy()
    120.	contours = cv2.findContours(img_contours, cv2.RETR_EXTERNAL, \
    121.	cv2.CHAIN_APPROX_SIMPLE)[-2]

In an array with more than 0, that is, the recognized white regions, the largest area is calculated with the max() command. Here, each contour is scanned one by one and the contourArena() command is accepted as the key, and the largest area is found.

    122.	if len(contours) != 0:
    123.	cmax = max(contours, key=cv2.contourArea)
    124.	xmax,ymax,w,h=cv2.boundingRect(cmax)

The x, y and w, h dimensions of the square surrounding the found region are obtained with the boundingRect() command. If it needs to be shown with a graph, these values are represented as follows.

 ![enter image description here](https://i.ibb.co/Jmbyrb0/Resim9.png)
 
The tolerance value received from the user in the web application comes into play here. The tolerance determined by the person determines the smallest diameter that the white areas can be noticed by the system. If the diameter detected in the program is smaller than this, the program continues to run as if it did not see any object. The main purpose of this is to prevent small color mixing and reflections that are not balls around, as well as color mixing in the distance.

    125.	# If there no blob larger than tolerance return zero.
    126.	if xmax+w < MIN_RAD*2:
    127.	xmax=0
    128.	ymax=0
    129.	w=0
    130.	h=0
    131.	# If there no blob return zero.
    132.	else:
    133.	ymax = 0
    134.	xmax = 0
    135.	w=0
    136.	h=0

After the time calculations for FPS are made, the grid and data additions to be made on the images taken with the draw_overlays() command are prepared as an interface. In addition, the data we process is first converted to a jpeg file and then to bytes and sent to the website via Flask.

    137.	arr_dur[0]=time.time() - start_t0
    138.	start_t1=time.time()
    139.	arr_dur[1]=time.time() - start_t1
    140.	start_t2=time.time()    
    141.	if cv2.waitKey(1) & 0xFF == ord('q'):
    142.	break    
    143.	# draw overlays to image
    144.	cv2_im = draw_overlays(img, xmax, ymax,w,h, centermax, arr_dur)    
    145.	#Flask streaming
    146.	# encode image to jpeg.
    147.	ret, jpeg = cv2.imencode('.jpg', cv2_im)
    148.	# encode jpeg to bytes.
    149.	pic = jpeg.tobytes()    
    150.	#Flask streaming
    151.	yield (b'--frame1\r\n'
    152.	       b'Content-Type: image/jpeg\r\n\r\n' + pic + b'\r\n\r\n')    
    153.	# encode image to jpeg.
    154.	ret, binary = cv2.imencode('.jpg', img_binary)
    155.	# encode jpeg to bytes.
    156.	pic2 = binary.tobytes()    
    157.	#Flask streaming
    158.	yield (b'--frame2\r\n'
    159.	       b'Content-Type: image/jpeg\r\n\r\n' + pic2 + b'\r\n\r\n')    
    160.	arr_dur[2]=time.time() - start_t2
    161.	fps = round(1.0 / (time.time() - start_time),1)    
    162.	cap.release()
    163.	cv2.destroyAllWindows()
    
    ## 2.8 Segmentation

In this section, segmentation calculations in the program are included. The segmentation part is done with two different functions. These are Position and Segmentation functions. The position function calculates the position of the greatest detected color intensity by giving the result of probabilities. To do this, the height is divided into 5 parts vertically and 2 parts horizontally, and a total of 15 different regions are defined.

In order not to be affected by the user's new resolution definition in the position function, all operations are written using mathematical formulas. With the Shape() function, the adjusted height and width of the image are taken and this value is compared with the midpoint in the square coordinate system described above.

The vertical and horizontal midpoints of the defined rectangle are compared with the vertical and horizontal region boundaries to find the midpoint of the noticed color space. Accordingly, the midpoint of the rectangle with x, y, w, h can be expressed with the formula below.

![enter image description here](https://i.ibb.co/yqcTw8P/Resim10.png)

    164.	Position algorithm returns psoition value as integer.
    165.	# It decides its position by comparing center of the blob
    166.	# and 15 partition of the image
    167.	# centerofblob = (x + w/2, y + h/2)        
    168.	def position(cv2_im,x,y,w,h):
    
    169.	# 16 statement compiled here. 15 of them returns position 1-15 
    170.	# and where there is no detection program sends arduino 
    171.	# 16 because 0 is not suitable for the parseInt(); command
    172.	# due it also may give 0 when there is no data.
    
    173.	# --------------------  Position between 1 to 5 --------------------
    174.	height, width, channels = cv2_im.shape
    175.	if (1/5)*width > x+w/2 > 0 and (1/3 * height) > y+h/2 > 0:
    176.	position = 1
    177.	serialsend(position)
    178.	return position
    
    179.	if (2/5)*width > x+w/2 > (1/5)*width and (1/3 * height) >y+h/2> 0:
    180.	position = 2
    181.	serialsend(position)
    182.	return position
    
    183.	if (3/5)*width > x+w/2 > (2/5)*width and (1/3 * height) > y+h/2 > 0:
    184.	position = 3
    185.	serialsend(position)
    186.	return position
    
    187.	if (4/5)*width > x+w/2> (3/5)*width and (1/3 * height) > y+h/2 > 0:
    188.	position = 4
    189.	serialsend(position)
    190.	return position
    
    191.	if width > x+w/2 > (4/5)*width and (1/3 * height) > y+h/2 > 0:
    192.	position = 5
    193.	serialsend(position)
    194.	return position
    
    195.	# --------------------  Position between 6 to 10 --------------------
    196.	if (1/5)*width > x+w/2 > 0 and (2/3 * height) > y+h/2 > (1/3 * height):
    197.	position = 6
    198.	serialsend(position)
    199.	return position
    
    200.	if (2/5)*width > x+w/2 > (1/5)*width and (2/3 * height) > y+h/2 > (1/3 * height):
    201.	position = 7
    202.	serialsend(position)
    203.	return position
    
    204.	if (3/5)*width > x+w/2 > (2/5)*width and (2/3 * height) > y+h/2 > (1/3 * height):
    205.	position = 8
    206.	serialsend(position)
    207.	return position
    
    208.	if (4/5)*width > x+w/2 > (3/5)*width and (2/3 * height) > y+h/2 > (1/3 * height):
    209.	position = 9
    210.	serialsend(position)
    211.	return position
    
    212.	if width > x+w/2 > (4/5)*width and (2/3 * height) > y+h/2 > (1/3 * height):
    213.	position = 10
    214.	serialsend(position)
    215.	return position
    
    216.	# --------------------  Position between 11 to 15 --------------------
    217.	if (1/5)*width > x+w/2 > 0 and (height) > y+h/2 > (2/3 * height):
    218.	position = 11
    219.	serialsend(position)
    220.	return position
    
    
    221.	if (2/5)*width > x+w/2 > (1/5)*width and (height) > y+h/2 > (2/3 * height):
    222.	position = 12
    223.	serialsend(position)
    224.	return position
    
    
    225.	if (3/5)*width > x+w/2 > (2/5)*width and (height) > y+h/2 > (2/3 * height):
    226.	position = 13
    227.	serialsend(position)
    228.	return position
    
    
    229.	if (4/5)*width > x+w/2 > (3/5)*width and (height) > y+h/2 > (2/3 * height):
    230.	position = 14
    231.	serialsend(position)
    232.	return position
    
    
    233.	if width > x+w/2 > (4/5)*width and (height) > y+h/2 > (2/3 * height):
    234.	position = 15
    235.	serialsend(position)
    236.	return position
    164.	Position algorithm returns psoition value as integer.
    165.	# It decides its position by comparing center of the blob
    166.	# and 15 partition of the image
    167.	# centerofblob = (x + w/2, y + h/2)        
    168.	def position(cv2_im,x,y,w,h):
    
    169.	# 16 statement compiled here. 15 of them returns position 1-15 
    170.	# and where there is no detection program sends arduino 
    171.	# 16 because 0 is not suitable for the parseInt(); command
    172.	# due it also may give 0 when there is no data.
    
    173.	# --------------------  Position between 1 to 5 --------------------
    174.	height, width, channels = cv2_im.shape
    175.	if (1/5)*width > x+w/2 > 0 and (1/3 * height) > y+h/2 > 0:
    176.	position = 1
    177.	serialsend(position)
    178.	return position
    
    179.	if (2/5)*width > x+w/2 > (1/5)*width and (1/3 * height) >y+h/2> 0:
    180.	position = 2
    181.	serialsend(position)
    182.	return position
    
    183.	if (3/5)*width > x+w/2 > (2/5)*width and (1/3 * height) > y+h/2 > 0:
    184.	position = 3
    185.	serialsend(position)
    186.	return position
    
    187.	if (4/5)*width > x+w/2> (3/5)*width and (1/3 * height) > y+h/2 > 0:
    188.	position = 4
    189.	serialsend(position)
    190.	return position
    
    191.	if width > x+w/2 > (4/5)*width and (1/3 * height) > y+h/2 > 0:
    192.	position = 5
    193.	serialsend(position)
    194.	return position
    
    195.	# --------------------  Position between 6 to 10 --------------------
    196.	if (1/5)*width > x+w/2 > 0 and (2/3 * height) > y+h/2 > (1/3 * height):
    197.	position = 6
    198.	serialsend(position)
    199.	return position
    
    200.	if (2/5)*width > x+w/2 > (1/5)*width and (2/3 * height) > y+h/2 > (1/3 * height):
    201.	position = 7
    202.	serialsend(position)
    203.	return position
    
    204.	if (3/5)*width > x+w/2 > (2/5)*width and (2/3 * height) > y+h/2 > (1/3 * height):
    205.	position = 8
    206.	serialsend(position)
    207.	return position
    
    208.	if (4/5)*width > x+w/2 > (3/5)*width and (2/3 * height) > y+h/2 > (1/3 * height):
    209.	position = 9
    210.	serialsend(position)
    211.	return position
    
    212.	if width > x+w/2 > (4/5)*width and (2/3 * height) > y+h/2 > (1/3 * height):
    213.	position = 10
    214.	serialsend(position)
    215.	return position
    
    216.	# --------------------  Position between 11 to 15 --------------------
    217.	if (1/5)*width > x+w/2 > 0 and (height) > y+h/2 > (2/3 * height):
    218.	position = 11
    219.	serialsend(position)
    220.	return position
    
    
    221.	if (2/5)*width > x+w/2 > (1/5)*width and (height) > y+h/2 > (2/3 * height):
    222.	position = 12
    223.	serialsend(position)
    224.	return position
    
    
    225.	if (3/5)*width > x+w/2 > (2/5)*width and (height) > y+h/2 > (2/3 * height):
    226.	position = 13
    227.	serialsend(position)
    228.	return position
    
    
    229.	if (4/5)*width > x+w/2 > (3/5)*width and (height) > y+h/2 > (2/3 * height):
    230.	position = 14
    231.	serialsend(position)
    232.	return position
    
    
    233.	if width > x+w/2 > (4/5)*width and (height) > y+h/2 > (2/3 * height):
    234.	position = 15
    235.	serialsend(position)
    236.	return position

