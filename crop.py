from PIL import Image #Pip install
from PIL import ImageSequence
import time
import os

im = Image.open('NatLoop.gif')
#gif_dimension = 0,0,100,100

def gifcrop(ax,ay,bx,by): #defines two points, a and b. 
    i=0
    for frame in ImageSequence.Iterator(im):
        crop = im.crop((ax,ay,ax+bx,ay+by))
        i+=1
        crop.save('out'+str(i)+'.png')
        print('saved %s' % i)
#use gifcrop(x,y,width,height)
gifcrop(717,285,300,200)
