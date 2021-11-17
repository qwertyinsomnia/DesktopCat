import time
import tkinter as tk
import random
import os
import cv2

Walk_Rightward = 1
Walk_Leftward = -1


class WindowDraggable():
	def __init__(self, label):
		self.label = label
		label.bind('<ButtonPress-1>', self.StartMove)
		label.bind('<ButtonRelease-1>', self.StopMove)
		label.bind('<B1-Motion>', self.OnMotion)
	   
	def StartMove(self, event):
		self.x = event.x
		self.y = event.y
		
	def StopMove(self, event):
		self.x = None
		self.y = None
		
	def OnMotion(self,event):
		x = (event.x_root - self.x) 
		y = (event.y_root - self.y) 
		root.geometry("+%s+%s" % (x, y))

class CatControl:
    def __init__(self):
        self.event = 0
        self.walkFlag = 0
        self.walkDir = Walk_Leftward

def UpdateTest(catControl):
    # screen_pos_x = root.winfo_x() - 10 * event
    # screen_pos_y = root.winfo_y()
    # screen_position = '+' + str(screen_pos_x) + '+' + str(screen_pos_y)
    # root.geometry(screen_position)
    # event = 1
    # root.after(1000, UpdateTest, event)

    print(root.winfo_x(), catControl.walkFlag, catControl.event)
    if catControl.event == 0 and catControl.walkFlag == 0:
        showIdleToWalk(0, catControl.walkDir)
        catControl.event = 5
        catControl.walkFlag = 1
        root.after(frameCntIdleToWalk * frameIntervalIdleToWalk, UpdateTest, catControl)
    elif catControl.event == 5 and catControl.walkFlag != 0:
        if (root.winfo_x() < 1200 or root.winfo_x() > 1600) and catControl.walkFlag == 2:
            catControl.walkFlag = 0
            root.after(0, UpdateTest, catControl)
            
        else:
            print("walk")
            showWalk(0, catControl.walkDir)
            if catControl.walkFlag == 1:
                catControl.walkFlag = 2
            root.after(frameCntWalk * frameIntervalWalk, UpdateTest, catControl)
    elif catControl.event == 5 and catControl.walkFlag == 0:
        showWalkToIdle(0, catControl.walkDir)
        catControl.event = 0
        if catControl.walkDir == Walk_Leftward:
            catControl.walkDir = Walk_Rightward
        else:
            catControl.walkDir = Walk_Leftward
        root.after(frameCntWalkToIdle * frameIntervalWalkToIdle, UpdateTest, catControl)

def Update(event):
    # print("Update movement")
    # 逻辑比较混乱   event:0表示idle状态   1 2 3表示sleep   5表示走路
    seed = random.randrange(7)
    if seed == 0: # idle to sleep or sleep to idle
        if event == 0:
            showIdleToSleep(0)
            event = 1
            root.after(frameCntIdleToSleep * frameIntervalIdleToSleep, Update, event)
        elif event >= 3:
            showSleepToIdle(0)
            event = 0
            root.after(frameCntSleepToIdle * frameIntervalSleepToIdle, Update, event)
        else:
            showSleep(0)
            event += 1
            root.after(frameCntSleep * frameIntervalSleep, Update, event)
    elif seed == 1: # wag tail
        if event >= 1:
            showSleep(0)
            event += 1
            root.after(frameCntSleep * frameIntervalSleep, Update, event)
        elif event == 0:
            showWagTail(0)
            root.after(frameCntWagTail * frameIntervalWagTail, Update, event)
    elif seed == 2: # walk
        if event == 0:
            showIdleToWalk(0)
            event = 5
            root.after(frameCntIdleToWalk * frameIntervalIdleToWalk, Update, event)
        elif event >= 1 and event <= 3:
            showSleep(0)
            event += 1
            root.after(frameCntSleep * frameIntervalSleep, Update, event)
    else: # idle
        if event >= 1:
            showSleep(0)
            event += 1
            root.after(frameCntSleep * frameIntervalSleep, Update, event)
        elif event == 0:
            showIdle(0)
            root.after(frameCntIdle * frameIntervalIdle, Update, event)

def showIdle(idx):
    frame = framesIdle[idx]
    label.configure(image=frame)
    idx += 1
    if idx == frameCntIdle:
        return
    root.after(frameIntervalIdle, showIdle, idx)

def showWagTail(idx):
    frame = framesWagTail[idx]
    label.configure(image=frame)
    idx += 1
    if idx == frameCntWagTail:
        return
    root.after(frameIntervalWagTail, showWagTail, idx)

def showSleep(idx):
    frame = framesSleep[idx]
    label.configure(image=frame)
    idx += 1
    if idx == frameCntSleep:
        return
    root.after(frameIntervalSleep, showSleep, idx)

def showSleepToIdle(idx):
    frame = framesSleepToIdle[idx]
    label.configure(image=frame)
    idx += 1
    if idx == frameCntSleepToIdle:
        return
    root.after(frameIntervalSleepToIdle, showSleepToIdle, idx)
    
def showIdleToSleep(idx):
    frame = framesIdleToSleep[idx]
    label.configure(image=frame)
    idx += 1
    if idx == frameCntIdleToSleep:
        return
    root.after(frameIntervalIdleToSleep, showIdleToSleep, idx)

