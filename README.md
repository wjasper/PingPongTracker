# PingPongTracker

Project Team members:-
1. Warren Jasper (wjasper@ncsu.edu)
2. Shivam Ghodke (sghodke@ncsu.edu)


Techstack:- OpenCV, Python, RaspberryPi, Picamera

Read about this on blog:- https://shivam.foo/blogs/ping-pong-ball-tracking-system

Watch youtube video in here:- 

## Table of Contents
1. [Understanding the Project](#understanding-the-project)
2. [Motivation](#motivation)
3. [Traditional Way](#traditional-way)
4. [Our Method](#our-method)
    - [Calibration](#calibration)
    - [Ball Tracking and Distance Calculation](#ball-tracking-and-distance-calculation)
    - [Challenges We Faced](#challenges-we-faced)
        - [Hardware Limitation for Processing in Real-Time](#hardware-limitation-for-processing-in-real-time)
        - [Speed and Shape of Ball Made it Impossible to Track Ball](#speed-and-shape-of-ball-made-it-impossible-to-track-ball)
        - [Ball Not Being Ball Shaped](#ball-not-being-ball-shaped)
    - [Coordinates to Actual Distance](#coordinates-to-actual-distance)



## 1. Understanding the Project
Calculating the distance at which the ball is going to have its first point of contact with the ground after being launched using a catapult.

![Objective Image](https://shivam.foo/_next/image?url=%2Fimages%2Fping-pong-ball-tracking-system%2Fobjective.png&w=3840&q=75)

## 2. Motivation
The reason behind doing this project is for data modeling, which is to collect training data so it could later be used by machine learning regression models.

![Motivation Image](https://shivam.foo/_next/image?url=%2Fimages%2Fping-pong-ball-tracking-system%2Ftable.jpg&w=3840&q=75)


## 3. Traditional Way
Lay an aluminum foil in the expected area where the ball is going to land for a particular configuration, launch the ball, identify the dent on the foil, and calculate the distance using a measuring tape that has been placed in parallel with the foil. 

This is a tedious process and takes a lot of time. It's a two-man job and not feasible when sampling for 10,000 data points.

![Traditional Way Image](https://shivam.foo/_next/image?url=%2Fimages%2Fping-pong-ball-tracking-system%2Ftraditional.jpg&w=3840&q=75)


## 4. Our Method
Using a Raspberry Pi with an HD camera mounted on it, powered by a power bank, the system can be operated using a remote desktop, making it highly mobile. 

Place the Raspberry Pi camera as shown in the picture below:

![Our Method Image](https://shivam.foo/_next/image?url=%2Fimages%2Fping-pong-ball-tracking-system%2Fr_setup.jpg&w=3840&q=75)

### 4.1. Calibration
Place a ruler scale: Align the scale with the green and red lines, and get the values on the tape in inches accordingly.

Here are the values:
- Green value (mid_value) = 112
- Red value (minimum_value) = 84

![Calibration Image](https://shivam.foo/_next/image?url=%2Fimages%2Fping-pong-ball-tracking-system%2Fcalib_window.png&w=3840&q=75)


### 4.2. Ball Tracking and Distance Calculation
After weeks of research, trials, and errors, and nearly losing all hope, my professor came up with a brilliant idea: background separation. 

What we do is take the first frame, convert it to black & white, and for each frame, we take the absolute difference with this background image.

#### Base Frame
![Base Frame](https://shivam.foo/_next/image?url=%2Fimages%2Fping-pong-ball-tracking-system%2Fbase_frame.png&w=3840&q=75)

#### Background Separation Process
![Background Separation](https://shivam.foo/_next/image?url=%2Fimages%2Fping-pong-ball-tracking-system%2Fbg_seperation.gif&w=3840&q=75)

#### Ball Tracked
![Ball Tracked](https://shivam.foo/_next/image?url=%2Fimages%2Fping-pong-ball-tracking-system%2Fball_tracked.png&w=3840&q=75)

#### Distance Output
![Distance Output](https://shivam.foo/_next/image?url=%2Fimages%2Fping-pong-ball-tracking-system%2Fdistance_output.png&w=3840&q=75)

### 4.3 Challenges We Faced

#### 4.3.1 Hardware Limitation for Processing in Real-Time
Initially, we wanted to process the frames in real-time. However, due to hardware limitations, the Raspberry Pi was unable to process the frames as soon as they were captured. Consequently, we decided to use post-processing, which involved first recording the video, storing the frames in a buffer, and then processing each frame one by one.

#### 4.3.2 Speed and Shape of the Ball Made It Impossible to Track
The second challenge we encountered was that the ball was moving at a very high pace, making it visible for only 1-3 frames. This speed hindered the program's ability to perform any object detection. We even tried using a plain dark-colored background covered with a cloth, but despite this, the program struggled to track the ball due to its small size and rapid movement. 

After weeks of research, trials, and errors, and nearly losing all hope, my professor came up with a brilliant idea.

#### Important Note
OpenCV is not compatible with Raspberry Pi for accessing the camera object, thus need to use PiCamera library.

There is one caveat when shooting the ball: there should be no movement in the background. While the background can be cluttered, it’s crucial that there are no moving objects in the frame, as this movement would be captured by the absolute difference method.

#### 4.3.3 Ball Not Being Ball Shaped
When the ball travels at a faster pace, it may appear deformed, resembling more of a comet than a sphere.

![Comet Shape](https://shivam.foo/_next/image?url=%2Fimages%2Fping-pong-ball-tracking-system%2Fcomet_shape.jpeg&w=3840&q=75)

Unfortunately, no existing articles, blogs, or OpenCV functions helped us in this regard. 

This [article](https://pyimagesearch.com/2015/09/14/ball-tracking-with-opencv/) provided a good starting point, but it could not track the ball effectively due to its speed and the deformation of its shape, as it was only visible for 1-3 frames.

To tackle this challenge, we decided to detect the contours in the image after subtraction, measure the area of the contour, and if it was around 100px with an aspect ratio of 3 (indicating a more oval shape than a boxy shape), we would draw a circle around it and start tracking the center coordinates.

As seen in the images below, the ball is not a perfect circle but a deformed shape, which posed quite a challenge for tracking. However, by focusing on contour detection and setting thresholds for area and aspect ratio, we were able to draw around the contour, mark a circle, and obtain the center coordinates.

![Comet in GIF 1](https://shivam.foo/_next/image?url=%2Fimages%2Fping-pong-ball-tracking-system%2Fcomet_in_gif_1.png&w=3840&q=75)

![Comet in GIF 2](https://shivam.foo/_next/image?url=%2Fimages%2Fping-pong-ball-tracking-system%2Fcomet_in_gif_2.png&w=3840&q=75)

![Ping Track GIF](https://shivam.foo/_next/image?url=%2Fimages%2Fping-pong-ball-tracking-system%2Fping_track.gif&w=3840&q=75)


#### 4.4 Coordinates to Actual Distance
Now that you understand how we obtain the center coordinates of the ball, the next step is calculating the actual distance from these coordinates. This is where the calibration part comes into play.

We have the \(x, y\) coordinates of the circle with respect to the OpenCV window.

![Distance Relative 1](https://shivam.foo/_next/image?url=%2Fimages%2Fping-pong-ball-tracking-system%2Fdistance_relative_1.png&w=3840&q=75)

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


| **Description**   | **Link**                                                                                         |
|-------------------|--------------------------------------------------------------------------------------------------|
| **Portfolio website**     | [shivam.foo](https://shivam.foo)                                                                |
| **Important**     | Looking for entry level SWE roles, graduating @NC State in computer science in  May 2025                                                          |
| **GitHub**        | [nuttysunday](https://github.com/nuttysunday)       |
| **Blog Link**     | [shivam.foo/blogs/ping-pong-ball-tracking-system](https://shivam.foo/blogs/ping-pong-ball-tracking-system)                          |
| **Video Link**    | [Youtube Video](https://youtu.be/_IoQ6Dux8g8?si=CqIbvoVEVakvuekcg)                                     |
| **LinkedIn**      | [Linkedin Profile](https://www.linkedin.com/in/shivam-ghodke/)                                             |
| **Resume**        | [Resume](https://drive.google.com/file/d/1OC_mcMHkBaDhWbKEMfsnLY-uBS8Xee7G/view)              |
| **Twitter**       | [Twitter/X account](https://x.com/sundaycide)                                                                |

