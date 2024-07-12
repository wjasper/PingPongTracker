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

while True:
    for frame in frames:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        img = cv2.absdiff(gray, bg_img_bw)
        img = cv2.blur(img, (3,3))
        ret, img = cv2.threshold(img, 50, 255, cv2.THRESH_BINARY)
            
        cv2.imshow("Frame", frame)
        cv2.imshow("Image", img)
        
        key = cv2.waitKey(40) & 0xFF
        if key == ord("q"):
            break
        
    cv2.destroyAllWindows()