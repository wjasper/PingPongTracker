#!/usr/bin/env python3

from collections import deque
from picamera2 import Picamera2
import numpy as np
import cv2
import imutils

whiteLower = (0, 0, 200)
whiteUpper = (180, 30, 255)
buffer_size = 64
pts = deque(maxlen=buffer_size)

#Initialize the PiCamera2
cam = Picamera2()
cam.exposure_mode = 'night'

# Set preview configuration
cam.framerate = 80
width = 640
height = 480

main = {'size': (width, height), 'format': 'RGB888'}
controls = {'FrameRate': 80}
sensor = {'bit_depth': 10, 'output_size': (640,480)}
video_config = cam.create_video_configuration(main, controls=controls, sensor=sensor)
cam.configure(video_config)

# Start the preview
cam.start()

while True:
    frame = cam.capture_array()
    if frame is None:
        break
    frame = imutils.resize(frame, width=800)
    blurred = cv2.GaussianBlur(frame, (5, 5), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, whiteLower, whiteUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    center = None
    if len(cnts) > 0:
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        if radius > 5:
            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
            cv2.circle(frame, center, 5, (0, 0, 255), -1)
    pts.appendleft(center)
    for i in range(1, len(pts)):
        if pts[i - 1] is None or pts[i] is None:
            continue
        thickness = int(np.sqrt(buffer_size / float(i + 1)) * 2.5)
        cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)
    
    
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

# Release the video writer and video stream
cam.stop()
cv2.destroyAllWindows()
