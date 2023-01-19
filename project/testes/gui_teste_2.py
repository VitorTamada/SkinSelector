from win32api import GetSystemMetrics
import tkinter as tk
from urllib.request import urlopen
from PIL import Image, ImageTk
import io

screen_width, screen_height = GetSystemMetrics(0), GetSystemMetrics(1)

root = tk.Tk() # this is your window
root.geometry("{}x{}".format(screen_width//2, screen_height//2)) # set size of you window here is example for 1/2 screen height and width

img0 = 'http://ddragon.leagueoflegends.com/cdn/img/champion/splash/Lulu_15.jpg'
fin = urlopen(img0)
s = io.BytesIO(fin.read())
img = Image.open('E:\SkinSelectorProject\img\champion\splash\Annie_1.jpg', "r") # replace with picture path
width, height = screen_width//4, screen_height//4 # determine widght and height basing on screen_width, screen_height
img.resize((width, height), Image.Resampling.LANCZOS)
ph = ImageTk.PhotoImage(img)
label = tk.Label(root, image=ph)
label.grid(row=0, column=0)
label.image = ph

# todo: create more Tkinter objects and pack them into root

root.mainloop()