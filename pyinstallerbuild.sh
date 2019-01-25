#!/bin/bash
pyinstaller --noconsole qt5gifshower.py --add-data style.css:. --add-data TrayIcon.png:. --add-data loading.png:.
