import time
from filterpy.kalman import KalmanFilter
from filterpy.common import Q_discrete_white_noise
import imu
import numpy as np
import matplotlib.pyplot as plt
im = imu.imu()
im.initialize()
im.calibrate()

f = KalmanFilter (dim_x=2, dim_z=1)
f.x = np.array([[0],    # position
                [0.]])   # velocity

f.F = np.array([[1., 1.],
                [0., 1.]])

f.H = np.array([[1., 0.]])

f.P *= 1000.

f.R = 5

f.R = np.array([[5.]])

f.Q = Q_discrete_white_noise(dim=2, dt=0.1, var=0.13)
a = np.empty([40, 4])

for i in range(40):
    a[i][0] = i
    z = im.read_data(0) - im.offsetX
    a[i][1] = z
    f.predict()
    f.update(z)
    a[i][2] = f.x[0]
    a[i][3] = f.x[1]
    time.sleep(.1)

t = a[:,0]
print(t)
acc = a[:,1]
v = a[:, 2]
p = a[:, 3]
fig, (ax1, ax2, ax3) = plt.subplots(3, 1)
fig.suptitle('A tale of 2 subplots')
ax1.plot(t, acc, '.-')
ax1.set_xlabel("Accel x")
ax2.plot(t, v, '.-')
ax2.set_xlabel("Vel y")
ax3.plot(t, p, '.-')
fig.show()