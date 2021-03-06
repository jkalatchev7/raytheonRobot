import threading
import tkinter as tk
from tkinter import *
from random import randint
import test
import serial
import io
import time
from pynput.keyboard import Key, Listener
from signal import signal, SIGTERM, SIGHUP, pause
from rpi_lcd import LCD

import matplotlib.pyplot as plt
from accelerometer import imu
window = tk.Tk()
window.title("Robot Croquet GUI")
window.configure(background = 'light green')
width= window.winfo_screenwidth() 
height= window.winfo_screenheight() - 20
#setting tkinter window size
window.geometry("%dx%d" % (width, height))

print("Geometry set")

def make_label(master, x, y, h, w, *args, **kwargs):
    f = Frame(master, height=h, width=w)
    f.pack_propagate(0) # don't shrink
    f.place(x=x, y=y)
    label = Label(f, *args, **kwargs, font=("Arial", 20))
    label.pack(fill=BOTH, expand=1)
    return label


#create intial map
cHeight = height * .045
cwidth = cHeight * 1
outside = make_label(window, height * 0.05 - 5, height * 0.05 - 5, height * 0.9 + 10, height * .45 + 10, background='black')
inside = make_label(window, height * 0.05, height * 0.05, height * 0.9, height * .45, background='light green')
hoop2 = make_label(window, height * (0.05 + .045 * 23/ 12), height * (0.05 + .045 * 50/ 12), cHeight, cwidth, text='2', background='red')
hoop3 = make_label(window, height * (0.45 - .045 * 23 /12), height * (0.05 + .045 * 50/ 12), cHeight, cwidth, text='3', background='red')
hoop6 = make_label(window, height * 0.25, height * (0.05 + .045 * 81/ 12), cHeight, cwidth, text='6', background='red')
peg = make_label(window, height * 0.25, height * 0.5, cHeight, cwidth, text='peg', background='light blue')
hoop5 = make_label(window, height * 0.25, height * (0.95 - .045 * 81/ 12), cHeight, cwidth, text='5', background='red')
hoop1 = make_label(window, height * (0.05 + .045 * 23/ 12), height * (0.95 - .045 * 50/ 12), cHeight, cwidth, text='1', background='red')
hoop4 = make_label(window, height * (0.45 - .045 * 23/12), height * (0.95 - .045 * 50/ 12), cHeight, cwidth, text='4', background='red')

#array for hoops

hoop_arr = [hoop1, hoop2, hoop3, hoop4, hoop5, hoop6, peg]

blue = make_label(window, 250, 1300, 70, 70, background='blue')
red = make_label(window, 450, 1300, 70, 70, background='red')

yellow = make_label(window, 650, 1300, 70, 70, background='yellow')
# black1 = make_label(window, 70, height * 0.05, 5, height * 0.45, background='red')
# black2 = make_label(window, 70, height * .95, 5, height * 0.45, background='black')
# black3 = make_label(window, 70, height * 0.05, height * 0.9, 5, background='black')
# black4 = make_label(window, 959, 110, height * 0.9, 5, background='black')
#    
current_action = make_label(window, 1010, 120, 50, 700, text = "Current Actions: ", background = "red")
current_command = make_label(window, 1010, 220, 50, 700, text = "Current Command: ", background = "white")
current_state = make_label(window, 1010, 320, 50, 700, text = "Current state: ", background = "white")
current_position = make_label(window, 1010, 420, 50, 700, text = "Current Position: ", background = "white")
print("labels Made")



ball_img = Label(text = "Ball Image...")
ball_img.pack()
ball_img.place(width = 640, height = 320, x = 1010, y = 500)
hoop_num = Label(text = "Hoop Number...")
hoop_num.pack()
hoop_num.place(width = 224, height = 224, x = 610, y = 548)

window.update()
#to update the image of the bot in real time change the x and y fields in a while loop 

#we can add the matlab plots, just will require extra code see links on how to do that 


state = ""
nextState = "getInFrontOfHoop"
startHoop = 2
passStart = False
nextHoop = 2

# lcd = LCD()
# lcd.clear()

