from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import script

gui = Tk()
gui.geometry("750x250")
gui.title("Application")

def get_folder_path():
   folder_selected = filedialog.askopenfilename(title="select file",
                                                     filetypes=(('video files', '*.mp4'), ('audio files', 'mp3')))
   folder_path.set(folder_selected)

folder_path = StringVar()  # where clip is stored
var1 = StringVar()  # silence volume threshold
var2 = StringVar()  # silence length threshold
var3 = StringVar()  # silence length buffer

label1 = Label(gui ,text="File name")
label2 = Label(gui, text="Choose volume threshold")
label3 = Label(gui, text="Choose legnth threshold")
label4 = Label(gui, text="Choose legnth of buffer")
label1.grid(row=5, column = 0)
label2.grid(row=6, column = 0)
label3.grid(row=7, column = 0)
label4.grid(row=8, column = 0)
ent1 = Entry(gui, textvariable=folder_path)
ent2 = Entry(gui, textvariable=var1)
ent3 = Entry(gui, textvariable=var2)
ent4 = Entry(gui, textvariable=var3)
ent1.grid(row=5, column=1)
ent2.grid(row=6, column=1)
ent3.grid(row=7, column=1)
ent4.grid(row=8, column=1)
b1 = ttk.Button(gui, text="Choose file",command=get_folder_path)

b1.grid(row=5,column=2)

file = folder_path.get()
volume_threshold = var1.get()
length_threshold = var2.get()
length_of_buffer = var3.get()

b2 = ttk.Button(gui, text="run program", command=script.remove_silences_from_clip)
b2.grid(row=6, column=3)

gui.mainloop()
