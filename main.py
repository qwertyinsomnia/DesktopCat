import time
import tkinter as tk
import random
import os

Walk_Rightward = 1
Walk_Leftward = -1
WIDTH_LEFT_BOUND = 100
WIDTH_RIGHT_BOUND = 1500
HEIGHT_BOTTOM_BOUND = 800
HEIGHT_TOP_BOUND = 120


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
        self.sleepFlag = 0
        self.walkFlag = 0
        self.walkDir = Walk_Leftward
        
        self.jumpFlag = 0

def UpdateTest(catControl):
    seed = random.randrange(7)
    seed = 3
    if seed == 3: # idle to sleep or sleep to idle
        # showIdle(0)
        # root.after(frameCntIdle * frameIntervalIdle, showJumpHigh, 0)
        # root.after(frameCntJumpHigh * frameIntervalJumpHigh + frameCntIdle * frameIntervalIdle, UpdateTest, catControl)
        
        # showJumpLow(0)
        # root.after(frameCntJumpLow * frameIntervalJumpLow, UpdateTest, 0)
        showIdle(0)
        root.after(frameCntIdle * frameIntervalIdle, showJumpLow, 0)
        screen_pos_x = root.winfo_x()
        screen_pos_y = root.winfo_y() + 20 * 4
        screen_position = '+' + str(screen_pos_x) + '+' + str(screen_pos_y)
        root.geometry(screen_position)
        root.after(frameCntJumpLow * frameIntervalJumpLow + frameCntIdle * frameIntervalIdle, UpdateTest, catControl)


def Update(catControl):
    # print("Update movement")
    # 随机种子seed 范围7 0:sleep  1:wagtail  2:walk  others:idle
    # 逻辑比较混乱   event:0表示idle状态   1 2 3表示sleep 4表示由sleep转为idle  5表示走路

    if catControl.sleepFlag == 1:
        if random.randrange(6) == 0:
            # print("wake!!")
            catControl.sleepFlag = 0
            showSleepToIdle(0)
            root.after(frameCntSleepToIdle * frameIntervalSleepToIdle, Update, catControl)
            return
        else:
            # print("sleep...")
            showSleep(0)
            root.after(frameCntSleep * frameIntervalSleep, Update, catControl)
            return
    
    if catControl.walkFlag > 0:
        if catControl.walkFlag == 1:
            catControl.walkFlag = 2
        else:
            if (root.winfo_x() < WIDTH_RIGHT_BOUND or root.winfo_x() > WIDTH_LEFT_BOUND) or random.randrange(4) == 0:
                catControl.walkFlag = 0
                showWalkToIdle(0, catControl.walkDir)
                root.after(frameCntWalkToIdle * frameIntervalWalkToIdle, Update, catControl)
                return
        showWalk(0, catControl.walkDir)
        root.after(frameCntWalk * frameIntervalWalk, Update, catControl)
        return

    seed = random.randrange(7)
    # seed = 2
    if seed == 0: # idle to sleep or sleep to idle
        # print("sleep seed")
        catControl.sleepFlag = 1
        showIdleToSleep(0)
        root.after(frameCntIdleToSleep * frameIntervalIdleToSleep, showSleep, 0)
        root.after(frameCntSleep * frameIntervalSleep + frameCntIdleToSleep * frameIntervalIdleToSleep, Update, catControl)
    elif seed == 1:
        showWagTail(0)
        root.after(frameCntWagTail * frameIntervalWagTail, Update, catControl)
    elif seed == 2:
        if root.winfo_x() < WIDTH_RIGHT_BOUND:
            catControl.walkDir == Walk_Rightward
        elif root.winfo_x() > WIDTH_LEFT_BOUND:
            catControl.walkDir == Walk_Leftward
        else:
            catControl.walkDir = random.choice([Walk_Leftward, Walk_Rightward])
        showIdleToWalk(0, catControl.walkDir)
        catControl.walkFlag = 1
        root.after(frameCntIdleToWalk * frameIntervalIdleToWalk, Update, catControl)
    elif seed == 3:
        if random.randrange(2) == 0 and root.winfo_y() > HEIGHT_TOP_BOUND:
            showJumpHigh(0)
            root.after(frameCntJumpHigh * frameIntervalJumpHigh, Update, catControl)
        elif random.randrange(2) == 1 and root.winfo_y() < HEIGHT_BOTTOM_BOUND:
            showJumpLow(0)
            screen_pos_x = root.winfo_x()
            screen_pos_y = root.winfo_y() + 20 * 4
            screen_position = '+' + str(screen_pos_x) + '+' + str(screen_pos_y)
            root.geometry(screen_position)
            root.after(frameCntJumpLow * frameIntervalJumpLow, Update, catControl)
        else:
            showIdle(0)
            root.after(frameCntIdle * frameIntervalIdle, Update, catControl)
    else:
        showIdle(0)
        root.after(frameCntIdle * frameIntervalIdle, Update, catControl)


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

