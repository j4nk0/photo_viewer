#!/usr/bin/python3
# author: gajdijan@fit.cvut.cz

from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showerror

#import threading as th

from myImage import *
from controller import *

#def startPreview(tk, title, image):

root = Tk()
root.withdraw()
filename = askopenfilename()#filetypes=(("All files", "*.*") ))
img = None
try:
    img = MyImage(file2PPM6bytes(filename))
except ValueError:
    showerror(title = "Error", message = "Failed to load file")
    exit()

#prevThread = th.Thread(target=startPreview, args=(root, filename, img))
#prevThread.start()
root.deiconify()
Preview(root, filename, img)
Controller(root, img)
root.mainloop()
#ctrl = Controller(img)

