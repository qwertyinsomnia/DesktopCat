from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk, ImageSequence
import time

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

def update(index):
    if index < 3:
        ShowIdle(0)
    elif index == 3 or index == 4:
        ShowWagTail(0)
        # index = 0
    elif index == 5:
        ShowIdleToSleep(0)
    elif index >= 6 and index <= 7:
        ShowSleep(0)
    elif index == 8:
        ShowSleepToIdle(0)
        index = 0
    index += 1
    root.after(0, update, index)

#分解gif并逐帧显示
def ShowIdle(index):
    im = Image.open('src/CatSpriteIdle.gif')
    # GIF图片流的迭代器
    iter = ImageSequence.Iterator(im)
    #frame就是gif的每一帧，转换一下格式就能显示了
    for frame in iter:
        pic=ImageTk.PhotoImage(frame)
        canvas.create_image((80, 80), image=pic)
        time.sleep(2)
        root.update_idletasks()
        root.update()

def ShowWagTail(index):
    im = Image.open('src/CatSpriteWapTail.gif')
    iter = ImageSequence.Iterator(im)
    for frame in iter:
        pic=ImageTk.PhotoImage(frame)
        canvas.create_image((80, 80), image=pic)
        time.sleep(0.15)
        root.update_idletasks()
        root.update()

def ShowSleep(index):
    im = Image.open('src/CatSpriteSleep.gif')
    iter = ImageSequence.Iterator(im)
    for frame in iter:
        pic=ImageTk.PhotoImage(frame)
        canvas.create_image((80, 80), image=pic)
        time.sleep(1)
        root.update_idletasks()
        root.update()

def ShowSleepToIdle(index):
    im = Image.open('src/CatSpriteSleepToIdle.gif')
    iter = ImageSequence.Iterator(im)
    for frame in iter:
        pic=ImageTk.PhotoImage(frame)
        canvas.create_image((80, 80), image=pic)
        time.sleep(0.15)
        root.update_idletasks()
        root.update()

def ShowIdleToSleep(index):
    im = Image.open('src/CatSpriteIdleToSleep.gif')
    iter = ImageSequence.Iterator(im)
    for frame in iter:
        pic=ImageTk.PhotoImage(frame)
        canvas.create_image((80, 80), image=pic)
        time.sleep(0.15)
        root.update_idletasks()
        root.update()

def do_popup(event):
    try:
        root.tk_popup(event.x_root, event.y_root)
    finally:
        root.grab_release()
    
root = Tk()
# WindowDraggable(root)
frame = tk.Frame(root, highlightthickness=0, borderwidth=0, cursor="circle")
frame.pack()
WindowDraggable(frame)

root.overrideredirect(True)
screen_width = root.winfo_screenwidth() - 100 - 160
screen_height = root.winfo_screenheight() - 100 - 160
screen_resolution = '+' + str(screen_width) + '+' + str(screen_height)
root.geometry(screen_resolution)

# root.bind(("<Button-3>", do_popup))
root.bind('<Escape>', lambda e: root.destroy())

canvas = Canvas(root, width=160, height=160, bg='red')
canvas.config(highlightthickness=0)
canvas.pack()
root.wm_attributes("-transparentcolor", "red", '-topmost', True)
root.lift()
img=[]

frameCntWagTail = 23
root.after(0, update, 0)

root.mainloop()