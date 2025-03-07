# PingPongTracker

Project Team members:-
1. Warren Jasper (wjasper@ncsu.edu)
2. Shivam Ghodke (sghodke@ncsu.edu)


Techstack:- OpenCV, Python, RaspberryPi, Picamera

## Getting Started

To start with the project, follow these steps:

```
git clone https://github.com/wjasper/PingPongTracker.git
cd PingPongTracker
pip3 install -r requirements.txt #Recommend to install dependencies in virtual env
python3 main_linux.py  # For Linux
# or
python3 main_non_linux.py  # For non-Linux systems
```

| **Description**   | **Link**                                                                                         |
|-------------------|--------------------------------------------------------------------------------------------------|
| **Portfolio website**     | [shivam.foo](https://shivam.foo)                                                                |
| **Important**     | Looking for entry level SWE roles, graduating @NC State in computer science in  May 2025                                                          |
| **GitHub**        | [nuttysunday](https://github.com/nuttysunday)       |
| **Blog Link**     | [shivam.foo/blogs/ping-pong-ball-tracking-and-projected-distance-calculation-system-for-data-modeling](https://shivam.foo/blogs/ping-pong-ball-tracking-and-projected-distance-calculation-system-for-data-modeling)                          |
| **Video Link**    | [Youtube Video](https://youtu.be/N7TDCUCSW0k?si=lRdCIzLh7jm-0_Nt)                                     |
| **LinkedIn**      | [Linkedin Profile](https://www.linkedin.com/in/shivam-ghodke/)                                             |
| **Resume**        | [Resume](https://drive.google.com/file/d/1OC_mcMHkBaDhWbKEMfsnLY-uBS8Xee7G/view)              |
| **Twitter**       | [Twitter/X account](https://x.com/sundaycide)                                                                |



## Video overview
You can watch an overview of the project by clicking the link below:

[![Self Hosting Video](https://img.youtube.com/vi/N7TDCUCSW0k/0.jpg)](https://youtu.be/N7TDCUCSW0k?si=lRdCIzLh7jm-0_Nt)

**Video Link**: [Project Overview](https://youtu.be/N7TDCUCSW0k?si=lRdCIzLh7jm-0_Nt)


Feel free to modify any part of it to better suit your needs!
## Table of Contents
1. [Understanding the Project](#1-understanding-the-project)
2. [Motivation](#2-motivation)
3. [Traditional Way](#3-traditional-way)
4. [Our Method](#4-our-method)
    - [Calibration](#41-calibration)
    - [Ball Tracking and Distance Calculation](#42-ball-tracking-and-distance-calculation)
    - [Challenges We Faced](#43-challenges-we-faced)
        - [OpenCV not compatible with Raspberry Pi camera](#431-opencv-not-compatible-with-raspberry-pi-camera)
        - [Hardware Limitation for Processing in Real-Time](#432-hardware-limitation-for-processing-in-real-time)
        - [Speed and Shape of Ball Made it Impossible to Track Ball](#433-speed-and-shape-of-ball-made-it-impossible-to-track-ball)
        - [Ball Not Being Ball Shaped](#434-ball-not-being-ball-shaped)
    - [Coordinates to Actual Distance](#44-coordinates-to-actual-distance)



## 1. Understanding the Project
Calculating the distance at which the ball is going to have its first point of contact with the ground after being launched using a catapult.

![Objective Image](https://shivam.foo/images/ping-pong-ball-tracking-system/objective.png)

## 2. Motivation
The reason behind doing this project is for data modeling that is to collect training data so it could later be used by machine learning regression models.

![Motivation Image](https://shivam.foo/images/ping-pong-ball-tracking-system/table.jpg)


## 3. Traditional Way
Lay aluminium foil in the expected area where the ball is going to land for a particular configuration, launch the ball, identify the dent on the foil, and calculate the distance using the measuring tape placed parallel with the foil.
![Traditional Way Image](https://shivam.foo/images/ping-pong-ball-tracking-system/traditional.jpg)

This is a tedious process that takes a lot of time. It is a two-man job, and it is not feasible when sampling 10,000 data points.

## 4. Our Method
Using a Raspberry Pi with an HD camera mounted on it, powered by a power bank, can be operated using a remote desktop making the system very mobile. Place Raspberry Pi camera as shown in the picture below.
![Our System Image](https://shivam.foo/images/ping-pong-ball-tracking-system/raspberry_pi.png)


Place the Raspberry Pi camera as shown in the picture below:

![Our Method Image](https://shivam.foo/images/ping-pong-ball-tracking-system/r_setup.jpg)

### 4.1 Calibration
Place a ruler scale, align the scale with green and red line, and get the value on the tape in inches respectively.

Here are the values:
- Green value (mid_value) = 112
- Red value (minimum_value) = 84

![Calibration Image](https://shivam.foo/images/ping-pong-ball-tracking-system/calib_window.png)


### 4.2 Ball Tracking and Distance Calculation
So after weeks of research, trials and errors, after losing all hope and were almost about to scrap the project, my professor came up with a brilliant idea. Background separations:- So what we do is take the the first frame, convert it to b&w, and for each frame, we take the absolute the difference with this bg_image.

#### Base Frame
![Base Frame](https://shivam.foo/images/ping-pong-ball-tracking-system/base_frame.png)

#### Background Separation Process
![Background Separation](https://shivam.foo/images/ping-pong-ball-tracking-system/bg_seperation.gif)

#### Ball Tracked
![Ball Tracked](https://shivam.foo/images/ping-pong-ball-tracking-system/ball_tracked.png)

#### Distance Output
![Distance Output](https://shivam.foo/images/ping-pong-ball-tracking-system/distance_output.png)

### 4.3 Challenges We Faced

#### 4.3.1 OpenCV not compatible with Raspberry Pi camera
First challenge, we faced was opencv library is not compatible with the Raspberry Pi camera, and thus have to use Picamera library to get camera object. Also we were getting very low fps, and had to increase it by trying out various Picamera techniques.

#### 4.3.2 Hardware Limitation for Processing in Real-Time
We initially wanted to do this in real-time, but because of hardware limitations, the Pi was not able to process the frames as soon as it received them.
So we decided to use post-processing, that is first record the video, store the frames in a buffer, and process each frame one by one.

#### 4.3.3 Speed and Shape of the Ball Made It Impossible to Track
The second problem we faced was that the ball was moving at a very high pace, which was visible maybe for 1-3 frames, and the program was not able to do any object detection.

So we even tried using a plain dark color background, covered using a cloth, but nonetheless because of how small and fast the ball was, the program was not able to track it.

So after weeks of research, trials and errors, after losing all hope and almost about to scrap the project, my professor came up with a brilliant idea.

#### Important Note
OpenCV is not compatible with Raspberry Pi for accessing the camera object, thus need to use PiCamera library.

Note there is one caveat here, when we are shooting the ball, there should be no movement in the background, that is the background could be cluttered, does not matter, but there should not be a moving object in the frame, because then it would be captured by the absolute difference.

#### 4.3.4 Ball Not Being Ball Shaped
When the ball travels at a faster pace, in a particular frame, it appears to have a deformed shape, more like a comet.

![Comet Shape](https://shivam.foo/images/ping-pong-ball-tracking-system/comet_shape.jpeg)

So no existing articles, blogs or openCV functions which detect objects helped us.

This [article](https://pyimagesearch.com/2015/09/14/ball-tracking-with-opencv/) provided a good starting point, but it could not track the ball effectively due to its speed and the deformation of its shape, as it was only visible for 1-3 frames.

So that is where we decided to actually just detect the contours in the image subtracted, get the area of the contour and if it is 100px, and the aspect ratio 3, that is it is more of an oval shape than a boxier shape, then draw a circle around it, and start tracking its coordinates of the centre.
As you can see in this particular frame, it is not a circle, but a deformed shape, which was quite challenging to track, but because of not tracking a circle, but tracking contours and having a threshold of area and aspect ratio, we were able to draw around the contour and mark a circle around it and get the centre coordinates.

![Comet in GIF 1](https://shivam.foo/images/ping-pong-ball-tracking-system/comet_in_gif_1.png)

![Comet in GIF 2](https://shivam.foo/images/ping-pong-ball-tracking-system/comet_in_gif_2.png)

![Ping Track GIF](https://shivam.foo/images/ping-pong-ball-tracking-system/ping_track.gif)


#### 4.4 Coordinates to Actual Distance
Now that you understand how we obtain the center coordinates of the ball, the next step is calculating the actual distance from these coordinates. This is where the calibration part comes into play.

We have the \(x, y\) coordinates of the circle with respect to the OpenCV window.

![Distance Relative 1](https://shivam.foo/images/ping-pong-ball-tracking-system/distance_relative_1.png)

Here, the values are:
- Green value (mid_value) = 112
- Red value (minimum_value) = 84

![Distance Relative 2](https://shivam.foo/_next/image?url=%2Fimages%2Fping-pong-ball-tracking-system%2Fdistance_relative_2.png&w=3840&q=75)

Using the above two images, we determine that:
- 640 pixels = 56 inches
- Therefore, each pixel = 0.0875 inches.

With the coordinates of the ball being \(223\) px, \(263\) px, we can calculate the distance as follows:
- Distance = \(223 \times 0.0875 = 19.5125\) inches.

Now, considering the vertical offset from the origin (the red value), we can determine the total distance from the origin:

![Distance Relative 4](https://shivam.foo/_next/image?url=%2Fimages%2Fping-pong-ball-tracking-system%2Fdistance_relative_4.png&w=3840&q=75)

- Total Distance = \(84 + 19.5125 = 103.5125\) inches.

As shown in the output screenshot above, this calculation provides an accurate distance measurement.

