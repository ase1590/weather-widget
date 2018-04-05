#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtCore import Qt, QByteArray, QSettings
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QSizePolicy, QVBoxLayout, QAction
from PyQt5.QtGui import QMovie

class ImagePlayer(QWidget):
    def __init__(self, filename, title, parent=None):
        QWidget.__init__(self, parent)

        #set save position
        #self.settings = QtCore.qse
        # set up exit action
        quitAction = QAction("E&xit", self, shortcut = "Ctrl+Q", triggered = QApplication.instance().quit)
        self.addAction(quitAction)
        self.setContextMenuPolicy(Qt.ActionsContextMenu)

        # Load the file into a QMovie
        self.movie = QMovie(filename, QByteArray(), self)

        size = self.movie.scaledSize()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setGeometry(200, 200, size.width(), size.height())
        self.setWindowTitle(title)

        self.movie_screen = QLabel()
        # Make label fit the gif
        self.movie_screen.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.movie_screen.setAlignment(Qt.AlignCenter)

        # Create the layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.movie_screen)

        self.setLayout(main_layout)

        # Add the QMovie object to the label
        self.movie.setCacheMode(QMovie.CacheAll)
        self.movie.setSpeed(50) #set relative playback speed percentage
        self.movie_screen.setMovie(self.movie)
        self.movie.start()
        self.movie.loopCount()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragposition = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPos()- self.dragposition)
            event.accept()



if __name__ == "__main__":
    gif = "region.gif"
    app = QApplication(sys.argv)
    player = ImagePlayer(gif, "WeatherApp")
    player.show()
    sys.exit(app.exec_())