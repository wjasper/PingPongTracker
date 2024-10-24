import cv2
import numpy as np

video_path = 'ping_pong.avi'
cap = cv2.VideoCapture(video_path)
frames = []

while True:
    ret, frame = cap.read()
    if not ret:
        break
    frames.append(frame)

cap.release()

bg_img = frames[0] if frames else None
bg_img_bw = cv2.cvtColor(bg_img, cv2.COLOR_BGR2GRAY)

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

print("Found them:", X, Y)