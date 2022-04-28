#importing libraries
#------------------OPENCV-----------------------
import cv2
#---------------NUMPY AND SERIAL----------------
import numpy as np
import serial
#---------------OTHER LIBRARIES-----------------
import time
from datetime import datetime
from threading import Thread
#---------------IMUTILS VIDEO LIBRARY-----------
from imutils.video import VideoStream
import imutils

# If the Raspberry Pi camera will not be used, 
# use the src=0 command below. 
# So you can also use USB cameras.

cap = VideoStream(usePiCamera = 1).start()

# Initalize first values of HSV. 
# This will be default vairables on startup.

lh = 10
ls = 90
lv = 151
uh = 40
us = 161
uv = 255

# Starting serial communication between Arduino and RPi. 
# 9600 Baud with 1ms timeout is used.
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
ser.flush()

# Define default variables of xmax, ymax and
# centermax to avoid error when there is no object.

xmax = 0
ymax = 0
centermax = 0

# Define default minimum radius to detect.
MIN_RAD = 0

# Define default resolution of frame to 720p. 
# Also, arddata (Arduino Data) is False 
# on default to prevent sending data while user dont want to.
res = 720
arddata = False

# Importing Flask Libraries to Server Side Programming
from flask import Flask, Response
from flask import render_template
from flask import request, redirect

# Defining app name of our Flask. We use app for easier use. 
# You can change it.
app = Flask(__name__)

# Main Page of the program. It is stored in templates folder. 
@app.route('/')
def index():
    return render_template("index.html")

# Streaming Processed Image and BW Binary as Video Feed.
@app.route('/video_feed1')
def video_feed1():
    return Response(main(),
                    mimetype='multipart/x-mixed-replace; boundary=frame1')

@app.route('/video_feed2')
def video_feed2():
    return Response(main(),
                    mimetype='multipart/x-mixed-replace; boundary=frame2')

# Input form for changing HSV values via Webpage.
@app.route('/handle_data', methods=['POST'])
def handle_data():
    global lh
    global ls
    global lv
    global uh
    global us
    global uv
    lh = np.float32(request.form['lH'])
    ls = np.float32(request.form['lS'])
    lv = np.float32(request.form['lV'])
    uh = np.float32(request.form['uH'])
    us = np.float32(request.form['uS'])
    uv = np.float32(request.form['uV'])

    return redirect('/')

# Resolution input from Webpage
@app.route('/resolution', methods = ['POST'])
def resolution():
    global res
    res = np.int32(request.form['RES'])

    return redirect('/')

# Tolerance input from Webpage
@app.route('/tolerance', methods = ['POST'])
def tolerance():
    global MIN_RAD
    MIN_RAD = np.int32(request.form['TOL'])

    return redirect('/')

# Button script for start and stop for Arduino Data.
@app.route('/button2', methods = ['POST'])
def button2():
    global arddata
    if request.method == 'POST':
            if request.form.get('senddata') == 'START':
                arddata = True

            if request.form.get('stopdata') == 'STOP':
                arddata = False
    return redirect('/')

filter_sel = False
median_val = 5
# Filter Selection
@app.route('/buttonfilter', methods = ['POST'])
def buttonfilter():
    global filter_sel
    if request.method == 'POST':
            if request.form.get('medianfilter') == 'MEDIAN':
                filter_sel = True

            if request.form.get('gaussfilter') == 'GAUSS':
                filter_sel = False
    return redirect('/')

# Take Median Value from user
@app.route('/medianval', methods = ['POST'])
def medianval():
    global median_val
    median_val = np.int32(request.form['MED'])

    return redirect('/')
# Button script for predefined HSV Modes.
@app.route('/button', methods = ['POST'])
def button():
    global lh 
    global ls
    global lv
    global uh
    global us
    global uv
    if request.method == 'POST':
            if request.form.get('action1') == 'HSV1':
                lh = 21
                ls = 80
                lv = 68
                uh = 39
                us = 200
                uv = 255
            elif  request.form.get('action2') == 'HSV2':
                pass # do something else
            else:
                pass # unknown

    return redirect('/')

