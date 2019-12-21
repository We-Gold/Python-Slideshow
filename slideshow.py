#!/usr/bin/env python3

import os
import tkinter

from itertools import cycle
from PIL import Image, ImageTk

class Slideshow(tkinter.Tk):
    def __init__(self, images, slide_interval):
        tkinter.Tk.__init__(self)
        self.geometry("+0+0")
        self.slide_interval = slide_interval
        self.images = None
        self.set_images(images)
        self.slide = tkinter.Label(self)
        self.slide.pack()
        self.attributes("-fullscreen",True)
        self.configure(background='black',borderwidth=0,highlightthickness=0)

    def set_images(self, images):
         self.images = cycle(images)

    def center(self):
        self.update_idletasks()
        w = self.winfo_screenwidth()
        h = self.winfo_screenheight()
        self.geometry("%dx%d+0+0" % (w, h))

    def set_image(self):
        self.image_name = next(self.images)
        filename, ext = os.path.splitext(self.image_name)

        w = self.winfo_screenwidth()
        h = self.winfo_screenheight()

        pilImage = Image.open(self.image_name)
        imgWidth, imgHeight = pilImage.size
        if imgWidth > w or imgHeight > h:
            ratio = min(w/imgWidth, h/imgHeight)
            imgWidth = int(imgWidth*ratio)
            imgHeight = int(imgHeight*ratio)
            pilImage = pilImage.resize((imgWidth,imgHeight), Image.ANTIALIAS)
        self.image = ImageTk.PhotoImage(pilImage)
        
    def main(self):
        self.set_image()
        self.slide.config(image=self.image)
        self.title(self.image_name)
        self.center()
        self.after(self.slide_interval, self.start)
    
    def start(self):
        self.main()
        self.mainloop()


slide_interval = 4000

import glob
import random
images = glob.glob("*.jpg")
path = "images"
exts = ["jpg", "bmp", "png", "gif", "jpeg"]
images = [(path+"/"+fn) for fn in os.listdir(path) if any(fn.endswith(ext) for ext in exts)]
random.shuffle(images)
random.shuffle(images)

# start the slideshow
slideshow = Slideshow(images, slide_interval)
slideshow.bind("<Escape>",lambda e: slideshow.destroy())
slideshow.start()