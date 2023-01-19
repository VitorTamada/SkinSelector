import tkinter as tk
from PIL import Image, ImageTk
import io
from urllib.request import urlopen
from win32api import GetSystemMetrics

screen_width, screen_height = GetSystemMetrics(0), GetSystemMetrics(1)

# root window
root = tk.Tk()
root.resizable(width=False, height=False)

img0 = 'http://ddragon.leagueoflegends.com/cdn/img/champion/splash/Lulu_15.jpg'
img1 = 'http://ddragon.leagueoflegends.com/cdn/img/champion/splash/Ashe_22.jpg'
img2 = 'http://ddragon.leagueoflegends.com/cdn/img/champion/splash/Sona_0.jpg'
img3 = 'http://ddragon.leagueoflegends.com/cdn/img/champion/splash/Janna_17.jpg'

imgs = [img0, img1, img2, img3]

def get_imgs(imgs, size_increase=0):
    res = []
    for img in imgs:
        fin = urlopen(img0)
        s = io.BytesIO(fin.read())
        image = Image.open(s)
        pil_image = image.resize((screen_width//4+size_increase, screen_height//4+size_increase))
        res.append(pil_image)

    return res

res = get_imgs(imgs)
window_size = list(res[0].size)
window_size[0] += 300
window_size[1] += 100
root.geometry("{}x{}".format(window_size[0], window_size[1]))

tk_image = ImageTk.PhotoImage(res[0])
label = tk.Label(root, image=tk_image)
label.grid(row=0, column=3, columnspan=2, rowspan=2, padx=5, pady=5, sticky='E')

placeholder = tk.Label(root, text="0")
p1 = tk.Label(root, text="1")

placeholder.grid(row=0, column=0)
p1.grid(row=1, column=0)

def clicked():
    tk_image = ImageTk.PhotoImage(get_imgs(imgs, 10)[0])
    label = tk.Label(root, image=tk_image, anchor='right')
    label.grid(row=0, column=1, columnspan=2, rowspan=2, padx=5, pady=5, sticky='E')

button0 = tk.Button(root, text='click me', fg='red', command=clicked)
button0.grid(column=0, row=3)
button1 = tk.Button(root, text='click me', fg='red', command=clicked)
button1.grid(column=1, row=3)
button2 = tk.Button(root, text='click me', fg='red', command=clicked)
button2.grid(column=2, row=3)

'''
# Nome da janela
root.title("Título teste")

# Tamanho da janela
root.geometry('1280x720')

# Text
label = tk.Label(root, text='Hello, world!')
#label.pack()
label.grid()

# Entry text
txt = tk.Entry(root, width=10)
txt.grid(column=1, row=0)

# menu
menu = tk.Menu(root)
item = tk.Menu(menu)
item.add_command(label='New')
menu.add_cascade(label='File', menu=item)
root.config(menu=menu)

# Button and text change
def clicked():
    res = "You wrote " + txt.get()
    label.configure(text=res)
button = tk.Button(root, text='click me', fg='red', command=clicked)
button.grid(column=2, row=0)
'''

# Execute code and open window
root.mainloop()