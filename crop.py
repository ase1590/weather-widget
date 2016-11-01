from PIL import Image #Pip install
from PIL import ImageSequence
#import time
#import os

im = Image.open('NatLoop.gif')

#image size args
#kansas: 1361,500,510,270
x = 0
y = 0
width = 100
height = 100

def gifcrop(ax,ay,bx,by): #defines two points, a and b. 
    for i, frame in enumerate(ImageSequence.Iterator(im)):
        crop = im.crop((ax,ay,ax+bx,ay+by))
        crop.convert('RGB').save('out%d.png' % i)
        print('saved %d' % i)
        print(im.format, im.size, im.mode)
#use gifcrop(x,y,width,height)
gifcrop(1361, 500, 510, 270)
