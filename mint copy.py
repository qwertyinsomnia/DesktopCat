import time
import tkinter as tk

Walk_Rightward = 1
Walk_Leftward = -1
WIDTH_RIGHT_BOUND = 100
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


def Update():
    forward = GetRelativePosition()
    if forward == -1:
        image = imgLookLeft
    elif forward == 0:
        image = imgIdle
    else:
        image = imgLookRight
    
    label.configure(image=image)
    root.after(100, Update)

def GetRelativePosition():
    mouse_pos = root.winfo_pointerxy()
    mouse_x = mouse_pos[0]
    cat_x = root.winfo_x()

    if mouse_x < cat_x:
        return -1
    elif mouse_x >= cat_x and mouse_x <= cat_x + 160:
        return 0
    else:
        return 1


def rightKey(event, menu_time_flag):
    print(menu_time_flag)
    if menu_time_flag:
        menubar.delete(index1=0)
    else:
        menu_time_flag = True
    menubar.insert_command(index=0, label=time.strftime("%X", time.localtime()))
    menubar.post(event.x_root, event.y_root)


root = tk.Tk()
root.overrideredirect(1) # remove taskbar

# position
screen_width = root.winfo_screenwidth() - 100 - 160
screen_height = root.winfo_screenheight() - 100 - 160
print(root.winfo_screenwidth(), root.winfo_screenheight()) # 1707 960
screen_resolution = '+' + str(screen_width) + '+' + str(screen_height)
root.geometry(screen_resolution)
root.wm_attributes("-transparentcolor", "red", '-topmost', True)
root.lift()

# exit()
root.bind('<Escape>', lambda e: root.destroy())

# right mouse click menu
menubar = tk.Menu(root,tearoff=False) # 创建一个菜单
menubar.add_command(label="Exit", command=root.destroy)


menu_time_flag = False
root.bind("<Button-3>", lambda x: rightKey(x, menu_time_flag)) # 绑定右键鼠标事件
label = tk.Label(root, borderwidth=0)
label.pack()

WindowDraggable(label)
# root.bind("<Motion>", GetMousePosition)
time.sleep(0.5)

#####
# src config
imgIdle = [tk.PhotoImage(file='Src/mint/idle.gif', format = 'gif -index %i' %(i)) for i in range(1)]
imgLookLeft = [tk.PhotoImage(file='Src/mint/lookleft.gif', format = 'gif -index %i' %(i)) for i in range(1)]
imgLookRight = [tk.PhotoImage(file='Src/mint/lookright.gif', format = 'gif -index %i' %(i)) for i in range(1)]

root.after(0, Update)

tk.mainloop()