#!/usr/bin/python3
# author: gajdijan@fit.cvut.cz

from tkinter import *
from myImage import *

class AutoScrollbar(Scrollbar):
        """A scrollbar that hides itself if it's not needed."""

        def __init__(self, outer, *args, **kwargs):
            Scrollbar.__init__(self, *args, **kwargs)
            self.preview = outer

        def set(self, lo, hi):
            if (float(lo) <= 0.01 or float(hi) >= 0.99):
                if self.cget('orient') == HORIZONTAL:
                    if self.preview.root.winfo_width() >=   \
                        self.preview.photo.width():
                        self.pack_forget()
                    else:
                        self.pack(side=BOTTOM, fill=X)
                else:
                    if self.preview.root.winfo_height() >=  \
                        self.preview.photo.height():
                        self.pack_forget()
                    else:
                        self.pack(side=RIGHT, fill=Y)
                        self.preview.cnvs.pack_forget()
                        self.preview.cnvs.pack(side='top',
                            expand=True, fill=BOTH
                        )
            Scrollbar.set(self, lo, hi)

class Preview:
    """Displays image - expects image to be represented as MyImage instance"""
    
    WIDTH = 512     # size at the beginning
    HEIGHT = 512    # size at the beginning
    MIN_WIDTH = 128
    MIN_HEIGHT = 64

    def __init__(self, root, title, my_image):
        self.root = root
        self.root.title(title)
        self.image = my_image

        # keep reference to photo or face garbage colletion!
        self.photo = PhotoImage(data=my_image.getdata())
        photo_width, photo_height = self.photo.width(), self.photo.height()
        wndw_width = photo_width if photo_width < self.WIDTH else self.WIDTH
        wndw_height=photo_height if photo_height < self.HEIGHT else self.HEIGHT

        self.root.maxsize(width=photo_width, height=photo_height)
        self.root.minsize(width=self.MIN_WIDTH, height=self.MIN_HEIGHT)

        self.frame = Frame(self.root, width=wndw_width, height=wndw_height)
        self.frame.pack(side=LEFT, expand=True, fill=BOTH)

        self.cnvs = Canvas(self.frame,
            width=photo_width,
            height=photo_height,
            scrollregion=(0, 0, photo_width, photo_height)
        )

        hbar = AutoScrollbar(self, self.frame, orient=HORIZONTAL)
        hbar.pack(side=BOTTOM, fill=X)
        hbar.config(command=self.cnvs.xview)

        vbar = AutoScrollbar(self, self.frame, orient=VERTICAL)
        vbar.pack(side=RIGHT, fill=Y)
        vbar.config(command=self.cnvs.yview)

        self.cnvs.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
        self.cnvs.config(width=wndw_width, height=wndw_height)

        self.cnvsImage = self.cnvs.create_image((photo_width, photo_height),
            image=self.photo,
            anchor = 'se'
        )
        self.cnvs.pack(side='top', expand=True, fill=BOTH)

        self.root.after(500, self.refreshImage)

    def refreshImage(self):
        self.photo = PhotoImage(data=self.image.getdata())
        self.cnvs.itemconfig(self.cnvsImage, image=self.photo)
        self.cnvs.itemconfig(self.cnvsImage, anchor='se')
        self.cnvs.coords(self.cnvsImage,
            (self.photo.width(), self.photo.height())
        )
        wndw_width = self.WIDTH
        if self.photo.width() < self.WIDTH: wndw_width = self.photo.width() 
        wndw_height = self.HEIGHT
        if self.photo.height() < self.HEIGHT: wndw_height = self.photo.height()
        self.cnvs.config(width=wndw_width)
        self.cnvs.config(height=wndw_height)
        self.frame.config(width=wndw_width)
        self.frame.config(height=wndw_width)
        self.root.maxsize(width=self.photo.width(), height=self.photo.height())
        self.root.after(500, self.refreshImage)

if __name__ == '__main__':
    Preview("Window title", MyImage(file2PPM6bytes("Lenna.png")))

