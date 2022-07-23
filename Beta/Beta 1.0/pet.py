#imports
from cProfile import label
from tkinter import *
import random as r
from PIL import ImageTk,Image

#function
class PET():
    def __init__(self,obj):
        self.obj = obj
        self.move_q = []
        self.img_q = []
        self.max = (obj.winfo_screenwidth(),obj.winfo_screenheight())
        self.pos = [0,self.max[1]-140]
        self.speed = self.max[0]//200
    def move(self):
        range_x = [self.pos[0]+1,self.max[0]-100-self.pos[0]]
        if r.choice((0,1)) == 0:
            print(range_x[0])
            distance = r.choice(range(0,range_x[0]))
            num = distance//self.speed
            for i in range(num):
                self.move_q.append(-1*self.speed)
            for i in range(num//5):
                self.img_q += assets["move_left"]
            self.img_q += assets["move_left"][:num%5]
        else:
            distance = r.choice(range(0,range_x[1]))
            num = distance//self.speed
            for i in range(num):
                self.move_q.append(self.speed)
            for i in range(num//5):
                self.img_q += assets["move_right"]
            self.img_q += assets["move_right"][:num%5]
    def sleep(self):
        rounds = r.choice(range(240,1201))
        if r.choice([0,1]) == 0:
            for i in range(rounds):
                self.img_q += assets["sleep_left"]
        else:
            for i in range(rounds):
                self.img_q += assets["sleep_right"]
    def dance(self):
        rounds = r.choice(range(120,241))
        for i in range(rounds):
            self.img_q += assets["dance"]
    def idle(self):
        rounds = r.choice(range(20,121))
        if r.choice([0,1]) == 0:
            for i in range(rounds):
                self.img_q += assets["idle_left"]
        else:
            for i in range(rounds):
                self.img_q += assets["idle_right"]
    def advance_move(self):
        self.move_q.pop(0)
        if len(self.move_q) != 0:
            self.pos[0] = self.pos[0]+self.move_q[0]
    def advance_img(self):
        self.img_q.pop(0)
    def get_pos(self):
        return self.pos
    def display(self):
        return self.img_q[0]
    def update(self):
        if len(self.img_q) == 0:
            c = r.choice([1,2,3,4])
            if c == 1:
                self.move()
            if c == 2:
                self.sleep()
            if c == 3:
                self.dance()
            if c == 4:
                self.idle()
        else:
            self.advance_img()
        if len(self.move_q) == 0:
            pass
        else:
            self.advance_move()
def get_img(name):
    res = []
    for i in ["1","2","3","4","5"]:
        res.append(ImageTk.PhotoImage(Image.open("assets/"+name+"/"+i+".png")))
    return res
def gen_coord(inp):
    return "+"+str(inp[0])+"+"+str(inp[1])

#assets
root = Tk()
pet = PET(root)
assets = {"idle_left":get_img("idle_left"),"idle_right":get_img("idle_right"),"dance":get_img("dance"),"move_left":get_img("move_left"),"move_right":get_img("move_right"),"sleep_left":get_img("sleep_left"),"sleep_right":get_img("sleep_right")}

#varibles
label = Button(root,image=assets["idle_left"][0],bd=0,highlightthickness = 0)

#config
label.pack()
root.overrideredirect(True)
root.geometry("+0+"+str(pet.max[1]-140))
root.wm_attributes('-transparentcolor','black')
root.attributes('-topmost',True)

#functions
def update():
    pet.update()
    if len(pet.img_q) == 0:
        label.config(image=assets["idle_left"][0])
    else:
        label.config(image=pet.display())
    root.geometry(gen_coord(pet.get_pos()))
    root.after(50,update)

root.after(50,update)
root.mainloop()