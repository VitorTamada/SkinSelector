'''
import tkinter as tk
from PIL import Image, ImageTk
from urllib.request import urlopen
import io

def load_image(img_url, ratio=0.35):
    placeholder = img_url
    fin = urlopen(placeholder)
    s = io.BytesIO(fin.read())
    image = Image.open(s)
    new_size = (int(image.size[0] * ratio), int(image.size[1] * ratio))
    image = image.resize(new_size)
    placeholder = ImageTk.PhotoImage(image)
    print(new_size)

    return placeholder

root = tk.Tk()
root.geometry("{}x{}".format(250, 500))

placeholder = load_image('http://ddragon.leagueoflegends.com/cdn/img/champion/splash/Sona_0.jpg')

label = tk.Label(root, text='asifhsdakfhaskj').grid(column=0, row=0)

scrollbar = tk.Scrollbar(root, orient=tk.VERTICAL)
scrollbar.grid(row=0, column=0, sticky='ns')

root.mainloop()
'''

import tkinter as tk

class Example(tk.Frame):
    def __init__(self, parent):

        tk.Frame.__init__(self, parent)
        self.canvas = tk.Canvas(self, borderwidth=0, background="#ffffff")
        self.frame = tk.Frame(self.canvas, background="#ffffff")
        self.vsb = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)

        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((4,4), window=self.frame, anchor="nw",
                                  tags="self.frame")

        self.frame.bind("<Configure>", self.onFrameConfigure)

        self.populate()

    def populate(self):
        '''Put in some fake data'''
        for row in range(100):
            tk.Label(self.frame, text="%s" % row, width=3, borderwidth="1",
                     relief="solid").grid(row=row, column=0)
            t="this is the second column for row %s" %row
            tk.Label(self.frame, text=t).grid(row=row, column=1)

    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

if __name__ == "__main__":
    root=tk.Tk()
    example = Example(root)
    example.pack(side="top", fill="both", expand=True)
    root.mainloop()