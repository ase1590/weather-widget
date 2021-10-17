#!/usr/bin/python
# This Python file uses the following encoding: utf-8
import sys
import os

from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6 import QtCore, QtWidgets
# created from /usr/lib/qt6/rcc -g python qml.qrc -o resources.py
# converts the resources to bytes and can be called from qrc:/some/file.jpg
import resources


if __name__ == "__main__":
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)
    app = QGuiApplication(sys.argv)
    app.setApplicationName("WeatherWidget")
    app.setOrganizationName("AllspiceInc")
    app.setOrganizationDomain("AllspiceInc")
    engine = QQmlApplicationEngine()
    engine.load(os.path.join(os.path.dirname(__file__), "main.qml"))

    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec())