def showJumpHigh(idx):
    if idx == 0:
        screen_pos_x = root.winfo_x()
        screen_pos_y = root.winfo_y() - JumpHeight
        screen_position = '+' + str(screen_pos_x) + '+' + str(screen_pos_y)
        root.geometry(screen_position)
    frame = framesJumpHigh[idx]
    label.configure(image=frame)
    idx += 1
    if idx == frameCntJumpHigh:
        return
    root.after(frameIntervalJumpHigh, showJumpHigh, idx)

def showJumpLow(idx):
    if idx == 0:
        screen_pos_x = root.winfo_x()
        screen_pos_y = root.winfo_y() - 5 * 4
        screen_position = '+' + str(screen_pos_x) + '+' + str(screen_pos_y)
        root.geometry(screen_position)
    frame = framesJumpLow[idx]
    label.configure(image=frame)
    idx += 1
    if idx == frameCntJumpLow:
        # screen_pos_x = root.winfo_x()
        # screen_pos_y = root.winfo_y() + 40 * 4
        # screen_position = '+' + str(screen_pos_x) + '+' + str(screen_pos_y)
        # root.geometry(screen_position)
        return
    root.after(frameIntervalJumpLow, showJumpLow, idx)

def rightKey(event):
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
# print(root.winfo_screenwidth(), root.winfo_screenheight()) # 1707 960
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
menubar.add_command(label="Exit", command=root.destroy)
label = tk.Label(root, borderwidth=0)
label.bind("<Button-3>", lambda x: rightKey(x)) # 绑定右键鼠标事件
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
frameCntJumpHigh = 8
frameCntJumpLow = 7

frameIntervalIdle = 2000
frameIntervalWagTail = 100
frameIntervalSleep = 1000
frameIntervalIdleToSleep = 150
frameIntervalSleepToIdle = 150
frameIntervalWalk = 100
frameIntervalIdleToWalk = 100
frameIntervalWalkToIdle = 100
frameIntervalJumpHigh = 100
frameIntervalJumpLow = 150

walkSpeed = 8
JumpHeight = 80

framesIdle = [tk.PhotoImage(file='Src/CatSpriteIdle.gif', format = 'gif -index %i' %(i)) for i in range(frameCntIdle)]
framesWagTail = [tk.PhotoImage(file='Src/CatSpriteWagTail.gif', format = 'gif -index %i' %(i)) for i in range(frameCntWagTail)]
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

framesJumpHigh = [tk.PhotoImage(file='Src/CatSpriteJumpHigh.gif', format = 'gif -index %i' %(i)) for i in range(frameCntJumpHigh)]
framesJumpLow = [tk.PhotoImage(file='Src/CatSpriteJumpLow.gif', format = 'gif -index %i' %(i)) for i in range(frameCntJumpLow)]

####################################

catControl = CatControl()

root.after(0, Update, catControl)
# root.after(0, UpdateTest, catControl)

tk.mainloop()