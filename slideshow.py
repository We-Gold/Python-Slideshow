#!/usr/bin/env python3

import os
import tkinter

from itertools import cycle
from PIL import Image, ImageTk
import time
import _thread

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
        self.imageIndex = 0
        self.image_name = self.images[0]
        self.last_time = time.time()
        self.forward = True
        self.skip = False
        self.pause = False

    def set_images(self, images):
         self.images = images

    def center(self):
        self.update_idletasks()
        w = self.winfo_screenwidth()
        h = self.winfo_screenheight()
        self.geometry("%dx%d+0+0" % (w, h))

    def nextImage(self):
        self.image_name = self.images[self.imageIndex % len(self.images)]
        self.imageIndex+=1
        self.set_image()
        self.display()

    def previousImage(self):
        self.image_name = self.images[self.imageIndex % len(self.images)]
        self.imageIndex-=1
        self.set_image()
        self.display()

    def back(self):
        self.forward = False
        self.skip = False

    def toggle_pause(self):
        self.pause = not self.pause

    def skipImage(self):
        self.skip = True
        self.forward = True

    def set_image(self):
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
        self.nextImage()
    
    def display(self):
        self.slide.config(image=self.image)
        self.title(self.image_name)
        self.center()

slide_interval = 4

import glob
import random
import sys
images = glob.glob("*.jpg")
path = "images"
exts = ["jpg", "bmp", "png", "gif", "jpeg"]
images = [(path+"/"+fn) for fn in os.listdir(path) if any(fn.endswith(ext) for ext in exts)]
random.shuffle(images)
random.shuffle(images)

# start the slideshow
global slideshow
slideshow = Slideshow(images, slide_interval)
slideshow.bind("<Escape>",lambda e: slideshow.destroy())

def background():
    slideshow.nextImage()
    while True:
        slideshow.update()
        slideshow.update_idletasks()

        if(slideshow.pause):
            continue

        if(time.time() > slideshow.last_time + slideshow.slide_interval):
            slideshow.nextImage()
            slideshow.last_time = time.time()

        if(slideshow.skip):
            slideshow.skip = False
            slideshow.nextImage()
            slideshow.last_time = time.time()
            continue
        
        if(not slideshow.forward):
            slideshow.forward = True
            slideshow.previousImage()
            slideshow.last_time = time.time()
            continue

########################################################

from flask import Flask, render_template, request
app = Flask(__name__)

@app.route("/")
def index():
	templateData = {
      'paused' : False,
    }
	return render_template('index.html', **templateData)

@app.route("/<action>")
def action(action):
    if(action == "back"):
        slideshow.forward = False
        templateData = {
            'paused' : slideshow.pause,
        }
        return render_template('index.html', **templateData)
    elif(action == "toggle_pause"):
        slideshow.pause = not slideshow.pause
        templateData = {
            'paused' : slideshow.pause,
        }
        return render_template('index.html', **templateData)
    elif(action == "skip"):
        slideshow.skip = True
        templateData = {
            'paused' : slideshow.pause,
        }
        return render_template('index.html', **templateData)

if __name__ == '__main__':
    _thread.start_new_thread(app.run,('0.0.0.0',))
    background()