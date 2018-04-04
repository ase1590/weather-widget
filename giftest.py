from PIL import Image #Pip install windows pillow
from PIL import ImageSequence
import os

##image size args
##kansas: 1361,500,510,270
#x = 0
#y = 0
#width = 100
#height = 100

# this file is broken and only shows washington##############

def gifcrop(ax,ay,bx,by): #defines two points, a and b. 
    im = Image.open('NatLoop.gif')
#    if os.path.isdir('somedir'):
    for frame in enumerate(ImageSequence.Iterator(im)):
        crop = im.crop((ax,ay,ax+bx,ay+by))
        crop.convert('RGBA')
        #print('saved %d' % i)
        print(im.format, im.size, im.mode)
    frames = [frame.copy() for frame in ImageSequence.Iterator(im)]
    crop.convert('L').save('out.gif', save_all=True, append_images=frames[0:], duration=1)
#use gifcrop(x,y,width,height)
gifcrop(1361, 500, 510, 270)
