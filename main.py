#!/usr/bin/env python3

import numpy as np
import cv2
import sys
import time

def main():
    if sys.platform == "linux" or sys.platform == "linux2":
        import libcamera
        from picamera2 import Picamera2

        # Initialize the PiCamera2
        cam = Picamera2()

        # Set preview configuration
        framerate = 80
        width = 640
        height = 480
        cam.configure(cam.create_video_configuration(
            {"format": 'RGB888', "size": (width, height)},
            controls={"FrameRate": framerate}))
        # Start the preview
        cam.start()

    elif sys.platform == "win32":
        from imutils.video import VideoStream
        # Start the video stream
        vs = VideoStream(src=0).start()
    else:
        print("OS not supported.")
        sys.exit()

    # Start Calibration:
    while True:
        if sys.platform == "linux" or sys.platform == "linux2":
            frame = cam.capture_array()
        else:
            frame = vs.read()
          
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

    min_value = int(input("Enter the minimum value in inches: "))
    mid_value = int(input("Enter the mid value in inches: "))

    input("Hit any key to start: ")
    frames = []
    bg_img = cam.capture_array()
    bg_img_bw = cv2.cvtColor(bg_img, cv2.COLOR_BGR2GRAY)
    
    start_time = time.time()
    while time.time() - start_time < 5:
        if sys.platform == "linux" or sys.platform  == "linux2":
            frame = cam.capture_array()
        else:
            frame = vs.read()
        frames.append(frame)

    # Stop the camera
    if sys.platform == "linux" or sys.platform == "linux2":
        cam.stop()
    # Release the video stream and close all windows
    elif sys.platform == "win32":
        vs.stop()

    for frame in frames:
        cv2.imshow('Frame', frame)
        key = cv2.waitKey(40) & 0xFF
        if key == ord("q"):
            break
        
    ans = input("Save to file? ")
    if ans == 'y':
        # Define codec and create a VideoWriter object
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter('ping_pong.avi',fourcc,20.0,(640,480))
        for frame in frames:
            out.write(frame)
        out.release

    centers = []

    X, Y = None, None
    y_prev = None
    x_prev = None

    for frame in frames:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        img = cv2.absdiff(gray, bg_img_bw)
        img = cv2.blur(img, (3, 3))
        ret, img = cv2.threshold(img, 50, 255, cv2.THRESH_BINARY)

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
                    
                        #setting the y_prev for the first time
                        if y_prev is None:
                            y_prev = cy
                            x_prev = cx
                    
                        #Changing the y_prev if the y is increasing
                        if cy >= y_prev:
                            y_prev = cy
                            x_prev = cx
                    
                        #Y is decreasing and X and Y both are not been found yet
                        elif cy < y_prev and X is None and Y is None:
                            X = x_prev
                            Y = y_prev
                            
        cv2.imshow("Frame", frame)
        cv2.imshow("Image", img)

        key = cv2.waitKey(40) & 0xFF
        if key == ord("q"):
            break
    
    print("Found them:", X, Y)
    x_inches = min_value + (mid_value - min_value)/(width/2)*X
    print("Distance in inches: ", x_inches)

cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
    
