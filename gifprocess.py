import requests  #going to need this one from pip
import os
import time
import sys

fname = 'NatLoop.gif'

if os.name == 'nt':
    pass #figure out something different here for Windows. 
else:
    os.chdir(os.path.dirname(sys.argv[0])) #sets working directory to script location. only works for linux

def pullgif():
    weathermap='http://radar.weather.gov/ridge/Conus/Loop/NatLoop.gif'
    r = requests.get(weathermap)
    open(fname, 'wb').write(r.content)

def updategif():
    u = os.path.getmtime(fname)
    agediff = 900   #age difference of file in seconds
    if time.time() > u + agediff:
        pullgif()
        print("updated gif")
    else:
        print("nothing to update")

def check_exist():
    if os.path.isfile(fname) == True:
        updategif()
        print("it existed, checking update")
    else:
        pullgif()
        print("didnt exist, pulling")

check_exist()
