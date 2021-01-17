#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import gifdownload, gifcropper, trayicon, statelist
from PyQt5.QtCore import Qt, QByteArray, QTimer, QSettings, QPoint, QSize
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QSizePolicy, QVBoxLayout, QAction, QSizeGrip
from PyQt5.QtGui import QMovie, QIcon

r = gifdownload.grabber('http://radar.weather.gov/ridge/Conus/Loop/NatLoop.gif')



class ImagePlayer(QWidget):
    def __init__(self, filename, title, parent=None):
        super(ImagePlayer, self).__init__()

        #set screen save
        self.settings = QSettings('settings.ini', QSettings.IniFormat)

        # set up exit action
        quitAction = QAction("E&xit", self, shortcut = "Ctrl+Q", triggered = self.close)
        self.addAction(quitAction)
        self.setContextMenuPolicy(Qt.ActionsContextMenu)


        # Load the file into a QMovie
        self.movie = QMovie(filename, QByteArray(), self)

        #size = self.movie.scaledSize()
        self.setWindowFlags(Qt.FramelessWindowHint| Qt.WindowStaysOnBottomHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        #self.resize(self.settings.value("size", QSize(size.width, size.height)))
        self.move(self.settings.value("pos", QPoint(50, 50)))
        #self.setGeometry(parser.getint('screen_position', 'x'), parser.getint('screen_position', 'y'), size.width(), size.height())
        self.setWindowTitle(title)

        self.movie_screen = QLabel()
        # Make label fit the gif
        self.movie_screen.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.movie_screen.setAlignment(Qt.AlignCenter)
        self.movie_screen.setScaledContents(True) #allow image to scale with label
        self.setMinimumSize(QSize(200, 150)) #restrict it to a min size
        self.movie_screen.setStyleSheet(open('style.css').read())

        # Create the layout
        main_layout = QVBoxLayout()
        sizegrip = QSizeGrip(self) #enable size grip for scaling borderless window
        main_layout.addWidget(self.movie_screen)
        main_layout.addWidget(sizegrip, 0, Qt.AlignBottom | Qt.AlignRight)

        self.setLayout(main_layout)

        # Add the QMovie object to the label
        self.movie.setCacheMode(QMovie.CacheAll)
        self.movie.setSpeed(self.settings.value("playspeed", 30, type=int)) #set relative playback speed percentage
        self.movie_screen.setMovie(self.movie)
        self.movie.start()
        self.movie.loopCount()

        self.timer = QTimer(self)
        self.timer.singleShot(2000, self.GetMap)
        self.timer.timeout.connect(self.GetMap)
        self.timer.start(901000) #milliseconds. 1000 is 1 second

    #override closing the program. use self.close to call this
    def closeEvent(self,event):
        #self.settings.setValue("size", self.size())
        self.settings.setValue("pos", self.pos())
        event.accept()


    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragposition = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPos()- self.dragposition)
            event.accept()

    def GetMap(self):
        r.downloadCheck('NatLoop.gif')
        #gifcropper.gifcrop(1361, 500, 510, 270) #TODO: only crop if gif updates
        gifcropper.gifcrop(self.settings.value("x", 1361, type=int), 
                           self.settings.value("y", 500, type=int), 
                           self.settings.value("width", 510, type=int), 
                           self.settings.value("height", 270, type=int)) #TODO: only crop if gif updates
        self.movie = QMovie(gif, QByteArray(), self)
        self.movie_screen.setMovie(self.movie)
        self.movie.setSpeed(self.settings.value("playspeed", 30, type=int)) #set relative playback speed percentage
        self.movie.start()
        print("refresh done")

    def simpleGetMap(self):
        r.SimpleDownload('NatLoop.gif')
        gifcropper.gifcrop(self.settings.value("x", 1361, type=int),
                           self.settings.value("y", 500, type=int),
                           self.settings.value("width", 510, type=int),
                           self.settings.value("height", 270, type=int)) #TODO: only crop if gif updates
        self.movie = QMovie(gif, QByteArray(), self)
        self.movie_screen.setMovie(self.movie)
        self.movie.setSpeed(self.settings.value("playspeed", 30, type=int))
        self.movie.start()
        print("refresh done")
        self.movie_screen.setMovie(self.movie)
        self.movie.start

    def speedsetter(self, speed):
        self.movie.setSpeed(speed)
        self.settings.setValue("playspeed", speed)

    def mapsetter(self, x, y, w, h):
        self.settings.setValue("x", x)
        self.settings.setValue("y", y)
        self.settings.setValue("width", w)
        self.settings.setValue("height", h)
        self.simpleGetMap()


