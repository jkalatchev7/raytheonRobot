import cv2
import numpy as np
import imutils
import cameraTest as ct
from datetime import datetime
PRINT = False
import time

def ball_search():
    cap = cv2.VideoCapture(-1)
    cap.set(3, 1280)
    cap.set(4, 720)
    _, frame = cap.read()
    cap.release()
    cv2.imwrite('preresult.jpg', frame)
    start = datetime.now()
    img = frame
    frame[1:325, :, :] = 0
    frame = cv2.GaussianBlur(frame, (11, 11), 0)
    l_b = np.array([0, 28, 23])
    u_b = np.array([255, 255, 255])
    
    mask = cv2.inRange(frame, l_b, u_b)

    tracking = cv2.bitwise_and(frame, frame, mask=mask)
    mask = cv2.erode(tracking, None, iterations=20)
    mask = cv2.dilate(mask, None, iterations=20)
    cv2.imwrite('mask.jpg', mask)
    circles = cv2.HoughCircles(cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY), cv2.HOUGH_GRADIENT, 2, 120, param1=120, param2=50, minRadius=10, maxRadius=0)
    for i in circles:
        #cv2.circle(img, (5, 10), 20, (0, 255, 0), 5)
        img = cv2.imread('preresult.jpg')
        cv2.circle(img, (int(i[0][0]), int(i[0][1])), int(i[0][2]), (0, 255, 0), 5)
        dist = 4.155692 + (38672870 - 4.155692) / ((1 + i[0][2] / 0.0003913803) ** 1.197)
        #print("Image 1 dist: " + str(dist))

    angle = (int(i[0][0])-640) / (dist**.1) / 17.7 * -1
    arr = (i[0][2], dist, angle)
    cv2.line(img, (640, int(i[0][1])), (int(i[0][0]), int(i[0][1])), (0, 0, 0))
    cv2.imwrite('result.png', img)
    return arr
    
    
def take_pic():
    cap = cv2.VideoCapture(-1)
    cap.set(3, 1280)
    cap.set(4, 720)
    _, frame = cap.read()
    frame[1:325, :, :] = 0
    date_string = datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
    name = date_string + ".jpg"
    cv2.imwrite(name, frame)
    cap.release()

def hoop_pic():
    cap = cv2.VideoCapture(-1)
    cap.set(3, 1280)
    cap.set(4, 720)
    _, frame = cap.read()
    name = "hoopPic.png"
    cv2.imwrite(name, frame)

