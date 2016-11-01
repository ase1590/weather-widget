from PIL import Image #Pip install
import time
import os

im = Image.open('NatLoop.gif')
#gif_dimension = 0,0,100,100

def gifcrop(ax,ay,bx,by): #defines two points, a and b. 
    crop = im.crop((ax,ay,ax+bx,ay+by))
    i=0
    try:
        while 1:
            crop.save('out'+str(i)+'.png')
            i += 1
            im.seek(im.tell()+1) #this is broken
    except EOFError:
        print('done')
#use gifcrop(x,y,width,height)
gifcrop(717,285,300,200)