def main():

    fps=1
    arr_dur=[0,0,0]
    while True:
        # Stat initial time.
        start_time=time.time()
        start_t0=time.time()

	# ---------------Capture Camera Frame-----------------
        frame = cap.read()

        # Resize and Rotate camera frame (RPi Camera shows inverted on program)
        frame = imutils.resize(frame, width = res)
        frame = imutils.rotate_bound(frame, 180)

        img=frame

        # Get image from camera
        # Blur image to remove noise

        if filter_sel == False:
            img_filter = cv2.GaussianBlur(img.copy(), (3, 3), 0)
        
        if filter_sel == True:
            img_filter = cv2.medianBlur(img.copy, median_val)

        # Convert image from BGR to HSV
        hsv = cv2.cvtColor(img_filter, cv2.COLOR_BGR2HSV)

        l_blue = np.array([lh,ls,lv],dtype=np.float32)
        u_blue = np.array([uh,us,uv],dtype=np.float32)

        # Set pixels to white if in color range, others to black (binary bitmap)
        img_binary = cv2.inRange(hsv, l_blue, u_blue)

        # Dilate image to make white blobs larger
        img_binary = cv2.dilate(img_binary, None, iterations = 1)
        
        # Find center of object using contours instead of blob detection.
        img_contours = img_binary.copy()
        contours = cv2.findContours(img_contours, cv2.RETR_EXTERNAL, \
            cv2.CHAIN_APPROX_SIMPLE)[-2]

        if len(contours) != 0:
            cmax = max(contours, key=cv2.contourArea)
            xmax,ymax,w,h=cv2.boundingRect(cmax)

            # If there no blob larger than tolerance return zero.
            if xmax+w < MIN_RAD*2:
                xmax=0
                ymax=0
                w=0
                h=0
                           
        # If there no blob return zero.
        else:
            ymax = 0
            xmax = 0
            w=0
            h=0
            

        arr_dur[0]=time.time() - start_t0
        start_t1=time.time()
        arr_dur[1]=time.time() - start_t1
        start_t2=time.time()

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
        # draw overlays to image
        cv2_im = draw_overlays(img, xmax, ymax,w,h, centermax, arr_dur)

        #Flask streaming
        # encode image to jpeg.
        ret, jpeg = cv2.imencode('.jpg', cv2_im)
        # encode jpeg to bytes.
        pic = jpeg.tobytes()

        #Flask streaming
        yield (b'--frame1\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + pic + b'\r\n\r\n')

        # encode image to jpeg.
        ret, binary = cv2.imencode('.jpg', img_binary)
        # encode jpeg to bytes.
        pic2 = binary.tobytes()

        #Flask streaming
        yield (b'--frame2\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + pic2 + b'\r\n\r\n')

        arr_dur[2]=time.time() - start_t2
        fps = round(1.0 / (time.time() - start_time),1)

    cap.release()
    cv2.destroyAllWindows()

# Segmentation part of the image. 
# In this process program will return overlay mark
# in detected position.
def segmentation(cv2_im,x, y, pos):
    #Define font and return h, w and channel value
    font=cv2.FONT_HERSHEY_SIMPLEX
    height, width, channels = cv2_im.shape

     # --------------------  Position between 1 to 5 --------------------
    if pos == 1:
        # Returns white rectangle in position
        cv2_im = cv2.rectangle(cv2_im, (0,0), (int((1/5)*width),int((1/3) * height)), (255,255,255), 2)
        # adds position text on overlay.
        cv2_im = cv2.putText(cv2_im, str(pos), (x,y), font,
                   1, (255, 0, 0), 2, cv2.LINE_AA)
        return cv2_im

    if pos == 2:
        cv2_im = cv2.rectangle(cv2_im, (int((1/5)*width),0), (int((2/5)*width),int((1/3) * height)), (255,255,255), 2)
        cv2_im = cv2.putText(cv2_im, str(pos), (x,y), font,
                   1, (255, 0, 0), 2, cv2.LINE_AA)
        return cv2_im

    if pos == 3:
        cv2_im = cv2.rectangle(cv2_im, (int((2/5)*width),0), (int((3/5)*width),int((1/3) * height)), (255,255,255), 2)
        cv2_im = cv2.putText(cv2_im, str(pos), (x,y), font,
                   1, (255, 0, 0), 2, cv2.LINE_AA)
        return cv2_im

    if pos == 4:
        cv2_im = cv2.rectangle(cv2_im, (int((3/5)*width),0), (int((4/5)*width),int((1/3) * height)), (255,255,255), 2)
        cv2_im = cv2.putText(cv2_im, str(pos), (x,y), font,
                   1, (255, 0, 0), 2, cv2.LINE_AA)
        return cv2_im

    if pos == 5:
        cv2_im = cv2.rectangle(cv2_im, (int((4/5)*width),0), (int(width),int((1/3) * height)), (255,255,255), 2)
        cv2_im = cv2.putText(cv2_im, str(pos), (x,y), font,
                   1, (255, 0, 0), 2, cv2.LINE_AA)
        return cv2_im

    # --------------------  Position between 6 to 10 --------------------
    if pos == 6:
        cv2_im = cv2.rectangle(cv2_im, (0,int((1/3) * height)), (int((1/5)*width),int((2/3) * height)), (255,255,255), 2)
        cv2_im = cv2.putText(cv2_im, str(pos), (x,y), font,
                   1, (255, 0, 0), 2, cv2.LINE_AA)
        return cv2_im

    if pos == 7:
        cv2_im = cv2.rectangle(cv2_im, (int((1/5)*width),int((1/3) * height)), (int((2/5)*width),int((2/3) * height)), (255,255,255), 2)
        cv2_im = cv2.putText(cv2_im, str(pos), (x,y), font,
                   1, (255, 0, 0), 2, cv2.LINE_AA)
        return cv2_im

    if pos == 8:
        cv2_im = cv2.rectangle(cv2_im, (int((2/5)*width),int((1/3) * height)), (int((3/5)*width),int((2/3) * height)), (255,255,255), 2)
        cv2_im = cv2.putText(cv2_im, str(pos), (x,y), font,
                   1, (255, 0, 0), 2, cv2.LINE_AA)
        return cv2_im

    if pos == 9:
        cv2_im = cv2.rectangle(cv2_im, (int((3/5)*width),int((1/3) * height)), (int((4/5)*width),int((2/3) * height)), (255,255,255), 2)
        cv2_im = cv2.putText(cv2_im, str(pos), (x,y), font,
                   1, (255, 0, 0), 2, cv2.LINE_AA)
        return cv2_im

    if pos == 10:
        cv2_im = cv2.rectangle(cv2_im, (int((4/5)*width),int((1/3) * height)), (int(width),int((2/3) * height)), (255,255,255), 2)
        cv2_im = cv2.putText(cv2_im, str(pos), (x,y), font,
                   1, (255, 0, 0), 2, cv2.LINE_AA)
        return cv2_im

    # --------------------  Position between 11 to 15 --------------------
    if pos == 11:
        cv2_im = cv2.rectangle(cv2_im, (0,int((2/3) * height)), (int((1/5)*width),int(height)), (255,255,255), 2)
        cv2_im = cv2.putText(cv2_im, str(pos), (x,y), font,
                   1, (255, 0, 0), 2, cv2.LINE_AA)
        return cv2_im

    if pos == 12:
        cv2_im = cv2.rectangle(cv2_im, (int((1/5)*width),int((2/3) * height)), (int((2/5)*width),int(height)), (255,255,255), 2)
        cv2_im = cv2.putText(cv2_im, str(pos), (x,y), font,
                   1, (255, 0, 0), 2, cv2.LINE_AA)
        return cv2_im

    if pos == 13:
        cv2_im = cv2.rectangle(cv2_im, (int((2/5)*width),int((2/3) * height)), (int((3/5)*width),int(height)), (255,255,255), 2)
        cv2_im = cv2.putText(cv2_im, str(pos), (x,y), font,
                   1, (255, 0, 0), 2, cv2.LINE_AA)
        return cv2_im

    if pos == 14:
        cv2_im = cv2.rectangle(cv2_im, (int((3/5)*width),int((2/3) * height)), (int((4/5)*width),int(height)), (255,255,255), 2)
        cv2_im = cv2.putText(cv2_im, str(pos), (x,y), font,
                   1, (255, 0, 0), 2, cv2.LINE_AA)
        return cv2_im

    if pos == 15:
        cv2_im = cv2.rectangle(cv2_im, (int((4/5)*width),int((2/3) * height)), (int(width),int(height)), (255,255,255), 2)
        cv2_im = cv2.putText(cv2_im, str(pos), (x,y), font,
                   1, (255, 0, 0), 2, cv2.LINE_AA)
        return cv2_im

    # Returns black rectangle on center when there is none
    else:
        cv2_im = cv2.rectangle(cv2_im, (int((2/5)*width),int((1/3) * height)), (int((3/5)*width),int((2/3) * height)), (0,0,0), 2)
        return cv2_im

# Serial Send algorithm for communication between Arduino and Rpi
# Since this communication sends too much data in time Arduino 
# program will struggle. Due that program will only send position
# if position changes in Global Control.

# Initial position cache selected higher to send inital position also.
positionold=25
def serialsend(position):
    # Using global to call and change 
    # variable inside of the function
    global arddata
    global positionold

    # Serial send controlled by Server Application. 
    # If button passed, program will send data to Arduino. 
    if arddata == True:
        # If position changes program sends 
        # position with serial communicaiton.
        # If it didnt change, it wont send any variable.
        if(positionold!=position):

            print(position)

            send_string = str(position)
            send_string += "\n"
            print(send_string)

            # Send the string. Make sure you encode it before you send it to the Arduino.
            ser.write(send_string.encode('utf-8'))
            positionold=position

        else:
            pass

# Position algorithm returns psoition value as integer.
# It decides its position by comparing center of the blob
# and 15 partition of the image
# centerofblob = (x + w/2, y + h/2)        
def position(cv2_im,x,y,w,h):
    
    # 16 statement compiled here. 15 of them returns position 1-15 
    # and where there is no detection program sends arduino 
    # 16 because 0 is not suitable for the parseInt(); command
    # due it also may give 0 when there is no data.

    # --------------------  Position between 1 to 5 --------------------
    height, width, channels = cv2_im.shape
    if (1/5)*width > x+w/2 > 0 and (1/3 * height) > y+h/2 > 0:
        position = 1
        serialsend(position)
        return position
    if (2/5)*width > x+w/2 > (1/5)*width and (1/3 * height) >y+h/2> 0:
        position = 2
        serialsend(position)
        return position
    if (3/5)*width > x+w/2 > (2/5)*width and (1/3 * height) > y+h/2 > 0:
        position = 3
        serialsend(position)
        return position
    if (4/5)*width > x+w/2> (3/5)*width and (1/3 * height) > y+h/2 > 0:
        position = 4
        serialsend(position)
        return position
    if width > x+w/2 > (4/5)*width and (1/3 * height) > y+h/2 > 0:
        position = 5
        serialsend(position)
        return position

     # --------------------  Position between 6 to 10 --------------------
    if (1/5)*width > x+w/2 > 0 and (2/3 * height) > y+h/2 > (1/3 * height):
        position = 6
        serialsend(position)
        return position
    if (2/5)*width > x+w/2 > (1/5)*width and (2/3 * height) > y+h/2 > (1/3 * height):
        position = 7
        serialsend(position)
        return position
    if (3/5)*width > x+w/2 > (2/5)*width and (2/3 * height) > y+h/2 > (1/3 * height):
        position = 8
        serialsend(position)
        return position
    if (4/5)*width > x+w/2 > (3/5)*width and (2/3 * height) > y+h/2 > (1/3 * height):
        position = 9
        serialsend(position)
        return position
    if width > x+w/2 > (4/5)*width and (2/3 * height) > y+h/2 > (1/3 * height):
        position = 10
        serialsend(position)
        return position

    # --------------------  Position between 11 to 15 --------------------
    if (1/5)*width > x+w/2 > 0 and (height) > y+h/2 > (2/3 * height):
        position = 11
        serialsend(position)
        return position
    if (2/5)*width > x+w/2 > (1/5)*width and (height) > y+h/2 > (2/3 * height):
        position = 12
        serialsend(position)
        return position
    if (3/5)*width > x+w/2 > (2/5)*width and (height) > y+h/2 > (2/3 * height):
        position = 13
        serialsend(position)
        return position
    if (4/5)*width > x+w/2 > (3/5)*width and (height) > y+h/2 > (2/3 * height):
        position = 14
        serialsend(position)
        return position
    if width > x+w/2 > (4/5)*width and (height) > y+h/2 > (2/3 * height):
        position = 15
        serialsend(position)
        return position
    
    # Returns 16 when there is none
    if x==0 and y==0:
        position=16
        serialsend(position)
        
        return position


# This function will create a overlay on the camera frame.
# Overlay will divide camera to 15 same rectangle and
# give info about FPS, Time, if arduino sending data etc.
def draw_overlays(cv2_im, x, y,w,h, center, arr_dur):
    height, width, channels = cv2_im.shape
    font=cv2.FONT_HERSHEY_SIMPLEX

    # We call our arddata boolean to process.
    global arddata

    # draw black rectangle on top and bottom.
    cv2_im = cv2.rectangle(cv2_im, (0,0), (width, 24), (0,0,0), -1)
    cv2_im = cv2.rectangle(cv2_im, (0,height-24), (width, height), (0,0,0), -1)

    # It shows the transmission status of the data sent to the Arduino. 
    if arddata == True:
        datatext = "Sending to Arduino"
    if arddata == False:
        datatext = "No data sending to Arduino"
    Data_status = 'Datasend: {}'.format(str(datatext))
    cv2_im = cv2.putText(cv2_im, Data_status, (int(width/4)-30, 16),font, 0.55, (255, 255, 255), 1)

    # writes FPS on the screen.
    dur1=round(arr_dur[0]*1000,0)
    dur2=round(arr_dur[1]*1000,0)
    dur3=round(arr_dur[2]*1000,0)
    total_duration=dur1+dur2+dur3
    fps=round(1000/total_duration,1)
    text1 = 'FPS: {}'.format(fps)
    cv2_im = cv2.putText(cv2_im, text1, (10, 20),font, 0.7, (255, 255,255), 2)
   
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")

    # Prints current time on screen
    str_time='{}'.format(current_time)
    cv2_im = cv2.putText(cv2_im, str_time, (10, height-8),font, 0.55, (255, 255, 255), 2)


    str_hsv="HSV: lH: "+ str(lh) + " lS: " + str(ls) +" lV: " +str(lv) +" uH: "+ str(uh) + " uS: " + str(us) +" uV: " +str(uv)
    cv2_im = cv2.putText(cv2_im, str_hsv, (int(width/2 - 60), height-8),font, 0.45, (150, 150, 255), 2)

    # Split image to 15 pair
    cv2_im = cv2.rectangle(cv2_im, (int(width/5)-1,0), (int(width/5)+1,height), (255,0,0), -1)
    cv2_im = cv2.rectangle(cv2_im, (int(2*width/5)-1,0), (int(2*width/5)+1,height), (255,0,0), -1)
    cv2_im = cv2.rectangle(cv2_im, (int(3*width/5)-1,0), (int(3*width/5)+1,height), (255,0,0), -1)
    cv2_im = cv2.rectangle(cv2_im, (int(4*width/5)-1,0), (int(4*width/5)+1,height), (255,0,0), -1)
    cv2_im = cv2.rectangle(cv2_im, (int(5*width/5)-1,0), (int(5*width/5)+1,height), (255,0,0), -1)

    # Get position and run segmentation 
    pos = position(cv2_im, x,y,w,h)
    segmentation(cv2_im,x, y, pos)

    # Return X and Y values if there is blob
    if pos != 16:
        coord_of_x='X: {}'.format(x)
        cv2_im = cv2.putText(cv2_im, coord_of_x, (110, height-8),font, 0.55, (0,255,0), 2)

        coord_of_y='Y: {}'.format(y)
        cv2_im = cv2.putText(cv2_im, coord_of_y, (220, height-8),font, 0.55, (0,255,0), 2)

    # Prints if there is none
    if(pos==16):
        str1="No object"

    # Prints the numbber of position 1-15
    else:
        str1='Object is at:' + " " + str(pos)
    
    cv2_im = cv2.putText(cv2_im, str1, (width-180, 18),font, 0.7, (0, 255, 255), 2)
    center=(x,y)

    # prints rectangle for detected area
    if pos !=16:
        cv2_im = cv2.rectangle(cv2_im,center,(x+w,y+h), (0, 255,0),2)


    return cv2_im


# App works on localhost:2250 and accesable with all devices connected to same internet
if __name__ == '__main__':
    app.run(host='0.0.0.0', port='2250', debug=False, threaded=True) # Run FLASK
    main()
