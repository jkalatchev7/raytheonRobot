import time
from filterpy import KalmanFilter
from filterpy.common import Q_discrete_white_noise
import imu
import numpy as np
im = imu()
im.initialize()
im.calibrate()

f = KalmanFilter (dim_x=2, dim_z=1)
f.x = np.array([[2.],    # position
                [0.]])   # velocity

f.F = np.array([[1., 1.],
                [0., 1.]])

f.H = np.array([[1., 0.]])

f.P *= 1000.

f.R = 5

f.R = np.array([[5.]])

f.Q = Q_discrete_white_noise(dim=2, dt=0.1, var=0.13)

while True:
    z = im.read_data(0)
    f.predict()
    f.update(z)
    print(f.x)
    time.sleep()
