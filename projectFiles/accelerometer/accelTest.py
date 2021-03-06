from smbus2 import SMBus
import time
import imu
import threading
import matplotlib.pyplot as plt
import tkinTest
a = tkinTest.tkinTest()

#create imu object
hold = imu.imu()
#initialize to set up connections
hold.initialize()
#calibrate the sensors and store offsets
hold.calibrate()
#create a thread that runs that function so it can run simultaneously
x = threading.Thread(target=hold.update, args=[0])
y = threading.Thread(target=tkinTest.run, args=[imu])
x.start()
y.start()
hold.turning = False
time.sleep(5)
print("turn")
hold.turning = True
time.sleep(5)
print("straight")
hold.turning = False
time.sleep(5)
#set variable that will end loop
hold.stop = True
print("sleep done")
time.sleep(.5)
#close other thread
x.join()
y.join()

#all of this below is for plotting
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
ax7.set_xlim(0,2)
ax7.set_ylim(0,2)
fig1.show()
#print final positions which are stored in the object we've created
print("Final Positions: " + str(round(hold.posX * 12, 1)) + ", " + str(round(hold.posY * 12, 1)))
print("Final Orientation: " + str(-1 * round(hold.angleZ,1)) + " degrees")
# prev = time.time()
# try:
#     while (1):
#         next = time.time()
#         elapse = next-prev
#         prev = next
#         print(elapse)
#         acX = read_raw(ACCEL_XOUT)
#         acY = read_raw(ACCEL_YOUT)
#         gyroZ = read_raw(GYRO_ZOUT)
#     
#         Ax = acX/16384.0*32.174
#         Ay = acY/16384.0*32.174
#         Gz = gyroZ/131.0
#     
#         velX = velX + Ax * elapse
#         velY = velY + Ay * elapse
#         angularZ = angularZ + Gz * elapse
#     
#         posX = posX + velX * elapse
#         posY = posY + velY * elapse
#         angleZ = angleZ + angularZ * elapse
#     
#         print("\nGz=%.3f d/s\t Ax=%.3f ft/s^2\t Ay=%.3f ft/s^2" % (Gz, Ax, Ay))
# except KeyboardInterrupt:
#     print(posX)
#     print(posY)
#     print(angleZ)
#     pass
# 
