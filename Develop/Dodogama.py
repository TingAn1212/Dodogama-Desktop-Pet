#imports ---------------------------------------------------------------------------------------------
from tkinter import *
import threading
import pystray
import random as r
from win32api import GetMonitorInfo, MonitorFromPoint, GetCursorPos
from playsound import playsound
from PIL import ImageTk,Image

#functions --------------------------------------------------------------------------------------------
def screen_size():
    monitor_info = GetMonitorInfo(MonitorFromPoint((0,0)))
    work_area = monitor_info.get("Work")
    return (work_area[2],work_area[3])
def get_img(name,num=5,dance=False):
    res = []
    if dance:
        for i in range(1,num+1):
            i = str(i)
            res.append(ImageTk.PhotoImage(Image.open("assets/"+name+"/"+i+".png").resize((140,140))))
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
def mouse_pos():
    pos = GetCursorPos()
    return (pos[0]-100,pos[1]-100)
def cycle(arr):
    res = []
    last = None
    first = True
    for item in arr:
        if first:
            first = False
            last = item
        else:
            res.append(item)
    res.append(last)
    return res

#global variable ------------------------------------------------------------------------------------
root = Tk()
anger = 0
max = screen_size()
base = screen_size()[1] - 180
speed = max[0]//400
start_x = r.choice(range(0,max[0]-200))
pos = [start_x,max[1]-180]
invi = False
unmute = True

#class ----------------------------------------------------------------------------------------------
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

