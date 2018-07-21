#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import gifdownload, gifcropper, trayicon, statelist
from PyQt5.QtCore import Qt, QByteArray, QSettings, QTimer, QSettings, QPoint, QSize
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
        self.setMinimumSize(QSize(200,150)) #restrict it to a min size

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
        gifcropper.gifcrop(1361, 500, 510, 270) #TODO: only crop if gif updates
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

    def speedsetter(self, speed):
        self.movie.setSpeed(speed)
        self.settings.setValue("playspeed", speed)

    def mapsetter(self, x, y, w, h):
        self.settings.setValue("x", x)
        self.settings.setValue("y", y)
        self.settings.setValue("width", w)
        self.settings.setValue("height", h)


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
    for key, value in statecombo.items():
        stateselector.addAction("%s" %key, lambda: print(key,value[0], value[1], value[2], value[3])) #lambda breaks iteration

    mytrayicon.menu.addAction("Refresh", player.simpleGetMap) #add manual refresh action
    mytrayicon.menu.addAction("Exit", player.close)
    
    player.show()
    sys.exit(app.exec_())

