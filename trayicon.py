from PyQt5.QtWidgets import QSystemTrayIcon, QWidget, QMenu
from PyQt5.QtCore import QCoreApplication
import qt5gifshower
class SystemTrayIcon(QSystemTrayIcon):
    def __init__(self, icon, parent=None):
        QSystemTrayIcon.__init__(self, icon, parent)
        self.menu = QMenu(parent)
        self.setContextMenu(self.menu)
        #self.menu.triggered.connect(self.exit)
        
        
