# raytheonRobot
The code in this respository was written as a part of my Summer 2021 internship with Raytheon

The project was to create an autonomous robot to play minature-croquet, navigating a course, recognizing numbers, and intereacting with a ball
The highlevel design features a Raspberry pi as the robot's central computer and an Arduino for sensor interfacing. 
This repositiory holds code for each as well as some code that enables communciation between the two. 

Some highlights and achievements include:
  OpenCV code to recognize a green tennis ball and draw a circle around it
  A regression that takes the radius of this circle to estimate its distance from the robot as well as the angle
  Code that interfaces with IMU and runs on separate thread to update the robot's position and bearing constantly
  A state-machine high-level implementation to control robot's lifecycle and operational phases
  Code that runs on arduino to interface with ultrasonic sensor, motors, IR sensor, and Raspberry Pi
  
