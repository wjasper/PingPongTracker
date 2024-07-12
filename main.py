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
        metadata = cam.capture_metadata()
        print("framerate = ", metadata)

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

    while True:
      for frame in frames:
          gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
          img = cv2.absdiff(gray, bg_img_bw)
          img = cv2.blur(img, (3,3))
          ret, img = cv2.threshold(img, 50, 255, cv2.THRESH_BINARY)
          circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1, 20,
                                     param1=50, param2=30, minRadius=0, maxRadius=0)
          if circles is not None:
              detected_circles = np.uint16(np.around(circles))
              print(detected_circles)
              for pt in detected_circles[0, :]:
                  x, y, r = pt[0], pt[1], pt[2]
                  cv2.circle(frame, (x, y), r, (0, 255, 0), 3)
                  cv2.circle(frame, (x, y), 2, (0, 255, 0), 3)
                  cv2.circle(img, (x, y), 2, (0, 255, 0), 3)
            
          cv2.imshow("Frame", frame)
          cv2.imshow("Image", img)
          key = cv2.waitKey(40) & 0xFF
          if key == ord("q"):
              break
        
    
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
