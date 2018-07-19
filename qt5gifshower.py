#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import gifdownload, gifcropper, trayicon
from PyQt5.QtCore import Qt, QByteArray, QSettings, QTimer, QSettings, QPoint, QSize
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QSizePolicy, QVBoxLayout, QAction
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
        #self.movie_screen.setMinimumWidth(300)
        #self.movie_screen.setMinimumHeight(200)
        self.movie_screen.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.movie_screen.setAlignment(Qt.AlignCenter)

        # Create the layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.movie_screen)

        self.setLayout(main_layout)

        # Add the QMovie object to the label
        self.movie.setCacheMode(QMovie.CacheAll)
        self.movie.setSpeed(30) #set relative playback speed percentage
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
        self.movie.setSpeed(30) #set relative playback speed percentage
        self.movie.start()
        print("refresh done")

    def simpleGetMap(self):
        r.SimpleDownload('NatLoop.gif')
        gifcropper.gifcrop(1361, 500, 510, 270) #TODO: only crop if gif updates
        self.movie = QMovie(gif, QByteArray(), self)
        self.movie_screen.setMovie(self.movie)
        self.movie.start()
        print("refresh done")


if __name__ == "__main__":

    # set gif name to grab
    gif = "region.gif"

    app = QApplication(sys.argv)

    # load in tray icon class and run
    mytrayicon = trayicon.SystemTrayIcon(QIcon("TrayIcon.png"))
    mytrayicon.show()

    # show the radar map
    player = ImagePlayer('loading.png', "WeatherWidget") #show an initial loading image
    mytrayicon.menu.addAction("Refresh", player.simpleGetMap) #add manual refresh action
    mytrayicon.menu.addAction("Exit", player.close)

    player.show()
    sys.exit(app.exec_())

