import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import cv2
import time 
import math 
import numpy as np 
import asyncio
from sphero_sdk import AsyncSpheroRvr
from sphero_sdk import SerialAsyncDal
from picamera.array import PiRGBArray 
from picamera import PiCamera

# Initialize RVR
loop = asyncio.get_event_loop()

rvr = AsyncSpheroRvr(
    dal=SerialAsyncDal(
        loop
    )
)
# Sets up video capture to write out to pi
out = cv2.VideoWriter('output.mjpg', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 10, (640,480))

# Initializes global variables for PID controller
prev_rc = 0.0
rc_integral = 0.0

async def filter_image(image):
       gray = cv2.cvtColor(image[150:], cv2.COLOR_BGR2GRAY)
       #cv2.imwrite('gray.jpg', gray)
       blurred = cv2.GaussianBlur(gray, (5, 5), 0)
       #cv2.imwrite('blur.jpg',blurred)
       edged = cv2.Canny(blurred, 85, 85)
       #cv2.imwrite('canny.jpg', edged)
       return edged

async def turn_rvr(theta):
# Calculates new heading based on theta
    if theta<0 :
        heading = -theta
    else:
        heading = 359-theta

    print('The current heading is {} degrees'.format(int(heading)))


    # Drive RVR based on new heading
    if theta == 0:
        await rvr.raw_motors(1, 0, 1, 0)
        await asyncio.sleep(.5)
    elif abs(theta) > 15:
        await rvr.drive_with_heading(10, int(heading),0)
        asyncio.sleep(.01)
    else:
        await rvr.drive_with_heading(45, int(heading), 0)
        asyncio.sleep(.01)


# PID controller
async def drive_PID(delta, reset = False):
    rc_integral_bleedoff = .98
    rc_tolerance = .05

    global prev_rc
    prev_rc = 0.0
    global rc_integral
    rc_integral = 0.0
    coeff_p = 2  # Change as needed (Proportional Term)
    coeff_i = 0.5  # Change as needed (Integral Term)
    coeff_d = 0.05 # Change as needed (Derivative Term)

    if reset:
        prev_rc = 0.0
        rc_integral = 0.0
        return 0.0

    rc_error = delta

    if abs(rc_error) >= rc_tolerance:
        rc_integral += rc_error
    else:
        rc_integral *= rc_integral_bleedoff

    deriv = delta - prev_rc
    prev_rc = delta

    rc_p_term = coeff_p * rc_error
    rc_i_term = coeff_i * rc_integral
    rc_d_term = coeff_d * deriv

    if abs(rc_i_term) > 200.0:
        rc_integral -= rc_error

    return rc_p_term + rc_i_term + rc_d_term


async def self_drive():
    await rvr.wake()
    await rvr.reset_yaw()
    #  Initialize camera and variables for Hough Transform
    theta=0
    min_line_length = 5
    max_line_gap = 10
    camera = PiCamera()
    camera.vflip = True
    camera.hflip = True
    camera.exposure_mode = 'sports'
    camera.resolution = (640,480)
    camera.framerate = 30
    raw_capture = PiRGBArray(camera, size=(640, 480))
    time.sleep(.2)

    try:
        for frame in camera.capture_continuous(raw_capture, format="bgr", use_video_port=True):

            image = frame.array # Capture image from continuous capture

            # Filter the image to better detect edges
            edged = await filter_image(image)
            # Calculate lines using built in Hough Transform
            lines = cv2.HoughLinesP(edged,1,np.pi/180,10,min_line_length,max_line_gap)

            if lines is not None:
                for x in range(0, len(lines)):
                    for x1, y1, x2, y2 in lines[x]:
                        cv2.line((image[150:]),(x1,y1),(x2,y2),(0,255,0),2)
                        theta = theta+math.atan2((y2-y1),(x2-x1))

            threshold = 0 # Minimum turning angle threshold

            # Check if angle is too small to spend time resetting yaw
            if abs(theta) > threshold:
                await rvr.reset_yaw()

            theta = await drive_PID(theta)
            await turn_rvr(theta)

            #cv2.imshow("Frame",image)  # Shows camera feed in frame when raspberry pi is plugged into monitor
            out.write(image)
            raw_capture.truncate(0)
            theta = 0
    except KeyboardInterrupt:
        
        global loop 
        loop.stop()





loop.run_until_complete(
    asyncio.gather(
        self_drive()
    )
)

loop.close()
out.release()
quit()

