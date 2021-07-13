import numpy as np

vertical = [0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0]
horizontal = [0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1,
              1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0]

#position given as (x, y, theta)
currentPos = [5, 7, -90]
nextPos = [15, 7, 0]

if (currentPos[1] > 17.5 and nextPos[1] > 17.5) or (currentPos[1] < 2.5 and nextPos[1] < 2.5):
    #move vertically first
    #imu.turning = True
    print("turning: " + str(0 + currentPos[2]))
    #turn bot to 0 degrees
    print("moving: " + str(currentPos[0] - nextPos[0]))
    #sendToArduino(0, currentPos[1] - nextPos[1])
    #imu.turning = False


