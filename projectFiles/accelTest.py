from smbus2 import SMBus
import time
import imu
import threading
import matplotlib.pyplot as plt

#create imu object
hold = imu.imu()
#initialize to set up connections
hold.initialize()
#calibrate the sensors and store offsets
hold.calibrate()
#create a thread that runs that function so it can run simultaneously
x = threading.Thread(target=hold.update, args=[0])
x.start()
time.sleep(3)
#set variable that will end loop
hold.stop = True
print("sleep done")
time.sleep(.5)
#close other thread
x.join()

#all of this below is for plotting
fig, (ax1, ax2, ax3) = plt.subplots(3, 1)
t = list(range(len(hold.acc)))
fig.suptitle('A tale of 2 subplots')
ax1.plot(t, hold.acc, '.-')
ax1.set_xlabel("Accel x")
ax2.plot(t, hold.vell, '.-')
ax2.set_xlabel("Vel y")
ax3.plot(t, hold.pos, '.-')
fig.show()

#print final positions which are stored in the object we've created
print("Final Positions: " + str(hold.posX * 12) + ", " + str(hold.posY * 12))
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
