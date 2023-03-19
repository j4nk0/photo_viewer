#!/usr/bin/python3
# author: gajdijan@fit.cvut.cz

import threading as th
from preview import *
from myImage import *

class Controller:
    
    def __init__(self, root, img):
        self.root = root
        self.img = img
        self.frame = Frame(root, )
        self.window = Toplevel(self.frame)
        self.window.resizable(False, False)
        self.window.title('Controller')

        invert_button = Button(self.window, text="Invert",
            command=self.invert
        )
        invert_button.pack(fill=BOTH, expand=1)
        grayscale_button = Button(self.window, text="Grayscale",
            command=self.grayscale
        )
        grayscale_button.pack(fill=BOTH, expand=1)
        mirror_button = Button(self.window, text="Mirror",
            command=self.mirror
        )
        mirror_button.pack(fill=BOTH, expand=1)
        darken_button = Button(self.window, text="- Brightnes",
            command=self.darken
        )
        darken_button.pack(fill=BOTH, expand=1)
        bringhten_button = Button(self.window, text="+ Brightnes",
            command=self.brighten
        )
        bringhten_button.pack(fill=BOTH, expand=1)
        rotate_clockwise_button = Button(self.window, text="Rotate +90",
            command=self.rotate_clockwise
        )
        rotate_clockwise_button.pack(fill=BOTH, expand=1)
        rotate_counterclockwise_button = Button(self.window, text="Rotate -90",
            command=self.rotate_counterclockwise
        )
        rotate_counterclockwise_button.pack(fill=BOTH, expand=1)
        sharpen_button = Button(self.window, text="Sharpen",
            command=self.sharpen
        )
        sharpen_button.pack(fill=BOTH, expand=1)

    def invert(self):
        th.Thread(target=self.img.invert).start()

    def grayscale(self):
        th.Thread(target=self.img.grayscale).start()
        
    def mirror(self):
        th.Thread(target=self.img.mirror).start()

    def darken(self):
        th.Thread(target=self.img.darken).start()

    def brighten(self):
        th.Thread(target=self.img.brighten).start()

    def rotate_clockwise(self):
        th.Thread(target=self.img.rotate_clockwise).start()

    def rotate_counterclockwise(self):
        th.Thread(target=self.img.rotate_counterclockwise).start()

    def sharpen(self):
        th.Thread(target=self.img.sharpen).start()


