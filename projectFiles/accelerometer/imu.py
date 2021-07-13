import math

from smbus2 import SMBus
import time
import numpy as np
import matplotlib.pyplot as plt

PWR_MGMT_1 = 0x6B
SMPLRT_DIV = 0x19
CONFIG = 0x1A
GYRO_CONFIG = 0x1B
INT_ENABLE = 0x38
ACCEL_XOUT = 0x3B
ACCEL_YOUT = 0x3D
ACCEL_ZOUT = 0x3F
GYRO_XOUT = 0x43
GYRO_YOUT = 0x45
GYRO_ZOUT = 0x47
Device_Address = 0x68


# defines some instance variables of the class
class imu:
    def __init__(self):
        # most important 3 are at the top
        self.posX = 5.
        self.posY = 0.
        self.angleZ = 90

        # offsets help us get rid of some of the sensor's noise
        self.offsetX = 6.9
        self.offsetZ = 1.0

        # defines the bus that will be used to communicate with the accelerometer
        self.bus = SMBus(1)
        self.stop = False
        self.turning = False

        # some temporary variables for troubleshootin
        self.velX = 0
        self.angularZ = 0
        self.cordX = 0
        self.cordY = 0
        self.vell = 0
        self.acc = 0
        self.theta = 0
        self.omega = 0
        self.alpha = 0
        self.dist = 0

    # called once to set up the bus
    def initialize(self):
        self.bus.write_byte_data(Device_Address, SMPLRT_DIV, 7)
        self.bus.write_byte_data(Device_Address, PWR_MGMT_1, 1)
        self.bus.write_byte_data(Device_Address, CONFIG, 0)
        self.bus.write_byte_data(Device_Address, GYRO_CONFIG, 24)
        self.bus.write_byte_data(Device_Address, INT_ENABLE, 1)

    # temporary function, dw about it
    def read_dataA(self):
        acX = self.read_raw(ACCEL_XOUT)
        gyroZ = self.read_raw(GYRO_ZOUT)
        Ax = acX / 16384.0 * 32.174
        Gz = gyroZ / 131.0 * 8
        return Ax, Gz

    # Reads data from acceleromter and returns linear acceleration if type = 0, angular acceleration otherwise
    def read_data(self, type):
        if (type == 0):
            acX = self.read_raw(ACCEL_XOUT)
            Ax = acX / 16384.0 * 32.174
            return Ax
        else:
            gyroZ = self.read_raw(GYRO_ZOUT)
            Gz = gyroZ / 131.0 * 8
            return Gz

    # this is run to reset the offsets so that we don't get gravity or magnetic fields interferring with our acceleration measurements
    def calibrate(self):
        print("Calibrating...")
        arr = []
        offsets = [0.0, 0.0]
        for i in range(1, 500):
            time.sleep(.002)
            ax, gz = self.read_dataA()
            arr.append([ax, gz])
        for qq in range(0, 2):
            offsets[qq] = np.mean(np.array(arr)[:, qq])  # average

        self.offsetX = offsets[0]
        self.offsetZ = offsets[1]
        print("Calibration Finished: Offsets below")
        print(offsets)

    # method to convert data from bus to numerical values
    def read_raw(self, addr):
        high = self.bus.read_byte_data(Device_Address, addr)
        low = self.bus.read_byte_data(Device_Address, addr + 1)
        value = ((high << 8) | low)
        if (value > 32768):
            value = value - 65536
        return value

    # run from another function to calculate position continuously but for one movement at a time (0 for linear, 1 for angular)
    # this function needs to be run in a separate thread because that is the only way to get it to exit as shown in the other file in the drive
    def update(self, typ):
        print("Function Running...")
        deltaX = 0
        deltaTheta = 0
        self.stop = False
        acc = [0.0]
        vell = [0.0]
        posX = [self.posX]
        posY = [self.posY]
        alpha = [0.0]
        omega = [self.angleZ]
        dist = [0.0]
        theta = [0.0]
        turning = False

        vel = 0
        angular = self.angleZ
        prev = time.time()
        # runs until self.stop becomes True
        while (True):
            holder = 0
            holderB = 0
            if (self.turning):

                for i in range(3):
                    time.sleep(.001)
                    temp = self.read_data(1)
                    temp = temp - self.offsetZ
                    temp = temp / 3 * -1
                    holder += temp

                if abs(holder) < 1:
                    holder = 0

                
                nextT = time.time()
                elapse = nextT - prev
                self.angleZ += holder * elapse
                angular = angular + holder * elapse
                alpha.append(holder)
                omega.append(angular)
                
                acc.append(0.)
                vel = 0
                vell.append(vel)
                posX.append(self.posX)
                posY.append(self.posY)
                dist.append(deltaX)
                prev = nextT
            else:
                for i in range(3):
                    time.sleep(.001)
                    temp = self.read_data(0)
                    tempB = self.read_data(1)
                    temp = temp - self.offsetX
                    tempB = tempB - self.offsetZ
                    temp = temp / 3
                    temoB = tempB / 3 * -1
                    
                    holder += temp
                    holderB += tempB
                    
                if abs(holder) < .35:
                    holder = 0
                if abs(holderB) < 10:
                    holderB = 0
                    
                acc.append(holder)
                alpha.append(holderB)
                
                
                nextT = time.time()
                elapse = nextT - prev
                angular = angular + holderB * elapse
                omega.append(angular)
                vel = vel + holder * elapse
                # squishes down to 0 if vel is sufficiently small
                if vel < .2 and holder <= 0:
                    vel = 0
                vell.append(vel)
                deltaX = deltaX + vel * elapse
                self.posX += vel * elapse * math.cos(self.angleZ * .0174533)
                self.posY += vel * elapse * math.sin(self.angleZ * .0174533)
                posX.append(self.posX)
                posY.append(self.posY)
                dist.append(deltaX)
                prev = nextT
            # sets arrays so they can be plotted
            if (self.stop):
                self.cordX = posX
                self.cordY = posY
                self.acc = acc
                self.vell = vell
                self.theta = theta
                self.omega = omega
                self.alpha = alpha
                self.dist = dist
                break
