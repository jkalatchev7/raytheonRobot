import time
import tkinter as tk
import threading
from random import randint


class MyTkApp(threading.Thread):
    def __init__(self):

        threading.Thread.__init__(self)

    def run(self):
        print("run")
        self.root = tk.Tk()
        self.s = tk.StringVar()
        self.s.set('Foo')
        self.go = True
        self.label = tk.Label(self.root, textvariable=self.s)
        self.label.pack()
        self.update()

    def update(self):
        print("trun")
        while self.go:
            self.root.update()
            self.label['text'] = randint(300, 400)
            self.label.pack()

app = MyTkApp()
app.start()
print("started")
time.sleep(3)
app.go = False

# Now the app should be running and the value shown on the label
# can be changed by changing the member variable s.
# Like this:
# app.s.set('Bar')