class Action:
    def __init__(self,name):
        self.Name = name
        self.displace = 0
        self.img_q = []
        self.move_q = []
        self.round = 0
        self.previous = None
        if self.Name == "move":
            self.move()
        if self.Name == "yawn":
            self.yawn()
        if self.Name == "sleep":
            self.sleep()
        if self.Name == "dance":
            self.dance()
        if self.Name == "idle":
            self.idle()
        if self.Name == "eat":
            self.eat()
        if self.Name == "lift":
            self.lift()
        if self.Name == "fall":
            self.fall()
        if self.Name == "anger":
            self.anger()
    def move(self):
        global pos
        range_x = [pos[0]+1,max[0]-200-pos[0]]
        if range_x[0] > 100 and range_x[1] > 100:
            if r.choice((0,1)) == 0:
                distance = r.choice(range(100,range_x[0]))
                num = distance//speed
                for i in range(num):
                    self.move_q.append(-1*speed)
                for i in range(num//20):
                    self.img_q += assets["move_left"]
                self.img_q += assets["move_left"][:num%20]
            else:
                distance = r.choice(range(100,range_x[1]))
                num = distance//speed
                for i in range(num):
                    self.move_q.append(speed)
                for i in range(num//20):
                    self.img_q += assets["move_right"]
                self.img_q += assets["move_right"][:num%20]
        else:
            if range_x[0] < 100:
                distance = r.choice(range(100,range_x[1]))
                num = distance//speed
                for i in range(num):
                    self.move_q.append(speed)
                for i in range(num//20):
                    self.img_q += assets["move_right"]
                self.img_q += assets["move_right"][:num%20]
            else:
                distance = r.choice(range(100,range_x[0]))
                num = distance//speed
                for i in range(num):
                    self.move_q.append(-1*speed)
                for i in range(num//20):
                    self.img_q += assets["move_left"]
                self.img_q += assets["move_left"][:num%20]
    def yawn(self):
        self.displace = 0
        if r.choice([0,1]) == 0:
            self.img_q += assets["yawn_left"]
        else:
            self.img_q += assets["yawn_right"]
    def sleep(self,full=False):
        self.displace = 20
        if full:
            dur = 10
            rounds = int((dur*60*20)/40)
        else:
            rounds = r.choice(time_range(5,10,40,"min"))
        if r.choice([0,1]) == 0:
            self.img_q += assets["dig_left"]
            for i in range(rounds):
                self.img_q += assets["sleep_left"]
        else:
            self.img_q += assets["dig_right"]
            for i in range(rounds):
                self.img_q += assets["sleep_right"]
    def dance(self):
        self.displace = -48
        rounds = r.choice(time_range(5,10,20,"sec"))
        for i in range(rounds):
            self.img_q += assets["dance"]
    def idle(self,left_only=False):
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
        rounds = r.choice(time_range(5,15,10,"sec"))   
        if r.choice([0,1]) == 0:
            for i in range(rounds):
                self.img_q += assets["eat_left"] 
        else:
            for i in range(rounds):
                self.img_q += assets["eat_right"]
    def lift(self):
        if r.choice([0,1]) == 0:
            self.img_q += assets["pickup_left"] 
        else:
            self.img_q += assets["pickup_right"]
    def fall(self):
        self.img_q += assets["fall"]
    def anger(self):
        if r.choice([0,1]) == 0:
            self.img_q += assets["anger_left"]
        else:
            self.img_q += assets["anger_right"]
    def get_img(self):
        if len(self.img_q) > 0:
            return self.img_q[0]
        else:
            return self.previous
    def get_move(self):
        if len(self.move_q) > 0:
            return self.move_q[0]
        else:
            return 0
    def advance(self):
        if self.Name == "lift" or self.Name == "fall":
            self.img_q = cycle(self.img_q)
            self.round += 1
            return 0
        if len(self.img_q) > 0:
            self.previous = self.img_q[0]
            self.img_q.pop(0)
        if len(self.move_q) > 0:
             self.move_q.pop(0)
        self.round += 1
    def can_remove(self):
        global anger
        if len(self.img_q) < 1 and self.Name != "lift":
            anger = 0
            return True
        elif pos[1] >= base and self.Name == "fall":
            return True
        else:
            return False

class PET():
    def __init__(self,obj):
        self.obj = obj
        self.action_q = []
        self.previous = None
    def add_action(self,name,pre=False):
        if pre:
            self.action_q.insert(0,Action(name))
        else:
            self.action_q.append(Action(name))
    def get_action(self):
        res = []
        for i in self.action_q:
            res.append(i.Name)
        return res
    def pressed_move(self,x):
        global anger
        anger += 1
        if anger > 4:
            self.clear()
            self.add_action("anger")
            anger -= 1
        else:
            player = Sound_play(assets["pop"])
            player.start()
            self.clear()
            self.add_action("move")
    def pressed_sleep(self,x):
        player = Sound_play(assets["pop"])
        player.start()
        self.clear()
        self.add_action("yawn")
        self.add_action("sleep")
    def lifted(self,x):
        self.clear()
        self.add_action("lift",True)
    def downed(self,x):
        self.clear()
        self.add_action("fall",pre=True)
        self.add_action("idle")
    def advance_move(self,move):
        global pos
        pos[0] = pos[0]+move
    def clear(self):
        self.action_q = []
    def display(self):
        return self.action_q[0].get_img()
    def get_previous(self):
        return self.previous
    def cancel_lift(self):
        for i in self.action_q:
            if i.Name == "lift" or i.Name == "fall":
                self.action_q.remove(i)
    def update(self):
        global pos
        if len(self.action_q) < 2:
            c = r.choice(["move","move","move","sleep","dance","dance","idle","idle","eat","eat"])
            if c == self.action_q[0].Name:
                c = r.choice(["sleep","dance","dance","idle","idle","eat","eat"])
            if c == "sleep":
                self.add_action("yawn")
            self.add_action(c)
        self.advance_move(self.action_q[0].get_move())
        self.action_q[0].advance()
        if self.action_q[0].can_remove():
            self.previous = self.action_q[0]
            self.action_q.pop(0)

#assets
pet = PET(root)
assets = {
    "idle_left":slow(get_img("idle_left",num=2),20),
    "idle_right":slow(get_img("idle_right",num=2),20),
    "dance":slow(get_img("dance",dance=True),8),
    "move_left":slow(get_img("move_left"),4),
    "move_right":slow(get_img("move_right"),4),
    "yawn_left":slow(get_img("yawn_left",4),16),
    "yawn_right":slow(get_img("yawn_right",4),16),
    "sleep_left":slow(get_img("sleep_left"),16),
    "sleep_right":slow(get_img("sleep_right"),16),
    "eat_left":slow(get_img("eat_left"),4),
    "eat_right":slow(get_img("eat_right"),4),
    "pickup_left":slow(get_img("pickup_left",num=2),20),
    "pickup_right":slow(get_img("pickup_right",num=2),20),
    "fall":slow(get_img("fall",num=4),6),
    "anger_left":slow(get_img("angry_left",8),16),
    "anger_right":slow(get_img("angry_right",8),16),
    "dig_left":slow(get_img("dig_left"),8),
    "dig_right":slow(get_img("dig_right"),8),
    "pop":"assets/sound/pop.mp3"}

def main():
    icon_img = Image.open("assets/icon.png")
    tray = Show_tray(None)
    pet.add_action("idle")
    label = Label(root,image=assets["idle_left"][0],borderwidth=0)
    label.pack()
    label.bind("<ButtonPress-1>", pet.lifted)
    label.bind("<ButtonRelease-1>", pet.downed)
    label.bind("<Button-3>",pet.pressed_move)
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
    def sleep():
        pet.clear()
        pet.add_action("yawn")
        pet.add_action("sleep")
    icon = pystray.Icon(name="Dodogama", icon=icon_img, title="Dodogama", menu=(pystray.Menu(pystray.MenuItem("sleep",sleep),pystray.MenuItem("hide",show),pystray.MenuItem("mute",mute),pystray.MenuItem("close",stop))))
    tray.add(icon)

    #config ------------------------------------------------------------------------------------------
    root.overrideredirect(1) 
    root.geometry(gen_coord((start_x,max[1]-180)))
    root.wm_attributes('-transparentcolor','black')
    root.attributes('-topmost',True)

    #frame update ----------------------------------------------------------------------------------
    def debug():
        # print(mouse_pos())
        # print(pos)
        # print(max,base)
        for i in pet.action_q:
            print(i.Name,anger, end=", ")
        print("")
        pass

    def update():
        global pos
        debug()
        pet.update()
        if pos[1] < base:
            pos[1] = pos[1]+10
        if pos[1] > base:
            pos[1] = base
        label.config(image=pet.display())
        if pet.action_q[0].Name == "lift":
            root.geometry(gen_coord(mouse_pos()))
            pos = list(mouse_pos())
        else:
            root.geometry(gen_coord((pos[0],pos[1]-pet.action_q[0].displace)))
        root.after(25,update)

    root.after(50,update)
    tray.start()
    root.mainloop()

if __name__ == "__main__":
    main()