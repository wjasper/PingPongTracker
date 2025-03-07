# IMPORTS
# We don't need Picamera as camera can be accessed using opencv, whereas that is not the case with RaspberryPi
import numpy as np
import cv2
import sys
import time
import platform


def to_continue():
    """
    Prompts the user to start a new sampling session and returns a Boolean indicating their choice.

    This function displays a prompt asking if the user would like to start a new 5-second sampling session.
    If the user inputs 'y', 'Y', or simply presses Enter without typing anything, the function returns True,
    signaling that the program should continue with a new sampling session. If the user inputs 'n' or any
    other character, the function returns False, halting the sampling process.

    Returns:
        bool: True if the user chooses to start a new sampling session ('y', 'Y', or no input); 
              False otherwise.
    """
    answer = input("Start sampling for 5 seconds [y/n]: ")
    if answer == "y" or answer == "Y" or len(answer) == 0:
        return True
    else:
        return False


def calibration():
    """
    Calibrates the camera by capturing live video frames and displaying a calibration window,
    allowing the user to input minimum and middle distance values in inches from the origin (i.e., table).

    This function initializes the camera with specific video settings, initiates a live preview 
    with overlayed calibration lines, and prompts the user to enter minimum and middle distance 
    values (in inches) for calibration purposes. The function returns these user-defined values 
    for further use in the application.

    Configuration:
        - Sets up the camera with resolution, frame rate, and other properties.
        - Creates a live preview with calibration lines drawn vertically at the start, middle, 
          and end of the frame width.

    Controls:
        - The user can press 'q' to exit the preview window once calibration is complete.

    Returns:
        tuple: (min_value, mid_value)
            min_value (float): The user-defined minimum calibration value in inches.
            mid_value (float): The user-defined middle calibration value in inches.
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
        cv2.line(frame, (0, 0), (0, 480), (0, 0, 255), 3)  # Red line at beginning
        cv2.line(frame, (320, 0), (320, 480), (0, 255, 0), 3)  # Green line in middle
        cv2.line(frame, (640, 0), (640, 480), (255, 0, 0), 3)  # Blue line at end
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
    """
    Captures a 5-second video to detect a moving object (specifically, a ping pong ball),
    processes the frames to estimate the object's position in inches, and saves multiple output videos.

    This function operates the camera in a loop, capturing real-time frames and employing 
    a background subtraction technique to isolate the moving object. The function detects the object's 
    contours, identifies its center, and calculates its horizontal position based on calibration values.

    Parameters:
        min_value (float): The minimum calibration distance in inches, corresponding to a known position.
        mid_value (float): The mid calibration distance in inches, representing the midpoint of the calibration range.

    Process Overview:
        - Continuously captures frames until the user opts to stop.
        - Initializes the camera and captures a background image for subsequent background subtraction.
        - Captures video frames in real-time (approximately 90 frames per second) for a duration of 5 seconds.
        - Processes each frame to detect and mark the moving object.
        - Uses contours to locate the object's position and calculates its coordinates based on specified criteria 
          (minimum area and aspect ratio).
        - Outputs processed frames with detected contours to video files for further analysis.

    Outputs:
        - Three video files saved in the 'output' directory:
            - "ping_pong_raw_input.avi": Contains the raw video input from the camera.
            - "ping_pong_with_detection.avi": Shows the video with detected contours highlighted.
            - "ping_pong_bw_with_detection.avi": A black-and-white video overlaying the detection.
        - Prints the estimated horizontal distance of the object in inches if tracking is successful.

    Controls:
        - Press 'q' to stop the video preview or terminate the recording early.

    Returns:
        None
    """

    while to_continue():

        # Initialize the camera using OpenCV
        cap = cv2.VideoCapture(0)  # 0 for the default camera

        frames = []

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

        # Define codec and create a VideoWriter object
        fourcc = cv2.VideoWriter_fourcc(*"XVID")
        inp = cv2.VideoWriter(
            "output/ping_pong_raw_input.avi", fourcc, framerate, (width, height)
        )
        out = cv2.VideoWriter(
            "output/ping_pong_with_detection.avi", fourcc, framerate, (width, height)
        )
        out_bw = cv2.VideoWriter(
            "output/ping_pong_bw_with_detection.avi",
            fourcc,
            framerate,
            (width, height),
            0,
        )

        for frame in frames:
            og_frame = frame.copy()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            img = cv2.absdiff(gray, bg_img_bw)
            img = cv2.blur(img, (3, 3))
            ret, img = cv2.threshold(img, 40, 255, cv2.THRESH_BINARY)

            contours, _ = cv2.findContours(
                img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
            )

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
            cv2.imshow("Raw", og_frame)

            # write images to file
            inp.write(og_frame)
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
        inp.release()
        cap.release()


def main():
    """
    Main function to initialize the camera, perform calibration, and start video capture.

    This function serves as the entry point of the program, initializing the camera, 
    conducting a calibration process to obtain minimum and middle distance values in inches, 
    and initiating a 5-second video capture and processing loop for object detection and tracking.

    Process:
        - Initializes the camera.
        - Calls the `calibration` function to open a calibration window and prompts the user 
        for minimum and mid-point calibration values in inches.
        - Passes these calibration values to the `shoot_video` function, which captures and processes 
        real-time frames to track an object and estimate its position in inches.

    Functions:
        - `calibration()`: Calibrates the camera and returns user-defined min and mid values.
        - `shoot_video(min_value, mid_value)`: Captures and processes video using calibration values.

    Returns:
        None
    """

    # Calibration function
    min_value, mid_value = calibration()
    # Function to shoot the video
    shoot_video(min_value, mid_value)


# Set camera properties
framerate = 90  # Frames per second for video capture
width = 640     # Width of video frame
height = 480    # Height of video frame

if __name__ == "__main__":
    """
    Main script entry point.

    Sets camera properties such as framerate, frame width, and height, then
    checks if the operating system is compatible with the program.
    If running on a non-Linux system (e.g., Windows), it initializes and starts
    the main process for calibration and video capture. If executed on a Linux system,
    a message is displayed indicating OS incompatibility.

    Compatibility:
        - Non-Linux OS required (e.g., Windows).
        - On Linux systems, a message is displayed indicating OS incompatibility.

    Functions:
        - main(): Initializes the camera, performs calibration, and starts video capture.

    """
    if platform.system() != "Linux":
        # OS is windows/macOS program executed using OpenCV
        main()
    else:
        print("OS not compatible")
