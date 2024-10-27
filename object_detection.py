#IMPORTS
import cv2
import numpy as np

"""
Post-processing logic, first we just got the video saved it,
and later wrote the logic to track the ball and calculate the distance.

Decided to do this, so we don't have to conduct the experiment again and again.
After this logic is completed it later can be included in main.py/main_linux.py/main_non_linux.py
"""

video_path = 'demo_output/ping_pong.avi'
cap = cv2.VideoCapture(video_path)
frames = []

while True:
    ret, frame = cap.read()
    if not ret:
        break
    frames.append(frame)

cap.release()

#get the base frame to later compare with 
bg_img = frames[0] if frames else None
#convert the frame to b&w, reducing computational work 
bg_img_bw = cv2.cvtColor(bg_img, cv2.COLOR_BGR2GRAY)

centers = []

X, Y = None, None
y_prev = None
x_prev = None

for frame in frames:
    #convert the current frame to b&w, reducing computational work
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #taking absolute difference between the first converted b&w frame with the current frame
    img = cv2.absdiff(gray, bg_img_bw)
    img = cv2.blur(img, (3, 3))
    ret, img = cv2.threshold(img, 50, 255, cv2.THRESH_BINARY)

    #draw contours around the differences
    contours, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    #find the area of all the contours
    for contour in contours:
        area = cv2.contourArea(contour)
        min_area = 100
        
        #draw a circle/track the deformed shape, only if its area and aspect_ratio > threshold
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
                    
                    print(cx, cy)
                    
                    #setting the y_prev for the first time
                    if y_prev is None:
                        y_prev = cy
                        x_prev = cx
                    
                    #Changing the y_prev if the y is increasing
                    if cy>=y_prev:
                        y_prev = cy
                        x_prev = cx
                    
                    #Y is decreasing and X and Y both are not been found yet
                    elif cy<y_prev and X is None and Y is None:
                        X = x_prev
                        Y = y_prev
    

    cv2.imshow("Frame", frame)
    cv2.imshow("Image", img)

    key = cv2.waitKey(40) & 0xFF
    if key == ord("q"):
        break

cv2.destroyAllWindows()

#return the coordinates of circle, after its first point of contact with the ground.
print("Found them:", X, Y)