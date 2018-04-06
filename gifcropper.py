# uses python3-pillow
# gif sourced from http://radar.weather.gov/ridge/Conus/Loop/NatLoop.gif
from PIL import Image
from PIL import ImageSequence

def gifcrop(ax, ay, bx, by):
    im = Image.open('NatLoop.gif')
    #crop = im.crop((ax,ay,ax+bx,ay+by))
    frames = [frame.copy().crop((ax, ay, ax+bx, ay+by)).convert('RGBA') for frame in ImageSequence.Iterator(im)]
    frames[0].save('region.gif', save_all=True, append_images=frames[1:])



if __name__ == "__main__":
    gifcrop(1361, 500, 510, 270)
