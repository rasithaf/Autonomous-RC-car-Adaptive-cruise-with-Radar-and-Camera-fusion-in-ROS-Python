# Autonomous-RC-car-Adaptive-cruise-with-Radar-and-Camera-fusion-in-ROS-Python

This project was built on Jetson Nano developer kit, RC Car, and Perception SSR 2.0 Radar.

I tested the project on the following environment: (If you are not using ROS environment, remove the ros commands in the code) 

Ubuntu 18.04,
Python,
ROS Melodic,
Numpy,
OpenCV

Camera:

• Used logitech usb cam

• It follows a Red dot

• Our RC car has steering angle range between 55 and 145

• wheel position: 55 -> left most, 100 -> straight, 145 -> right most

• frame has been segmented to 5 main positions

Cruise:

• Used Perceptin Radar SSR 2.0 

• It tracks objects between -15 and 15 degrees

• Get the distance of the closest object in mentioned angle

• Get the relative speed of that object

• It determines pwm as prioratized

Servo:

• Needs "adafruit_servokit" module

Use https://github.com/rasithaf/Autonomous-Car-Obstacle-detection-and-avoidance-using-Radar/blob/master/README.md for Radar settings

Output Video: See Adaptive cruise (Radar+Camera fusion) in https://rasithaf.wixsite.com/mysite/videos
