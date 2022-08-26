import time
import random
import tkinter as tk


class WindowDraggable():
    def __init__(self, label, root):
        self.label = label
        self.root = root
        self.label.bind('<ButtonPress-1>', self.StartMove)
        self.label.bind('<ButtonRelease-1>', self.StopMove)
        self.label.bind('<B1-Motion>', self.OnMotion)
        
    def StartMove(self, event):
        self.x = event.x
        self.y = event.y
        
    def StopMove(self, event):
        self.x = None
        self.y = None
        
    def OnMotion(self, event):
        x = (event.x_root - self.x)
        y = (event.y_root - self.y)
        self.root.geometry("+%s+%s" % (x, y))


class DesktopCat():
    def __init__(self):
        
        self.root = tk.Tk()
        self.root.overrideredirect(1) # remove taskbar

        # position
        screen_width = self.root.winfo_screenwidth() - 100 - 160
        screen_height = self.root.winfo_screenheight() - 100 - 160
        print(self.root.winfo_screenwidth(), self.root.winfo_screenheight()) # 1707 960
        screen_resolution = '+' + str(screen_width) + '+' + str(screen_height)
        self.root.geometry(screen_resolution)
        self.root.wm_attributes("-transparentcolor", "red", '-topmost', True)
        self.root.lift()

        # exit()
        self.root.bind('<Escape>', lambda e: self.root.destroy())

        # right mouse click menu
        self.menubar = tk.Menu(self.root,tearoff=False) # 创建一个菜单
        self.menubar.add_command(label="恰饭", command=self.feed)
        self.menubar.add_command(label="Exit", command=self.root.destroy)


        self.menu_time_flag = False
        self.root.bind("<Button-3>", lambda x: self.rightKey(x)) # 绑定右键鼠标事件
        self.label = tk.Label(self.root, borderwidth=0)
        self.label.pack()

        WindowDraggable(self.label, self.root)
        time.sleep(0.5)

        #####
        # src config
        self.frameCntEat = 4
        self.frameCntIdleToEat = 6
        self.frameCntEatToIdle = 6
        self.frameCntSleep = 2

        self.frameIntervalEat = 500
        self.frameIntervalIdleToEat = 200
        self.frameIntervalEatToIdle = 200
        self.frameIntervalSleep = 800


        self.framesIdle = [tk.PhotoImage(file='Src/mint/idle.gif', format = 'gif -index %i' %(i)) for i in range(1)]
        self.framesLookLeft = [tk.PhotoImage(file='Src/mint/lookleft.gif', format = 'gif -index %i' %(i)) for i in range(1)]
        self.framesLookRight = [tk.PhotoImage(file='Src/mint/lookright.gif', format = 'gif -index %i' %(i)) for i in range(1)]
        self.framesEat = [tk.PhotoImage(file='Src/mint/eat.gif', format = 'gif -index %i' %(i)) for i in range(self.frameCntEat)]
        self.framesIdleToEat = [tk.PhotoImage(file='Src/mint/idletoeat.gif', format = 'gif -index %i' %(i)) for i in range(self.frameCntIdleToEat)]
        self.framesEatToIdle = [tk.PhotoImage(file='Src/mint/eattoidle.gif', format = 'gif -index %i' %(i)) for i in range(self.frameCntEatToIdle)]
        self.framesSleep = [tk.PhotoImage(file='Src/mint/sleep.gif', format = 'gif -index %i' %(i)) for i in range(self.frameCntSleep)]

        # self.root.after(0, Update)
        # tk.mainloop()
        self.eatFlag = 0
        self.sleepFlag = False
        self.sleepBeginTime = 0
        self.sleepTime = 300

        self.startRunningTime = time.time()


    def feed(self):
        self.eatFlag = 1

    def wake(self):
        self.sleepFlag = False
        self.menubar.delete(index1=2)
        self.startRunningTime = time.time()

    def catControl(self):
        if self.sleepFlag:
            if (time.time() - self.sleepBeginTime) > self.sleepTime:
                self.sleepFlag = False
                self.menubar.delete(index1=2)

        if self.eatFlag != 0 or self.sleepFlag:
            return
        
        if (time.time() - self.startRunningTime) > 400:
            if random.randrange(2) == 0:
                # print("sleep...")
                self.sleepFlag = True
                self.sleepBeginTime = time.time()
                self.menubar.insert_command(index=1, label="醒醒", command=self.wake)
            else:
                self.startRunningTime = time.time()
        # elif random.randrange(10) == 1:
        #     self.eatFlag = 1

    def Update(self):
        self.catControl()

        if self.sleepFlag:
            self.showSleep(0)
            self.root.after(self.frameCntSleep * self.frameIntervalSleep, self.Update)

        elif self.eatFlag == 1:
            self.eatFlag = 2
            self.showIdleToEat(0)
            self.root.after(self.frameCntIdleToEat * self.frameIntervalIdleToEat, self.Update)
        elif self.eatFlag == 2:
            self.eatFlag = 3
            for i in range(2):
                self.showEat(0)
                self.root.after(self.frameCntEat * self.frameIntervalEat * (i + 1), self.showEat, 0)
            self.root.after(self.frameCntEat * self.frameIntervalEat * 3, self.Update)
        elif self.eatFlag == 3:
            self.eatFlag = 0
            self.showEatToIdle(0)
            self.root.after(self.frameCntEatToIdle * self.frameIntervalEatToIdle, self.Update)

        else:
            forward = self.GetRelativePosition()
            if forward == -1:
                image = self.framesLookLeft
            elif forward == 0:
                image = self.framesIdle
            else:
                image = self.framesLookRight
            
            self.label.configure(image=image)
            self.root.after(100, self.Update)


    def showSleep(self, idx):
        frame = self.framesSleep[idx]
        self.label.configure(image=frame)
        idx += 1
        if idx == self.frameCntSleep:
            return
        self.root.after(self.frameIntervalSleep, self.showSleep, idx)


    def showIdleToEat(self, idx):
        frame = self.framesIdleToEat[idx]
        self.label.configure(image=frame)
        idx += 1
        if idx == self.frameCntIdleToEat:
            return
        self.root.after(self.frameIntervalIdleToEat, self.showIdleToEat, idx)


    def showEat(self, idx):
        frame = self.framesEat[idx]
        self.label.configure(image=frame)
        idx += 1
        if idx == self.frameCntEat:
            return
        self.root.after(self.frameIntervalEat, self.showEat, idx)


    def showEatToIdle(self, idx):
        frame = self.framesEatToIdle[idx]
        self.label.configure(image=frame)
        idx += 1
        if idx == self.frameCntEatToIdle:
            return
        self.root.after(self.frameIntervalEatToIdle, self.showEatToIdle, idx)


    def GetRelativePosition(self):
        mouse_pos = self.root.winfo_pointerxy()
        mouse_x = mouse_pos[0]
        cat_x = self.root.winfo_x()

        if mouse_x < cat_x:
            return -1
        elif mouse_x >= cat_x and mouse_x <= cat_x + 160:
            return 0
        else:
            return 1

    def rightKey(self, event):
        # print(self.menu_time_flag)
        if self.menu_time_flag:
            self.menubar.delete(index1=0)
        else:
            self.menu_time_flag = True
        self.menubar.insert_command(index=0, label=time.strftime("%X", time.localtime()))

        self.menubar.post(event.x_root, event.y_root)


if __name__== "__main__":

    cat = DesktopCat()
    cat.root.after(0, cat.Update)
    tk.mainloop()
