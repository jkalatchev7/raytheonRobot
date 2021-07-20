import threading
import tkinter
from random import randint

import test
import serial
import io
import time
from signal import signal, SIGTERM, SIGHUP, pause
from rpi_lcd import LCD

import matplotlib.pyplot as plt
from accelerometer import imu

root = tkinter.Tk()
root.title("Robot Visual")
label = tkinter.Label(root, text="hello world")
labelA = tkinter.Label(root, text= "temp")
root.geometry("300x500")

canv = tkinter.Canvas(root, height=400, width=200, bg="green")
robot = canv.create_image(10,10, image=tkinter.PhotoImage(file='accelerometer/robot.png'))
label.pack()
labelA.pack()
canv.pack()
root.update()
state = ""
nextState = "testTurn"
startHoop = 1
passStart = False
nextHoop = 1
hoops = [[3., 1., 90], [3., 15., 90], [7., 19., -90], [7., 5., -90], [5., 5., 90], [5., 15., -90]]
pin = [5, 10]
# lcd = LCD()
# lcd.clear()


def wait_for_done():
    inp = arduinoRead()
    #canv.move(robot, 10, 0)
    #root.update()
    while (inp != 'done'):
        print(inp)
        inp = arduinoRead()

def safe_exit(signum, frame):
    exit(1)


# signal(SIGTERM, safe_exit)
# signal(SIGHUP, safe_exit)
# lcd.text("State:", 1)
# lcd.text(state, 2)

try:
    ser = serial.Serial(  # set parameters, in fact use your own :-)
        port='/dev/ttyACM1', baudrate=9600,
        bytesize=serial.SEVENBITS,
        parity=serial.PARITY_EVEN,
        stopbits=serial.STOPBITS_ONE,
        write_timeout = 0,
        timeout=None,
        rtscts = False,
        xonxoff  = False
    )
    ser.isOpen()  # try to open port, if possible print message and proceed with 'while True:'
    print("port is opened!")

except IOError:  # if port is already opened, close it and open it again and print message
    ser.close()
    ser.open()
    print("port was already open, was closed and opened again!")
hold = imu.imu(7, 0, 90)
hold.initialize()
hold.calibrate()

x = threading.Thread(target=hold.update, args=[0])
x.start()
time.sleep(.1)
ser.flushInput()


def sendToArduino(a, b):
    strr = ""
    if (a == 0):
        strr = "move " + str(float(b))

    elif (a == 1):
        strr = "turn " + str(int(b))

    elif (a == 2):
        strr = "sequ "

    elif (a == 3):
        strr = "coll "

    elif (a == 4):
        if (b == 0):
            strr = "turL "
        else:
            strr = "turR "  
        
    elif (a == 5):
        strr = "stop "
        
    elif (a == 6):
        strr = "forw"

    print("Sending Command: " + strr)
    ser.write(bytes(strr, 'utf-8'))
    ser.flush()
    
    
def arduinoRead():
    return ser.readline().rstrip().decode('utf-8')

def turnTo(angle):
    hold.turning = True
    if (hold.angleZ < angle):
        sendToArduino(4, 0)
    else:
        sendToArduino(4, 1)
        
    while (round(hold.angleZ) > (angle + 4) or round(hold.angleZ) < (angle - 4)):
        labelA['text'] = str(round(hold.angleZ)) + "  "+ str(round(hold.posX, 2)) + "  " + str(round(hold.posY, 2))
        labelA.pack()
        root.update()
        time.sleep(.01)
    sendToArduino(5, 0)
    time.sleep(.8)
    labelA['text'] = str(round(hold.angleZ))
    labelA.pack()
    root.update()

def moveAmount(dist):
    hold.turning = False
    curr = hold.dist_gone

    distToGo = dist
    sendToArduino(6, 0)
        
    while (hold.dist_gone < (curr + distToGo)):
        print(arduinoRead())
        labelA['text'] = str(round(hold.angleZ)) + "  "+ str(round(hold.posX, 2)) + "  " + str(round(hold.posY, 2))
        labelA.pack()
        root.update()
        time.sleep(.01)
    sendToArduino(5, 0)
    time.sleep(.5)
    labelA['text'] = str(round(hold.angleZ)) + "  "+ str(round(hold.posX, 2)) + "  " + str(round(hold.posY, 2))
    labelA.pack()
    root.update()

