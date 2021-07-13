import time

import tkinTest
import threading



a = tkinTest.tkinTest()
x = threading.Thread(target=a.run, args=[])
x.start()
print("started")
time.sleep(3)
print("done")
a.working = False
x.join()
print("Done")