if __name__ == "__main__":

    # set gif name to grab
    gif = "region.gif"

    app = QApplication(sys.argv)

    # load in tray icon class and run
    mytrayicon = trayicon.SystemTrayIcon(QIcon("TrayIcon.png"))
    mytrayicon.show()

    # show the radar map
    player = ImagePlayer('loading.png', "WeatherWidget") #show an initial loading image

    playspeed = mytrayicon.menu.addMenu("Playspeed")
    playspeed.addAction("200%", lambda: player.speedsetter(200))
    playspeed.addAction("100%", lambda: player.speedsetter(100))
    playspeed.addAction("50%", lambda: player.speedsetter(50))
    playspeed.addAction("30% (default)", lambda: player.speedsetter(30))
    playspeed.addAction("25%", lambda: player.speedsetter(25))
    playspeed.addAction("10%", lambda: player.speedsetter(10))

    statecombo = statelist.us_state
    stateselector = mytrayicon.menu.addMenu("States")
        #for key, value in statecombo.items():
        #    stateselector.addAction("%s" %key, lambda: print(key,value[0], value[1], value[2], value[3])) #lambda breaks iteration
    # TODO: apologize for lambda abuse down below.
    stateselector.addAction("Alabama", lambda: player.mapsetter(2000,854, 510, 270))
    stateselector.addAction("Arizona", lambda: player.mapsetter(615,740, 510, 340))
    stateselector.addAction("Arkansas", lambda: player.mapsetter(663,677, 450, 390))
    stateselector.addAction("California", lambda: player.mapsetter(147,425, 667, 594))
    stateselector.addAction("Colorado", lambda: player.mapsetter(959,493, 510, 270))
    stateselector.addAction("Connecticut", lambda: player.mapsetter(2775,361, 510, 270))
    stateselector.addAction("Delaware", lambda: player.mapsetter(2630,517, 510, 270))
    stateselector.addAction("Florida", lambda: player.mapsetter(2196,987, 488, 442))
    stateselector.addAction("Georgia", lambda: player.mapsetter(2285,847, 366, 278))
    stateselector.addAction("Idaho", lambda: player.mapsetter(507,80, 462, 432))
    stateselector.addAction("Illinois", lambda: player.mapsetter(1967,418, 349, 342))
    stateselector.addAction("Indiana", lambda: player.mapsetter(2097,455, 407, 270))
    stateselector.addAction("Iowa", lambda: player.mapsetter(1693,328, 407, 270))
    stateselector.addAction("Kansas", lambda: player.mapsetter(1361,500, 510, 270))
    stateselector.addAction("Kentucky", lambda: player.mapsetter(2077,575, 510, 270))
    stateselector.addAction("Louisiana", lambda: player.mapsetter(1800,955, 380, 270))
    stateselector.addAction("Maine", lambda: player.mapsetter(3100,161, 284, 288))
    stateselector.addAction("Maryland", lambda: player.mapsetter(2722,518, 238, 229))
    stateselector.addAction("Massachusetts", lambda: player.mapsetter(2953,371, 280, 171))
    stateselector.addAction("Michigan", lambda: player.mapsetter(2017,103, 510, 391))
    stateselector.addAction("Minnesota", lambda: player.mapsetter(1636,45, 521, 357))
    stateselector.addAction("Mississippi", lambda: player.mapsetter(1945,834, 330, 320))
    stateselector.addAction("Missouri", lambda: player.mapsetter(1737,537, 445, 274))
    stateselector.addAction("Montana", lambda: player.mapsetter(612,81, 752, 270))
    stateselector.addAction("Nebraska", lambda: player.mapsetter(1284,374, 525, 250))
    stateselector.addAction("Nevada", lambda: player.mapsetter(389,452, 402, 414))
    stateselector.addAction("New Hampshire", lambda: player.mapsetter(237,200, 3004, 279))
    stateselector.addAction("New Jersey", lambda: player.mapsetter(2846,470, 200, 200))
    stateselector.addAction("New Mexico", lambda: player.mapsetter(973,704, 429, 366))
    stateselector.addAction("New York", lambda: player.mapsetter(2612,294, 510, 256))
    stateselector.addAction("North Carolina", lambda: player.mapsetter(2397,722, 510, 220))
    stateselector.addAction("North Dakota", lambda: player.mapsetter(1262,54, 510, 230))
    stateselector.addAction("Ohio", lambda: player.mapsetter(2148,432, 307, 290))
    stateselector.addAction("Oklahoma", lambda: player.mapsetter(1356,696, 510, 270))
    stateselector.addAction("Oregon", lambda: player.mapsetter(133,63, 510, 270))
    stateselector.addAction("Pennsylvania", lambda: player.mapsetter(2542,433, 480, 200))
    stateselector.addAction("Rhode Island", lambda: player.mapsetter(3018,391, 200, 200))
    stateselector.addAction("South Carolina", lambda: player.mapsetter(2432,797, 341, 256))
    stateselector.addAction("South Dakota", lambda: player.mapsetter(1274,203, 510, 270))
    stateselector.addAction("Tennessee", lambda: player.mapsetter(2058,684, 510, 220))
    stateselector.addAction("Texas", lambda: player.mapsetter(1134,728, 796, 652))
    stateselector.addAction("Utah", lambda: player.mapsetter(670,447, 426, 332))
    stateselector.addAction("Vermont", lambda: player.mapsetter(2958,268, 200, 200))
    stateselector.addAction("Virginia", lambda: player.mapsetter(2432,598, 481, 206))
    stateselector.addAction("Washington", lambda: player.mapsetter(137,55, 498, 245))
    stateselector.addAction("West Virginia", lambda: player.mapsetter(2458,539, 350, 217))
    stateselector.addAction("Wisconsin", lambda: player.mapsetter(1900,186, 371, 270))
    stateselector.addAction("Wyoming", lambda: player.mapsetter(874,279, 469, 268))


    mytrayicon.menu.addAction("Refresh", player.simpleGetMap) #add manual refresh action
    mytrayicon.menu.addAction("Exit", player.close)
    
    player.show()
    sys.exit(app.exec_())

