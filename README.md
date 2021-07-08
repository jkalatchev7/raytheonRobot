# raytheonRobot
Here is a bunch of code that should turn into the final code

The file called runfile.py is what will be run on the raspberry pi. It starts by initializing some variables and the serial connection and then acts like a state machine

The accelerometer folder has two files. The imu.py is the class that has everything for working with the accelerometer. It has instance variables posX, posY, and anglez which will be updated through the imu's update methods when we are moving

The file test.py has a few functions: the first is to take a picture pass it through openCV and pick out a green ball and return its distance and angle. The second and third are just for taking pictures

The code in the Arduino folder is the sketch that will run on the arduino. The motorFunctions is just a series of helper functions I put in another file to make it easier
This code has a lot of parts but the most important is probably the Serial read stuff because that's how we take in information from the raspi. You can see that the first part of the serial read basically gets the key word command (move, turn, sequ, etc..) which it then acts on and returns done when it is finished so the state machine in the raspi knows to move on.

I put this code in github to make sure we don't lose progress if a raspberry pi gets messed up plus it is easier to update and share
