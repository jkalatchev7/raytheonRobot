import cv2
import numpy as np
import imutils
import cameraTest as ct
from datetime import datetime
from imutils.perspective import four_point_transform, order_points
from scipy import ndimage

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
    img = imutils.resize(frame, height=500)
    hsv = cv2.cvtColor(img, cv2.COLOR_HSV2RGB)
    cv2.imwrite('hoopPic_og.png', hsv)
    l_b = np.array([102, 102, 102])
    u_b = np.array([153, 255, 255])

    mask = cv2.inRange(hsv, l_b, u_b)
    # erodes edges getting rid of small patches
    mask = cv2.erode(mask, None, iterations=5)
    # mask2 = cv2.erode(mask2, None, iterations=5)
    mask = cv2.dilate(mask, None, iterations=5)
    # mask2 = cv2.dilate(mask2, None, iterations=5)

    # finds contours or shapes in image
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    if len(cnts) == 0:
        return 0
    c = max(cnts, key=cv2.contourArea)
    rect = cv2.minAreaRect(c)
    area = rect[1][0] * rect[1][1]
    if area < 2000:
        print("None found")

    box = cv2.boxPoints(((rect[0][0], rect[0][1]), (rect[1][0] * .7, rect[1][1] * .7), rect[2]))
    box = np.int0(box)
    box = order_points(box)
    box = box.astype(int)
    output = four_point_transform(hsv, box.reshape(4, 2))
    cv2.drawContours(img, [box], 0, (0, 0, 255), 2)
    # change img and img2 to res and res2 to make adjustments and match colors using sliders
    gray1 = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)

    mask2 = cv2.inRange(gray1, 95, 255)
    mask2 = 255 - mask2

    cnts2 = cv2.findContours(mask2.copy(), cv2.RETR_EXTERNAL,
                             cv2.CHAIN_APPROX_SIMPLE)
    cnts2 = imutils.grab_contours(cnts2)
    if len(cnts2) == 0:
        return 0
    c2 = max(cnts2, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(c2)

    rectang = cv2.boxPoints(((x + w * .5, y + h * .5), (w * 1.2, h * 1.2), 0))
    rectang = np.int0(rectang)
    rectang = order_points(rectang)
    rectang = rectang.astype(int)
    outBR = output
    cv2.rectangle(output, (x, y), (x + w, y + h), (0, 255, 0), 2)

    mask2 = four_point_transform(mask2, rectang.reshape(4, 2))
    mask2 = 255 - mask2

    mask2 = imutils.resize(mask2, 28, 28)
    cv2.imwrite("number.png", mask2)
    return 1
    
hoop_pic()

