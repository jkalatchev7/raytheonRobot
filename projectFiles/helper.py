#Helper functions because its too crowded over there


#Serial Related Functions

def initialize_serial():
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