while 1:
    state = nextState
    label['text'] = "State: " + nextState
    root.update()
    
    #lcd.text(state, 2)
    print("Entering State: " + state)
    if state == "BallSearch":
        print("Searching for ball...")
        ar = test.ball_search()
        while (ar == None):
            print("none found")
            hold.turning = True
            sendToArduino(1, 40)
            wait_for_done()
            ar = test.ball_search()
        # sends turn command and waits until turning is finished
        sendToArduino(1, ar[3])
        wait_for_done()

        # sends move command and waits until moving is complete
        hold.turning = False
        sendToArduino(0, ar[1])
        wait_for_done()
        # sends command to recover ball
        hold.turning = True
        sendToArduino(3, 0)
        inp = arduinoRead()
        while inp != "done":
            print(inp)
            time.sleep(.01)
            if inp == 'turn':
                hold.turning = True
                print("Arduino -> turning")
            if inp == 'move':
                hold.turning = False
                print("Arduino -> moving forward")
            inp = arduinoRead()
        print("Ball Recovered")
        nextState = "getInFrontOfHoop"

    elif state == "Resting":
        inp = arduinoRead()
        while inp != "done":
            print(inp)
            time.sleep(.01)
            if inp == 'turn':
                hold.turning = True
                print("Arduino -> turning")
            if inp == 'move':
                hold.turning = False
                print("Arduino -> moving forward")
            inp = arduinoRead()
        nextState = "over"

    elif state == "getInFrontOfHoop":
        hoop = nextHoop
        print("Going for Hoop #" + str(hoop))
        if hoop == startHoop and passStart:
            nextState = "pinSearch"
            continue
        
        else:
            if hoop == startHoop:
                passStart = True
            curr = [hold.posX, hold.posY, hold.angleZ]
            nextH = hoops[hoop - 1]
            print(nextH)
            print(curr)
            hold.turning = True
            if (curr[0] < nextH[0]):
                sendToArduino(1, -1 * curr[2])
                #face right
            elif(curr[0] > nextH[0]):
                sendToArduino(1, 180 - curr[2])
                #face left
            #turn go horizontally
            wait_for_done()

            #now we move horizontally
            hold.turning = False
            sendToArduino(0, abs(hold.posX - nextH[0]))
            wait_for_done()
            hold.turning = True
            if (hold.posY > nextH[1]):
                sendToArduino(1, 270 - hold.angleZ)
                wait_for_done()
            else:
                sendToArduino(1, 90 - hold.angleZ)
                wait_for_done()

            hold.turning = False
            sendToArduino(0, abs(hold.posY - nextH[1]))
            wait_for_done()
            hold.turning = True
            sendToArduino(1, nextH[2] - hold.angleZ)
            wait_for_done()
            print("finished")

            nextState = "VerifyNumber"

    elif state == "VerifyNumber":
        print("Taking picture... ")
        #test.hoop_pic()
        print("Picture Taken, Getting number...")
        # a  = numverification()
        # if a == nextHoop:
        nextState = "over"
        # else:
        # god knows

    elif state == "Sequence":
        # Get distance to flag
        # Activate motors until black crease
        nextHoop = nextHoop % 6
        nextHoop += 1

        sendToArduino(2, 0)
        inp = arduinoRead()
        print(inp)
        while (inp != "done"):
            if inp == 'turn':
                hold.turning = True
                print("Arduino -> turning")
            if inp == 'move':
                hold.turning = False
                print("Aruino -> moving forward")
            inp = arduinoRead()
            print(inp)
        nextState = "BallSearch"
    elif state == "pegSearch":
        # Look for peg
        nextState = "shootAtPeg"
    elif state == "testTurn":
        #sendToArduino(5,0)
        time.sleep(1)
        moveAmount(1)
        wait_for_done()
        turnTo(180)
        time.sleep(1)

        nextState = "over"
    
    elif state == "testForw":
        moveAmount(1.2)
        nextState = "over"
        
    else:
        hold.stop = True
        x.join()
        # all of this below is for plotting
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1)
        t = list(range(len(hold.acc)))
        fig.suptitle('Linear Motion')
        ax1.plot(t, hold.acc, '.-')
        ax1.set_ylabel("Accel x (ft/s^2)")
        ax2.plot(t, hold.vell, '.-')
        ax2.set_ylabel("Vel y (ft/s)")
        ax3.plot(t, hold.dist, '.-')
        ax3.set_ylabel("Dist (ft)")
        fig.show()
        figure, (ax4, ax5) = plt.subplots(2, 1)
        fig.suptitle('Angular motion')
        ax4.plot(t, hold.alpha, '.-')
        ax4.set_ylabel("Omega (deg/s)")
        ax5.plot(t, hold.omega, '.-')
        ax5.set_ylabel("Theta (deg)")
        figure.show()
        fig1, (ax7) = plt.subplots(1, 1)
        fig1.suptitle('Movement on Plane')
        ax7.plot(hold.cordX, hold.cordY, 'o-')
        ax7.set_xlabel("X (feet)")
        ax7.set_ylabel("Y (feet)")
        ax7.set_xlim(0, 10)
        ax7.set_ylim(0, 20)
        #ax7.set_aspect('equal', adjustable="datalim")
        fig1.show()
        
        # print final positions which are stored in the object we've created
        print("Final Positions: " + str(round(hold.posX * 12, 1)) + ", " + str(round(hold.posY * 12, 1)))
        print("Final Orientation: " + str(round(hold.angleZ, 1)) + " degrees")
        print("over")
        ser.close()
        break
    time.sleep(.5)
