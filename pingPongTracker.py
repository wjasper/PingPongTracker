#!/usr/bin/env python3

import numpy as np
import cv2
import sys
import time
import libcamera
from picamera2 import Picamera2

def toContinue():
  answer = input('Start sampling for 5 seconds [y/n]: ')
  if (answer == 'y' or answer == 'Y' or len(answer) == 0):
    return True
  else:
    return False

def main():

    # Initialize the PiCamera2
    cam = Picamera2()

    # Set preview configuration
    framerate = 90
    width = 640
    height = 480

    main = {'size': (width, height), 'format': 'RGB888'}
    controls = {'FrameRate': framerate}
    sensor = {'bit_depth': 10, 'output_size': (640,480)}
    video_config = cam.create_video_configuration(main, controls=controls, sensor=sensor)
    cam.configure(video_config)

    # Print the current configuration settings:
#        current_config = cam.camera_controls
#        print("Current Configuration Settings:")
#        for key, value in current_config.items():
#            print(f"{key}: {value}")

    # Start the preview
    cam.start()

    # Start timing measurements
    start_time = time.time()
    for frame_count in range(1, 1000):
        if sys.platform == "linux" or sys.platform == "linux2":
            frame = cam.capture_array()
        else:
            frame = vs.read()
          
        if frame is None:
            break

        if frame_count % 100 == 0:
          end_time = time.time()
          elapsed_time = end_time - start_time
          print("frames per second: ", int(frame_count/elapsed_time))
        
    # Start Calibration:
    print("Determine minimum value (cm or inches) at red line.")
    print("Determine middle value (cm or inches) at green line.")
    print("Hit 'q' in the calibration window when done")
    
    while True:
        frame = cam.capture_array()
              
        if frame is None:
            break
    
        # Draw calibration lines
        cv2.line(frame, (0, 0), (0, 480), (0, 0, 255), 3)       # Red line at beginning
        cv2.line(frame, (320, 0), (320, 480), (0, 255, 0), 3)   # Green line in middle
        cv2.line(frame, (640, 0), (640, 480), (255, 0, 0), 3)   # Blue line at end
        cv2.imshow("Calibration", frame)
        key = cv2.waitKey(40) & 0xFF
        if key == ord("q"):
            break
  
    cv2.destroyAllWindows()

    # Stop the camera
    cam.stop()

    min_value = float(input("Enter the minimum value in inches: "))
    mid_value = float(input("Enter the mid value in inches: "))

    while toContinue():

        # Start the camera
        cam.start()

        frames = []

        # Store the background image
        bg_img = cam.capture_array()
        bg_img_bw = cv2.cvtColor(bg_img, cv2.COLOR_BGR2GRAY)
    
        start_time = time.time()
        # capture images in real time ~ 90fps
        while time.time() - start_time < 5:
          frame = cam.capture_array()
          frames.append(frame)

        for frame in frames:
            cv2.imshow('Frame', frame)
            key = cv2.waitKey(40) & 0xFF
            if key == ord("q"):
                break
        
        # Define codec and create a VideoWriter object
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter('ping_pong.avi',fourcc,framerate,(width,height))
        out_bw = cv2.VideoWriter('ping_pong_bw.avi',fourcc,framerate,(width,height),0)
        
        centers = []

        X, Y = None, None
        y_prev = None
        x_prev = None

        for frame in frames:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            img = cv2.absdiff(gray, bg_img_bw)
            img = cv2.blur(img, (3, 3))
            ret, img = cv2.threshold(img, 40, 255, cv2.THRESH_BINARY)

            contours, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            for contour in contours:
                area = cv2.contourArea(contour)
                min_area = 100
        
                if area > min_area:
                    x, y, w, h = cv2.boundingRect(contour)
                    aspect_ratio = float(w) / h
                    max_aspect_ratio = 3.0
            
                    if aspect_ratio <= max_aspect_ratio:
                        cv2.drawContours(frame, [contour], -1, (255, 0, 0), 2)

                        M = cv2.moments(contour)
                        if M["m00"] != 0:
                            cx = int(M["m10"] / M["m00"])
                            cy = int(M["m01"] / M["m00"])
                            centers.append((cx, cy))
                    

                            cv2.circle(frame, (cx, cy), 5, (0, 255, 0), -1)
                    
                            print("Centers:", cx, cy)
                            
                            # Setting the y_prev for the first time
                            if y_prev is None:
                                y_prev = cy
                                x_prev = cx
                    
                            # Changing the y_prev if the y is increasing
                            if cy >= y_prev:
                                y_prev = cy
                                x_prev = cx
                   
                            # Y is decreasing and X and Y both are not been found yet
                            # store values for first minimum in Y
                            elif cy < y_prev and X is None and Y is None:
                                X = x_prev
                                Y = y_prev
                            
            cv2.imshow("Frame", frame)
            cv2.imshow("Image", img)

            # write images to file        
            out.write(frame)
            out_bw.write(img)

            key = cv2.waitKey(40) & 0xFF
            if key == ord("q"):
                break

        if X == None and Y == None:
            print("Was not able to track the ping pong ball.  Try moving the sensor further away from the target")
            print("increasing the lighting or lowering the threshold.")
        else:
            print("Found them:", X, Y)
            x_inches = min_value + (mid_value - min_value)/(width/2)*X
            print("Distance in inches: ", x_inches)

        cam.stop()
        cv2.destroyAllWindows()
        out.release()
        out_bw.release()

if __name__ == "__main__":
    main()
    