def showWalk(idx, dir):
    # if root.winfo_x() < 1210 or root.winfo_x() > 2420:
    #     return
    if dir == 1:
        frame = framesWalkR[idx]
    else:
        frame = framesWalk[idx]
    label.configure(image=frame)
    screen_pos_x = root.winfo_x() + dir * walkSpeed
    screen_pos_y = root.winfo_y()
    screen_position = '+' + str(screen_pos_x) + '+' + str(screen_pos_y)
    root.geometry(screen_position)
    idx += 1
    if idx == frameCntWalk:
        return
    root.after(frameIntervalWalk, showWalk, idx, dir)

def showWalkToIdle(idx, dir):
    if dir == 1:
        frame = framesWalkToIdleR[idx]
    else:
        frame = framesWalkToIdle[idx]
    label.configure(image=frame)
    idx += 1
    if idx == frameCntWalkToIdle:
        return
    root.after(frameIntervalWalkToIdle, showWalkToIdle, idx, dir)
    
def showIdleToWalk(idx, dir):
    if dir == 1:
        frame = framesIdleToWalkR[idx]
    else:
        frame = framesIdleToWalk[idx]
    label.configure(image=frame)
    idx += 1
    if idx == frameCntIdleToWalk:
        return
    root.after(frameIntervalIdleToWalk, showIdleToWalk, idx, dir)

def rightKey(event):
    menubar.add_command(label="Exit", command=exit)
    menubar.post(event.x_root, event.y_root)


# window configuration
root = tk.Tk()
# root.title("kit")
# frame = tk.Frame(root, highlightthickness=0, borderwidth=0, cursor="circle")
# frame.pack()
root.overrideredirect(1) # remove taskbar

# position
screen_width = root.winfo_screenwidth() - 100 - 160
screen_height = root.winfo_screenheight() - 100 - 160
screen_resolution = '+' + str(screen_width) + '+' + str(screen_height)
root.geometry(screen_resolution)
root.wm_attributes("-transparentcolor", "red", '-topmost', True)
root.lift()
# canvas = tk.Canvas(frame, width=160, height=160, bd=-2)
root.bind('<Escape>', lambda e: root.destroy())

# label1_text=tk.StringVar()
# label1_text.set("Mishookoo\n ~your personal desk cat~")
# label1=tk.Label(root, textvariable=label1_text)
# label1.pack()
# attach popup to frame
# label1.bind("<Button-3>", do_popup)

# L = tk.Label(root, text="Right-click to display menu", width=40, height=20)
# L.pack()
menubar = tk.Menu(root,tearoff=False) # 创建一个菜单
root.bind("<Button-3>", lambda x: rightKey(x)) # 绑定右键鼠标事件
label = tk.Label(root, borderwidth=0)
label.pack()

WindowDraggable(label)
time.sleep(0.5)

###############################
# gif config
frameCntIdle = 2
frameCntWagTail = 23
frameCntSleep = 6
frameCntIdleToSleep = 19
frameCntSleepToIdle = 19
frameCntWalk = 12
frameCntIdleToWalk = 5
frameCntWalkToIdle = 5

frameIntervalIdle = 2000
frameIntervalWagTail = 100
frameIntervalSleep = 1000
frameIntervalIdleToSleep = 150
frameIntervalSleepToIdle = 150
frameIntervalWalk = 100
frameIntervalIdleToWalk = 100
frameIntervalWalkToIdle = 100

walkSpeed = 8

framesIdle = [tk.PhotoImage(file='Src/CatSpriteIdle.gif', format = 'gif -index %i' %(i)) for i in range(frameCntIdle)]
framesWagTail = [tk.PhotoImage(file='Src/CatSpriteWapTail.gif', format = 'gif -index %i' %(i)) for i in range(frameCntWagTail)]
framesSleep = [tk.PhotoImage(file='Src/CatSpriteSleep.gif', format = 'gif -index %i' %(i)) for i in range(frameCntSleep)]
framesIdleToSleep = [tk.PhotoImage(file='Src/CatSpriteIdleToSleep.gif', format = 'gif -index %i' %(i)) for i in range(frameCntIdleToSleep)]
framesSleepToIdle = [tk.PhotoImage(file='Src/CatSpriteSleepToIdle.gif', format = 'gif -index %i' %(i)) for i in range(frameCntSleepToIdle)]
framesWalk = [tk.PhotoImage(file='Src/CatSpriteWalk.gif', format = 'gif -index %i' %(i)) for i in range(frameCntWalk)]
framesIdleToWalk = [tk.PhotoImage(file='Src/CatSpriteIdleToWalk.gif', format = 'gif -index %i' %(i)) for i in range(frameCntIdleToWalk)]
framesWalkToIdle = [tk.PhotoImage(file='Src/CatSpriteWalkToIdle.gif', format = 'gif -index %i' %(i)) for i in range(frameCntWalkToIdle)]
# walk right ward   same parameters  diff images
framesWalkR = [tk.PhotoImage(file='Src/CatSpriteWalkR.gif', format = 'gif -index %i' %(i)) for i in range(frameCntWalk)]
framesIdleToWalkR = [tk.PhotoImage(file='Src/CatSpriteIdleToWalkR.gif', format = 'gif -index %i' %(i)) for i in range(frameCntIdleToWalk)]
framesWalkToIdleR = [tk.PhotoImage(file='Src/CatSpriteWalkToIdleR.gif', format = 'gif -index %i' %(i)) for i in range(frameCntWalkToIdle)]

####################################

catControl = CatControl()


# root.after(0, Update, 0)
root.after(0, UpdateTest, catControl)

tk.mainloop()