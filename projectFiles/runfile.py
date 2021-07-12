import threading

import test
import serial
import io
import time
from signal import signal, SIGTERM, SIGHUP, pause
from rpi_lcd import LCD

import matplotlib.pyplot as plt
from accelerometer import imu

hold = imu.imu()
hold.initialize()
hold.calibrate()

x = threading.Thread(target=hold.update, args=[0])
state = ""
nextState = "Resting"
startHoop = 1
nextHoop = 0
hoops = [[3, 7], [17, 7], [17, 3], [3, 3], [7, 5], [13, 5]]
pin = [10, 5]
# lcd = LCD()
# lcd.clear()
x.start()

def safe_exit(signum, frame):
    exit(1)


# signal(SIGTERM, safe_exit)
# signal(SIGHUP, safe_exit)
# lcd.text("State:", 1)
# lcd.text(state, 2)

try:
    ser = serial.Serial(  # set parameters, in fact use your own :-)
        port='/dev/ttyACM0', baudrate=9600,
        bytesize=serial.SEVENBITS,
        parity=serial.PARITY_EVEN,
        stopbits=serial.STOPBITS_ONE,
        timeout=1
    )
    ser.isOpen()  # try to open port, if possible print message and proceed with 'while True:'
    print("port is opened!")

except IOError:  # if port is already opened, close it and open it again and print message
    ser.close()
    ser.open()
    print("port was already open, was closed and opened again!")

time.sleep(.1)
ser.flushInput()


def sendToArduino(a, b):
    if (a == 0):
        strr = "move " + str(int(b))
        print(strr)
        ser.write(bytes(strr, 'utf-8'))
        ser.flush()
    elif (a == 1):
        strr = "turn " + str(int(b))
        print(strr)
        ser.write(bytes(strr, 'utf-8'))
        ser.flush()
    elif (a == 2):
        strr = "sequ "
        print(strr)
        ser.write(bytes(strr, 'utf-8'))
        ser.flush()
    elif (a == 3):
        strr = "coll"
        print(strr)
        ser.write(bytes(strr, 'utf-8'))
        ser.flush()


def arduinoRead():
    return ser.readline().rstrip().decode('utf-8')


while 1:
    state = nextState
    #lcd.text(state, 2)
    print("Entering State: " + state)
    if state == "BallSearch":
        print("Searching for ball...")
        ar = test.ball_search()
        while (ar == None):
            print("none found")
            hold.turning = True
            sendToArduino(1, 40)

            time.sleep(3)
            ar = test.ball_search()
        # sends turn command and waits until turning is finished
        sendToArduino(1, ar[3] + 6)
        inp = arduinoRead()
        print(inp)
        while inp != "done":
            inp = arduinoRead()
            print(inp)

        # sends move command and waits until moving is complete
        hold.turning = False
        sendToArduino(0, ar[1])
        inp = arduinoRead()
        print(inp)
        while inp != "done":
            inp = arduinoRead()
            print(inp)

        # sends command to recover ball
        hold.turning = True
        sendToArduino(3, 0)
        inp = arduinoRead()
        print(inp)
        while inp != "collected":
            inp = arduinoRead()
            print(inp)
        print("Ball Recovered")
        nextState = "Sequence"

    elif state == "Resting":
        inp = arduinoRead()
        while inp != "done":
            print(inp)
            time.sleep(.01)
            if inp == 'turn':
                hold.turning = True
                print("turning")
            if inp == 'move':
                hold.turning = False
                print("moving forward")
            inp = arduinoRead()
        nextState = "over"

    elif state == "getInFrontOfHoop":
        hoop = nextHoop
        if hoop == startHoop:
            nextState = "pinSearch"
        else:  # When we are in front of hoop
            # bunch of movement
            nextState = "VerifyNumber"

    elif state == "VerifyNumber":
        print("Taking picture... ")
        test.hoop_pic()
        print("Picture Taken, Getting number...")
        # a  = numverification()
        # if a == nextHoop:
        nextState = "Sequence"
        # else:
        # god knows

    elif state == "Sequence":
        # Get distance to flag
        # Activate motors until black crease
        nextHoop = nextHoop % 6
        nextHoop += 1
        nextState = "circleHoop"

        sendToArduino(2, 0)
        inp = arduinoRead()
        print(inp)
        while (inp != "circle"):
            inp = arduinoRead()
            print(inp)
        nextState = "circleHoop"
    elif state == "circleHoop":
        inp = arduinoRead()
        print(inp)
        while (inp != "done"):
            inp = arduinoRead()
            print(inp)
        # check which hoop we are at... preprogram which direction to go depending on where we want robot to be facing after
        # turn 90, move past hoop, turn -90 move past hoop, turn -90
        nextState = "ballSearch"
    elif state == "pegSearch":
        # Look for peg
        nextState = "shootAtPeg"

    else:
        hold.stop = True
        x.join()
        # all of this below is for plotting
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1)
        t = list(range(len(hold.acc)))
        fig.suptitle('A tale of 2 subplots')
        ax1.plot(t, hold.acc, '.-')
        ax1.set_ylabel("Accel x")
        ax2.plot(t, hold.vell, '.-')
        ax2.set_ylabel("Vel y")
        ax3.plot(t, hold.dist, '.-')
        ax3.set_ylabel("Dist (in)")
        fig.show()
        figure, (ax4, ax5) = plt.subplots(2, 1)
        fig.suptitle('A tale of 2 subplots')
        ax4.plot(t, hold.alpha, '.-')
        ax4.set_ylabel("Omega (deg/s)")
        ax5.plot(t, hold.omega, '.-')
        ax5.set_ylabel("Theta (deg)")
        figure.show()
        fig1, (ax7) = plt.subplots(1, 1)
        ax7.plot(hold.cordX[::5], hold.cordY[::5], 'o-')
        ax7.set_xlabel("X (feet)")
        ax7.set_ylabel("Y (feet)")
        ax7.set_xlim(0, 2)
        ax7.set_ylim(0, 2)
        fig1.show()
        # print final positions which are stored in the object we've created
        print("Final Positions: " + str(round(hold.posX * 12, 1)) + ", " + str(round(hold.posY * 12, 1)))
        print("Final Orientation: " + str(-1 * round(hold.angleZ, 1)) + " degrees")
        print("over")
        ser.close()
        break
    time.sleep(.5)
