# https://medium.com/@webmamoffice/getting-started-gui-s-with-python-pyqt-qthread-class-1b796203c18c
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import pyqtSignal
from http.client import HTTPSConnection
from bs4 import BeautifulSoup
import time


font_but = QtGui.QFont()
font_but.setFamily("Segoe UI Symbol")
font_but.setPointSize(10)
font_but.setWeight(95)


class QThread1(QtCore.QThread):

    sig1 = pyqtSignal(str, int, int)

    def __init__(self, parent=None):
        QtCore.QThread.__init__(self, parent)

    def on_source(self, lineftxt):
        self.source_txt = lineftxt

    def run(self):
        self.running = True
        while self.running:
            try:
                conn = HTTPSConnection(self.source_txt)
                conn.request('GET', "/")
                req = conn.getresponse()
                page = req.read().decode('utf-8')
                bs = BeautifulSoup(page, 'html.parser')
                links = bs.find_all('a')
                l = len(links)
                for i in range(0, l):
                    if self.running is True:
                        self.sig1.emit(str(links[i]), i, l)
                        time.sleep(1.5)
            except Exception as err:
                self.sig1.emit(str(err), 0, 1)


class PushBut1(QtWidgets.QPushButton):
    def __init__(self, parent=None):
        super(PushBut1, self).__init__(parent)
        self.setMouseTracking(True)
        self.setStyleSheet("margin: 1px; padding: 7px; background-color: rgba(1,255,255,100); color: rgba(0,190,255,255); border-style: solid;"
                           "border-radius: 3px; border-width: 0.5px; border-color: rgba(127,127,255,255);")

    def enterEvent(self, event):
        if self.isEnabled() is True:
            self.setStyleSheet("margin: 1px; padding: 7px; background-color: rgba(1,255,255,100); color: rgba(0,230,255,255);"
                               "border-style: solid; border-radius: 3px; border-width: 0.5px; border-color: rgba(0,230,255,255);")
        if self.isEnabled() is False:
            self.setStyleSheet("margin: 1px; padding: 7px; background-color: rgba(1,255,255,100); color: rgba(0,190,255,255); border-style: solid;"
                               "border-radius: 3px; border-width: 0.5px; border-color: rgba(127,127,255,255);")

    def leaveEvent(self, event):
        self.setStyleSheet("margin: 1px; padding: 7px; background-color: rgba(1,255,255,100); color: rgba(0,190,255,255); border-style: solid;"
                           "border-radius: 3px; border-width: 0.5px; border-color: rgba(127,127,255,255);")


class QthreadApp(QtWidgets.QWidget):

    sig = pyqtSignal(str)

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.setWindowTitle("QThread Application")
        self.setWindowIcon(QtGui.QIcon("Path/to/Your/image/file.png"))
        self.setMinimumWidth(resolution.width() / 3)
        self.setMinimumHeight(resolution.height() / 1.5)
        self.setStyleSheet("QWidget {background-color: rgba(0,41,59,255);} QScrollBar:horizontal {width: 1px; height: 1px;"
                           "background-color: rgba(0,41,59,255);} QScrollBar:vertical {width: 1px; height: 1px;"
                           "background-color: rgba(0,41,59,255);}")
        self.linef = QtWidgets.QLineEdit(self)
        self.linef.setPlaceholderText("Connect to www.example.com")
        self.linef.setStyleSheet("margin: 1px; padding: 7px; background-color: rgba(0,255,255,100); color: rgba(0,190,255,255);"
                                 "border-style: solid; border-radius: 3px; border-width: 0.5px; border-color: rgba(0,140,255,255);")
        self.textf = QtWidgets.QTextEdit(self)
        self.textf.setPlaceholderText("Results...")
        self.textf.setStyleSheet("margin: 1px; padding: 7px; background-color: rgba(0,255,255,100); color: rgba(0,190,255,255);"
                                 "border-style: solid; border-radius: 3px; border-width: 0.5px; border-color: rgba(0,140,255,255);")
        self.but1 = PushBut1(self)
        self.but1.setText("⯈")
        self.but1.setFixedWidth(72)
        self.but1.setFont(font_but)
        self.but2 = PushBut1(self)
        self.but2.setText("⯀")
        self.but2.setFixedWidth(72)
        self.but2.setFont(font_but)
        self.grid1 = QtWidgets.QGridLayout()
        self.grid1.addWidget(self.linef, 0, 0, 1, 12)
        self.grid1.addWidget(self.but1, 0, 12, 1, 1)
        self.grid1.addWidget(self.but2, 0, 13, 1, 1)
        self.grid1.addWidget(self.textf, 1, 0, 13, 14)
        self.grid1.setContentsMargins(7, 7, 7, 7)
        self.setLayout(self.grid1)
        self.but1.clicked.connect(self.on_but1)
        self.but2.clicked.connect(self.on_but2)

    def on_but1(self):
        self.textf.clear()
        lineftxt = self.linef.text()
        self.thread1 = QThread1()
        self.sig.connect(self.thread1.on_source)
        self.sig.emit(lineftxt)
        self.thread1.start()
        self.thread1.sig1.connect(self.on_info)
        self.but1.setEnabled(False)

    def on_but2(self):
        try:
            self.thread1.running = False
            time.sleep(2)
            self.but1.setEnabled(True)
        except:
            pass

    def on_info(self, info, i, l):
        if i == l-1:
            self.textf.clear()
            self.textf.append(str(info))
        else:
            self.textf.append(str(info))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    desktop = QtWidgets.QApplication.desktop()
    resolution = desktop.availableGeometry()
    myapp = QthreadApp()
    myapp.setWindowOpacity(0.95)
    myapp.show()
    myapp.move(resolution.center() - myapp.rect().center())
    sys.exit(app.exec_())
else:
    desktop = QtWidgets.QApplication.desktop()
    resolution = desktop.availableGeometry()



"""
# One Side communication


class QThread1(QtCore.QThread):

    sig1 = pyqtSignal(str, int, int)

    def __init__(self, parent=None):
        QtCore.QThread.__init__(self, parent)

    def run(self):
        self.running = True
        while self.running:
            try:
                conn = HTTPSConnection(source_txt)
                conn.request('GET', "/")
                req = conn.getresponse()
                page = req.read().decode('utf-8')
                bs = BeautifulSoup(page, 'html.parser')
                links = bs.find_all('a')
                l = len(links)
                for i in range(0, l):
                    if self.running is True:
                        self.sig1.emit(str(links[i]), i, l)
                        time.sleep(1.5)
            except Exception as err:
                self.sig1.emit(str(err), 0, 1)


def on_but1(self):
    self.textf.clear()
    global source_txt
    source_txt = self.linef.text()
    self.thread1 = QThread1()
    self.thread1.start()
    self.thread1.sig1.connect(self.on_info)
    self.but1.setEnabled(False)

"""

