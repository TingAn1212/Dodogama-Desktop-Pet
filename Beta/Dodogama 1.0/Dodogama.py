#imports
from tkinter import *
import threading
import pystray
import random as r
from playsound import playsound
from PIL import ImageTk,Image

#function
class Sound_play(threading.Thread):
    def __init__(self,path):
        super().__init__()
        self.path = path
    def run(self):
        if unmute:
            playsound(self.path)
class Show_tray(threading.Thread):
    def __init__(self,obj):
        super().__init__()
        self.obj = obj
    def add(self,new):
        self.obj = new
    def run(self):
        self.obj.run()
    def stop(self):
        self.obj.stop()
class PET():
    def __init__(self,obj):
        self.obj = obj
        self.move_q = []
        self.img_q = []
        self.max = (obj.winfo_screenwidth(),obj.winfo_screenheight())
        self.start_x = r.choice(range(0,self.max[0]-200))
        self.pos = [self.start_x,self.max[1]-220]
        self.speed = self.max[0]//200
        self.previous = None
    def move(self):
        #print("move")
        range_x = [self.pos[0]+1,self.max[0]-200-self.pos[0]]
        if r.choice((0,1)) == 0:
            distance = r.choice(range(0,range_x[0]))
            num = distance//self.speed
            for i in range(num):
                self.move_q.append(-1*self.speed)
            for i in range(num//10):
                self.img_q += assets["move_left"]
            self.img_q += assets["move_left"][:num%10]
        else:
            distance = r.choice(range(0,range_x[1]))
            num = distance//self.speed
            for i in range(num):
                self.move_q.append(self.speed)
            for i in range(num//10):
                self.img_q += assets["move_right"]
            self.img_q += assets["move_right"][:num%10]
    def sleep(self):
        #print("sleep")
        rounds = r.choice(time_range(5,10,40,"min"))
        if r.choice([0,1]) == 0:
            for i in range(rounds):
                self.img_q += assets["sleep_left"]
        else:
            for i in range(rounds):
                self.img_q += assets["sleep_right"]
    def dance(self):
        #print("dance")
        rounds = r.choice(time_range(5,10,20,"sec"))
        for i in range(rounds):
            self.img_q += assets["dance"]
    def idle(self,left_only=False):
        #print("idle")
        rounds = r.choice(time_range(5,15,20,"sec"))
        if left_only:
            for i in range(rounds):
                self.img_q += assets["idle_left"]
        else:
            if r.choice([0,1]) == 0:
                for i in range(rounds):
                    self.img_q += assets["idle_left"]
            else:
                for i in range(rounds):
                    self.img_q += assets["idle_right"]
    def eat(self):
        #print("eat")
        rounds = r.choice(time_range(5,15,10,"sec"))   
        if r.choice([0,1]) == 0:
            for i in range(rounds):
                self.img_q += assets["eat_left"] 
        else:
            for i in range(rounds):
                self.img_q += assets["eat_right"] 
    def pressed(self,x):
        player = Sound_play(assets["pop"])
        player.start()
        self.clear()
        self.move()
    def advance_move(self):
        self.move_q.pop(0)
        if len(self.move_q) != 0:
            self.pos[0] = self.pos[0]+self.move_q[0]
    def clear(self):
        self.move_q = []
        self.img_q = []
    def advance_img(self):
        self.img_q.pop(0)
    def get_pos(self):
        return self.pos
    def display(self):
        return self.img_q[0]
    def get_previous(self):
        return self.previous
    def update(self):
        if len(self.img_q) == 0:
            c = r.choice([1,2,3,4,5])
            if c == 1:
                self.move()
            if c == 2:
                self.sleep()
            if c == 3:
                self.dance()
            if c == 4:
                self.idle()
            if c == 5:
                self.eat()
        else:
            self.advance_img()
            try:
                self.previous = self.img_q[0]
            except:
                pass
        if len(self.move_q) == 0:
            pass
        else:
            self.advance_move()
def get_img(name,num=5,dance=False):
    res = []
    if dance:
        for i in range(1,num+1):
            i = str(i)
            res.append(ImageTk.PhotoImage(Image.open("assets/"+name+"/"+i+".png").resize((180,180))))
    else:
        for i in range(1,num+1):
            i = str(i)
            res.append(ImageTk.PhotoImage(Image.open("assets/"+name+"/"+i+".png").resize((200,200))))
    return res
def slow(lst,speed):
    res = []
    for item in lst:
        for i in range(speed):
            res.append(item)
    return res
def gen_coord(inp):
    return "+"+str(inp[0])+"+"+str(inp[1])
def time_range(r1,r2,round,mode):
    if mode == "min":
        r1 = r1*60*20
        r2 = r2*60*20
        return range(int(r1/round),int(r2/round)+1)
    if mode == "sec":
        r1 = r1*20
        r2 = r2*20
        return range(int(r1/round),int(r2/round)+1)

#assets
root = Tk()
pet = PET(root)
assets = {"idle_left":slow(get_img("idle_left",num=2),10),"idle_right":slow(get_img("idle_right",num=2),10),"dance":slow(get_img("dance",dance=True),4),"move_left":slow(get_img("move_left"),2),"move_right":slow(get_img("move_right"),2),"sleep_left":slow(get_img("sleep_left"),8),"sleep_right":slow(get_img("sleep_right"),8),"eat_left":slow(get_img("eat_left"),2),"eat_right":slow(get_img("eat_right"),2),"pop":"assets/sound/pop.mp3"}

#varibles
invi = False
unmute = True
icon_img = Image.open("assets/icon.png")
tray = Show_tray(None)
pet.idle(True)
label = Label(root,image=assets["idle_left"][0],borderwidth=0)
label.pack()
label.bind("<Button-1>",pet.pressed)
def stop():
    root.quit()
    tray.stop()
def show():
    global invi
    if invi == False:
        invi = True
        root.attributes("-alpha",0)
    else:
        invi = False
        root.attributes("-alpha",1)
def mute():
    global unmute
    if unmute == False:
        unmute = True
    else:
        unmute = False
icon = pystray.Icon(name ="Dodogama", icon =icon_img, title ="Dodogama", menu =(pystray.Menu(pystray.MenuItem("hide",show),pystray.MenuItem("mute",mute),pystray.MenuItem("close",stop))))
tray.add(icon)

#config
root.overrideredirect(1) 
root.geometry("+"+str(pet.start_x)+"+"+str(pet.max[1]-220))
root.wm_attributes('-transparentcolor','black')
root.attributes('-topmost',True)

#functions
def update():
    pet.update()
    if len(pet.img_q) == 0:
        label.config(image=pet.get_previous())
    else:
        label.config(image=pet.display())
    root.geometry(gen_coord(pet.get_pos()))
    root.after(50,update)

root.after(50,update)
tray.start()
root.mainloop()