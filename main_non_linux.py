import numpy as np
import cv2
import sys
import time
import platform

def to_continue():
  answer = input('Start sampling for 5 seconds [y/n]: ')
  if (answer == 'y' or answer == 'Y' or len(answer) == 0):
    return True
  else:
    return False



def calibration():
    """
    The objective of this function is to access the camera of the device,
    Create a calibration frame,
    And return the frame values.
    """
    # Initialize the camera using OpenCV
    cap = cv2.VideoCapture(0)  # 0 for the default camera

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    cap.set(cv2.CAP_PROP_FPS, framerate)


    # Start Calibration:
    while True:
        ret, frame = cap.read()  # Capture frame from the camera
        if not ret:
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

    # Release the camera
    cap.release()
    
    min_value = float(input("Enter the minimum value in inches: "))
    mid_value = float(input("Enter the mid value in inches: "))
    
    return min_value, mid_value
   

def shoot_video(min_value, mid_value):
    
    
    while to_continue():
        
        # Initialize the camera using OpenCV
        cap = cv2.VideoCapture(0)  # 0 for the default camera
    

        frames = []

        # Store the background image
        # Store the background image
        ret, bg_img = cap.read()
    
        if not ret:
                print("Failed to grab background frame")
                break
        bg_img_bw = cv2.cvtColor(bg_img, cv2.COLOR_BGR2GRAY)
            
        start_time = time.time()
        # Capture images in real time (~90fps)
        while time.time() - start_time < 5:
            ret, frame = cap.read()
            if not ret:
                print("Failed to grab frame")
                break
            frames.append(frame)
        
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
            
           # Define codec and create a VideoWriter object
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            out = cv2.VideoWriter('ping_pong.avi',fourcc,framerate,(width,height))
            out_bw = cv2.VideoWriter('ping_pong_bw.avi',fourcc,framerate,(width,height),0)

            # write images to file        
            out.write(frame)
            out_bw.write(img)

            key = cv2.waitKey(40) & 0xFF
            if key == ord("q"):
                break
        if X is None and Y is None:
                print("Was not able to track the ping pong ball. Try adjusting the sensor.")
        else:
            print("Found them:", X, Y)
            x_inches = min_value + (mid_value - min_value) / (width / 2) * X
            print("Distance in inches:", x_inches)

        # Clean up after processing
        cv2.destroyAllWindows()
        out.release()
        out_bw.release()
        cap.release()



  
# Set camera properties
framerate = 90
width = 640
height = 480  

def main():

    min_value, mid_value = calibration()
    shoot_video(min_value, mid_value)
    #Function to shoot the video
    



if __name__ == "__main__":
    if platform.system() != "Linux":
        # OS is windows/Linux program executed using OpenCV
        main()
    else:
        print("OS not compatible")
