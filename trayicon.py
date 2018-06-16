from PyQt5.QtWidgets import QSystemTrayIcon, QWidget, QMenu
from PyQt5.QtCore import QCoreApplication
class SystemTrayIcon(QSystemTrayIcon):
    def __init__(self, icon, parent=None):
        QSystemTrayIcon.__init__(self, icon, parent)
        self.menu = QMenu(parent)
        exitAction = self.menu.addAction("Exit")
        self.setContextMenu(self.menu)
        self.menu.triggered.connect(self.exit)

    def exit(self):
        QCoreApplication.exit()
