from tkinter import *
from PIL import ImageTk, Image


width = 1280
height = 720

borders_width = int(width*0.03)

root = Tk()
root.resizable(width=False, height=False)
root.geometry("{}x{}".format(width, height))

canvas = Canvas(root,
                bg='red',
                width=width-borders_width,
                height=height-borders_width)
canvas.place(relx=0.5, rely=0.5, anchor=CENTER)

imagem = Image.open("Sona_0.jpg")
Label(canvas, text="AVAILABLE SKINS", font=("Helvetica", 13), bg='green').place(anchor=NW,
                                                                    relheight=0.1,
                                                                    relwidth=0.25)
Label(canvas, text="CHOSEN SKIN", font=("Helvetica", 13), bg='blue', fg='white').place(anchor=NW,
                                                                           relheight=0.1,
                                                                           relwidth=0.75,
                                                                           relx=0.25
                                                                           )
texto = Text(canvas, bg='pink', state=NORMAL)
texto.place(anchor=NW,
            relheight=0.7,
            relwidth=0.25,
            rely=0.1)
sample_text = "ueihiauehiua\n"
for i in range(50):
    sample_text += "ueihiauehiua" + str(i) + "\n"
texto.insert(END, sample_text)
texto.config(state=DISABLED)
Label(canvas, text="SKIN IMAGE", bg='gray').place(relheight=0.7,
                                             relwidth=0.75,
                                             relx=0.25,
                                             rely=0.1)
Label(canvas, text="CHOOSE SKIN", bg='purple').place(relheight=0.1,
                                                     relwidth=0.25,
                                                     rely=0.8,
                                                     )
Label(canvas, text="EXIT", bg='light blue').place(relheight=0.1,
                                                  relwidth=0.25,
                                                  rely=0.9)
Label(canvas, text="SKIN NAME", bg='dark green').place(relheight=0.2,
                                                       relwidth=0.75,
                                                       relx=0.25,
                                                       rely=0.8)

'''
image_count = 10
width = 300

image = Image.open("Sona_0.jpg")
image_width = image.size[0]
image_height = image.size[1]
image_height_width_ratio = image_height / image_width
new_size = (int(width), int(image_height_width_ratio * width))
height = max(1000, new_size[1]*image_count)
canvas_height = new_size[1]*3
canvas_width = width
image = ImageTk.PhotoImage(image.resize(new_size))

frame=Frame(root,width=width,height=height)
frame.grid(row=0,column=0)

canvas=Canvas(frame,bg='#FFFFFF',width=width,height=height,scrollregion=(0,0,width,height))

hbar=Scrollbar(frame,orient=HORIZONTAL)
hbar.pack(side=BOTTOM,fill=X)
hbar.config(command=canvas.xview)

vbar=Scrollbar(frame,orient=VERTICAL)
vbar.pack(side=RIGHT,fill=Y, expand=True)
vbar.config(command=canvas.yview)


for i in range(10):
    canvas.create_image(new_size[0]//2, (new_size[1]//2)*i*2+new_size[1]//2, image=image)

canvas.config(width=canvas_width,height=canvas_height)
canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
canvas.pack(side=LEFT,expand=True,fill=BOTH)

print(help(canvas.create_image))
'''

root.mainloop()