try:
    current_action['text'] = "Opening Port..."
    window.update()
    ser = serial.Serial(  # set parameters, in fact use your own :-)
        port='/dev/ttyACM0', baudrate=9600,
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

    ser.open()
    print("port was already open, was closed and opened again!")

def empty_serial():
    while ser.in_waiting > 0:
        ser.readline()

def on_press(key):

    if (key == Key.left):
        sendToArduino(4, 0)
        current_action['text'] = "Manual Control: Turning Left"

    elif (key == Key.right):
        sendToArduino(4, 1)
        current_action['text'] = "Manual Control: Turning Right"

    elif (key == Key.up):
        sendToArduino(6, 0)
        current_action['text'] = "Manual Control: Moving Forward"

    elif (key == Key.enter):
        sendToArduino(5, 0)
        current_action['text'] = "Manual Control: Stop"
        print("enter")
        #stop
    elif (key == Key.esc):
        current_action['text'] = "Exiting Manual Control..."
        return False
 
    print(key)
    time.sleep(.2)
    
def activate():
    with Listener(on_press=on_press) as listener:
        listener.join()


def wait_for_done():
    print("waiting for done")
    inp = arduinoRead()
    #canv.move(robot, 10, 0)
    #root.update()
    while (inp != 'done'):
        print(inp)
        current_position['text'] = "Current Angle: " + str(hold.angleZ)
        window.update()
        inp = arduinoRead()

def safe_exit(signum, frame):
    exit(1)


# signal(SIGTERM, safe_exit)
# signal(SIGHUP, safe_exit)
# lcd.text("State:", 1)
# lcd.text(state, 2)



current_action['text'] = "Initializing IMU..."
window.update()
hold = imu.imu(3, 20, 270)
hold.initialize()
pic = PhotoImage(file = 'bot.png')
bot_img = Label(image = pic)
bot_img.pack()
xL = (height * (0.05 + 0.045 * hold.posX) - 25)
print(height)
yL = height * (.95 - .045 * hold.posY) - 33
print(xL)
print(yL)
bot_img.place(width = 50, height = 67, x = xL , y = yL) 
current_action['text'] = "Calibrating IMU..."
window.update()
hold.calibrate()

x = threading.Thread(target=hold.update, args=[0])
x.start()
time.sleep(.1)


def sendToArduino(a, b):
    strr = ""
    if (a == 0):
        strr = "move " + str(int(b))

    elif (a == 1):
        strr = "turn " + str(int(b))

    elif (a == 2):
        if (b == 0):
            strr = "sequ "
            current_action['text'] = "Lining up with hoop"
        elif (b == 1):
            strr = "seqb "
            current_action['text'] = "Approaching Hoop and Deploying Ball"

        elif (b == 2):
            strr = "seqc "
            current_action['text'] = "Moving Past Hoop"

    elif (a == 3):
        strr = "coll "+ str(round(b, 2))
        current_action['text'] = "Collecting Ball"

    elif (a == 4):
        if (b == 0):
            strr = "turL "
        else:
            strr = "turR "  
        
    elif (a == 5):
        strr = "stop "
        
    elif (a == 6):
        strr = "forw"
    
    elif (a == 7):
        if (b == 0):
            strr = "armU"
        else:
            strr = "armD"
        

    print("Sending Command: " + strr)
    current_command['text'] = "Current Command: " + strr
    window.update()
    ser.write(bytes(strr, 'utf-8'))
    ser.flush()
    
    
def arduinoRead():
    return ser.readline().rstrip().decode('utf-8')

def turnTo(angle):
    hold.turning = True
    print("Turning from " + str(hold.angleZ) +" to " + str(angle))
    current_action['text'] = "Turning from " + str(hold.angleZ) +" to " + str(angle)
    if (hold.angleZ < angle):
        sendToArduino(4, 0)
    else:
        sendToArduino(4, 1)
        
    while (round(hold.angleZ) > (angle + 2) or round(hold.angleZ) < (angle - 2)):
        current_position['text'] = str(round(hold.angleZ)) + "  "+ str(round(hold.posX, 2)) + "  " + str(round(hold.posY, 2))
        window.update()
        time.sleep(.01)
    sendToArduino(5, 0)
    print("stopped")
    time.sleep(.8)
   
    current_position['text'] = str(round(hold.angleZ))
    window.update()


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




hoop_arr[startHoop - 1]['background'] = "yellow"
sendToArduino(7, 0)
time.sleep(1)


while 1:
    state = nextState
    current_state['text'] = "State: " + nextState
    window.update()
    time.sleep(1)
    #empty_serial()
    #lcd.text(state, 2)
    print("Entering State: " + state)
    if state == "BallSearch":
        print("Searching for ball...")
        current_action['text'] = "Taking Picture..."
        window.update()
        ar = test.ball_search()
        current_action['text'] = "Approaching Ball..."
        ball = PhotoImage(file = 'result.png')
        ball = ball.subsample(2)
        ball_img['image'] = ball
        window.update()
        print(ar)
        hold.turning = True
        turnTo(hold.angleZ + int(ar[2] - 1))
        time.sleep(1)
        
        # sends move command and waits until moving is complete
        hold.turning = False
        #sendToArduino(3, 0)
        sendToArduino(3, float(ar[1]/12))
        time.sleep(5)
        
        # sends command to recover ball

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
        if hoop == startHoop and passStart:
            nextState = "pinSearch"
        else:
            print("Going for Hoop #" + str(hoop))
            current_action['text'] = "Manual Control"
        def key_pressed(event):
            
            if (event.char == 'a'):
                hold.turning  = True
                sendToArduino(4, 0)
            elif (event.char == 'd'):
                hold.turning  = True
                sendToArduino(4, 1)
            elif (event.char == 'w'):
                hold.turning  = False
                sendToArduino(6, 0)
            elif (event.char == 's'):
                hold.turning  = True
                sendToArduino(5, 0)
            else:
                window.quit()
            current_position['text'] = str(round(hold.angleZ)) + "  "+ str(round(hold.posX, 2)) + "  " + str(round(hold.posY, 2))
            
        def task():
            current_position['text'] = str(round(hold.angleZ)) + "  "+ str(round(hold.posX, 2)) + "  " + str(round(hold.posY, 2))
            window.after(50, task)  # reschedule event in 2 seconds

           
        window.after(50, task)
        window.bind('<Key>', key_pressed)

#         window.bind('d', sendToArduino(4, 1))
#         window.bind('w', sendToArduino(6, 0))
#         window.bind('s', sendToArduino(5, 0))
        window.mainloop()
        time.sleep(1)
            
        nextState = "VerifyNumber"

    elif state == "VerifyNumber":
        print("Taking picture... ")
        current_action['text'] = "Taking Picture of Hoop..."
        if (test.hoop_pic() == 1):
            num = PhotoImage(file = 'number.png')
            num = num.zoom(5)
            hoop_num['image'] = num
            window.update()
        else:
            num = PhotoImage(file = 'hoopPic_og.png')
            num = num.subsample(5)
            hoop_num['image'] = num
            window.update()
        
        xL = (height * (0.05 + 0.045 * 5) - 25)

        yL = height * (.95 - .045 * 5) - 33

        bot_img.place(width = 50, height = 67, x = xL , y = yL) 
        window.update()
        print("Picture Taken, Getting number...")
        # a  = numverification()
        # if a == nextHoop:
        nextState = "Sequence"
        # else:
        # god knows

    elif state == "Sequence":
        # Get distance to flag
        # Activate motors until black crease
        current_action['text'] = "Beginning Sequence..."
        curr = nextHoop
        nextHoop = nextHoop % 6
        nextHoop += 1
        if (curr == 1, 2):
            angle1 = 180
            angle2 = 0
        else:
            angle1 = 0
            angle2 = 180
        hold.turning = False
        sendToArduino(2, 1)
        time.sleep(5)
        hoop_arr[curr - 1 ]['background'] = "green"
        hoop_arr[nextHoop - 1]['background'] = "yellow"
        hold.turning = True
        time.sleep(1)
        turnTo(angle1)
        time.sleep(1)
        hold.turning = False
        sendToArduino(0, 1.5)
        current_action['text'] = "Moving past Hoop"
        time.sleep(5)
        hold.turning = True
        turnTo(90)
        time.sleep(1)
        hold.turning = False
        sendToArduino(0, 2.5)
        time.sleep(5)
        hold.turning = True
        turnTo(angle2)
        time.sleep(1)
        
        
        
        nextState = "BallSearch"
        
        
    elif state == "pegSearch":
        # Look for peg
        
        nextState = "shocotAtPeg"
    elif state == "testTurn":

        
        
        nextState = "BallSearch"
    
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
