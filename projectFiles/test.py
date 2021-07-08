import cv2
import numpy as np
import imutils
import cameraTest as ct
import serialTestA
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
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    l_b = np.array([51, 75,26])
    u_b = np.array([83, 255, 247])
    mask = cv2.inRange(hsv, l_b, u_b)
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    center = None
    if len(cnts) > 0:

        # find the largest contour in the mask, then use
        # it to compute the minimum enclosing circle and
        # centroid
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        if M["m00"] == 0:
            return None
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        dis = 5.155692 + (38672870 - 5.155692) / ((1 + radius / 0.0003913803) ** 1.197)

        #print("Image 1 distance: " + str(dis))
        # only proceed if the radius meets a minimum size
        if radius > 30:
            # draw the circle and centroid on the frame,
            # then update the list of tracked points
            cv2.circle(img, (int(x), int(y)), int(radius),
                       (0, 255, 255), 2)
            cv2.circle(img, center, 5, (0, 0, 255), -1)
            cv2.line(img, (640, int(y)), (int(x), int(y)), (0, 0, 0))
            # pts.appendleft(center)
            t  = datetime.now() - start
            arr = [radius, dis, int(x)-640, (int(x)-640) / (dis**.1) / 17.7]
            cv2.imwrite('result.jpg' , img)
            return arr
        if PRINT:
            print("Image 1:")
            print((int(x), int(y)))
            print(radius)
            print((int(x) - 640) / (dis))
def take_pic():
    cap = cv2.VideoCapture(-1)
    cap.set(3, 1280)
    cap.set(4, 720)
    _, frame = cap.read()
    date_string = datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
    name = "practicePics/" + date_string + ".jpg"
    cv2.imwrite(name, frame)

def hoop_pic():
    cap = cv2.VideoCapture(-1)
    cap.set(3, 1280)
    cap.set(4, 720)
    _, frame = cap.read()
    name = "hoopPic.png"
    cv2.imwrite(name, frame)

# time.sleep(5)
# print("Starting")
# for i in range(1, 10):
#     print("taking Pic")
#     time.sleep(2)
#     take_pic()
# ar = ball_search()
#print(ar)
#serialTestA.sendToArduino(0,ar[1],ar[3])