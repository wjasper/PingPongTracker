from collections import deque

import numpy as np
import cv2
import imutils
import sys

def main():
    if sys.platform == "linux" or sys.platform  == "linux2":
        import libcamera
        from picamera2 import Picamera2
      
        # Initialize the PiCamera2
        cam = Picamera2()
    
        # Set preview configuration
        cam.framerate = 60
        width = 640
        height = 480
        cam.configure(cam.create_video_configuration(main={"format": 'RGB888', "size": (width, height)}))
    
        # Start the preview
        cam.start()
      elif sys.platform == "win32":
        from imutils.video import VideoStream
        vs = VideoStream(src=0).start()
      else:
        print("OS not supported.")
        sys.exit()
    elif sys.platform == "win32"
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

    # frame = cv2.flip(background_frame,1)
    cv2.line(frame,(0,0),(0,480),(0,0,255),3)       # Red line at beginning
    cv2.line(frame,(320,0),(320,480),(0,255,0),3)   # Green line in middle
    cv2.line(frame,(640,0),(640,480),(255,0,0),3)   # Blue line at end
    cv2.imshow("Calibration", frame)
    key = cv2.waitKey(40) & 0xFF
    if key == ord("q"):
      break
cv2.destroyAllWindows()    

whiteLower = (0, 0, 200)
whiteUpper = (180, 30, 255)
buffer_size = 64
pts = deque(maxlen=buffer_size)

input("Hit any key to start: ")
frames = []
start_time = sys.time()
while time.time() - start_time < 10:
    if sys.platform == "linux" or sys.platform  == "linux2":
        frame = cam.capture_array()
   else:
    frame = vs.read()
 frames.append(frame)

 # stop the camera
 cam.stop()

for frame in frames:
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
      vs.stop()
      cv2.destroyAllWindows()

if __name__ == "__main__":
  main()
