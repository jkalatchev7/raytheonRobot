import tkinter
from random import randint


class tkinTest:
    def __init__(self):
        self.root = tkinter.Tk()
        self.root.title("Robot Visual")
        self.root.geometry("300x500")
        self.label = tkinter.Label(self.root, text="State: ")
        self.canv = tkinter.Canvas(self.root, height=400, width=200, bg="green")
        self.img = tkinter.PhotoImage(file='robot.png')
        self.robot = self.canv.create_image(10,10, image=self.img)
        self.working = True
        self.label.pack()
        self.canv.pack()
        hoop1 = self.make_rec(50, 50, 10, 10)
        hoop2 = self.make_rec( 50, 350, 10, 10)
        self.hoops = [hoop1, hoop2]

    def make_rec(self, x, y, h, w):
        return self.canv.create_rectangle(x-w/2, y-h/2, x+w/2, y+h/2, fill="red")

    def update(self):
        while True:
            self.root.update()
            self.label['text'] = randint(300,400)
            self.label.pack()
