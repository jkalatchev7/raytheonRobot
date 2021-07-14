class myserial:
    def __init__(self):
       try:
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
            ser.close()
            ser.open()
            print("port was already open, was closed and opened again!")
            
        self.ser = ser
        
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
        self.ser.write(bytes(strr, 'utf-8'))
        self.ser.flush()
        
    def arduinoRead():
        return self.ser.readline().rstrip().decode('utf-8')
