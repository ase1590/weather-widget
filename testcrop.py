from PIL import Image
import time
import os
im = Image.open('NatLoop.gif')
# NatLoop.gif can be gotten from http://radar.weather.gov/Conus/Loop/NatLoop.gif
def docrop():
    crop = im.crop((335,345,565,560))
    i=0
    while os.path.exists("out%s.png" % i):
        i += 1
    crop.save("out%s.png" % i)
    print("out%s.png" % i)

for tt in range(7):
    im.seek(im.tell()+1)
    docrop()
    tt +=1
    print("we are at %s" % tt)
