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
        self.posX = 0
        self.posY = 0
        self.angleZ = 0

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
        self.pos = 0
        self.vell = 0
        self.acc = 0
        self.theta = 0
        self.omega = 0
        self.alpha = 0

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
        pos = [0.0]
        alpha = [0.0]
        omega = [0.0]
        theta = [0.0]
        turning = False

        vel = 0
        angular = 0
        prev = time.time()
        # runs until self.stop becomes True
        while (True):
            holder = 0
            if (self.turning):

                for i in range(3):
                    time.sleep(.001)
                    temp = self.read_data(1)
                    temp = temp - self.offsetZ
                    temp = temp * -1 / 3
                    holder += temp

                if abs(holder) < 1:
                    holder = 0

                alpha.append(holder)
                nextT = time.time()
                elapse = nextT - prev
                self.angleZ += holder * elapse
                angular = angular + holder * elapse
                omega.append(angular)
                acc.append(0.)
                vell.append(0.)
                pos.append(deltaX)
                prev = nextT
            else:
                for i in range(3):
                    time.sleep(.001)
                    temp = self.read_data(0)
                    temp = temp - self.offsetX
                    temp = temp / 3
                    holder += temp

                if abs(holder) < 1.5:
                    holder = 0

                acc.append(holder)
                alpha.append(0)
                nextT = time.time()
                elapse = nextT - prev
                vel = vel + holder * elapse
                # squishes down to 0 if vel is sufficiently small
                if vel < .01 and holder <= 0:
                    vel = 0
                vell.append(vel)
                deltaX = deltaX + vel * elapse
                self.posX += vel * elapse * math.cos(self.angleZ * .0174533)
                self.posY += vel * elapse * math.sin(self.angleZ * .0174533)
                pos.append(deltaX)
                omega.append(angular)
                prev = nextT
            # sets arrays so they can be plotted
            if (self.stop):
                self.pos = pos
                self.acc = acc
                self.vell = vell
                self.theta = theta
                self.omega = omega
                self.alpha = alpha
                break
