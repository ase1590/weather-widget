import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15
import QtWebEngine 1.1
import Qt.labs.platform 1.1
import Qt.labs.settings 1.1 //see https://doc.qt.io/qt-5/qml-qt-labs-settings-settings.html

ApplicationWindow {
    width: 600
    id: rootWindow
    height: 400
    visible: true
    flags: Qt.FramelessWindowHint|Qt.WA_TranslucentBackground//|Qt.WindowStaysOnBottomHint
    title: qsTr("Weather-Widget")
    color: "#00000000"
    Settings {
        property alias x: rootWindow.x
        property alias y: rootWindow.y
        property alias width: rootWindow.width
        property alias height: rootWindow.height
    }
    SystemTrayIcon {
        visible: true
        tooltip: "WeatherWidget"
        icon.source: "TrayIcon.png"

        menu: Menu {
            MenuItem {
                text: "Widget mode"
                checkable: true
                checked: true
                onCheckedChanged: {
                    if(checked)
                        rootWindow.flags = rootWindow.flags |Qt.FramelessWindowHint
                    else
                        rootWindow.flags = rootWindow.flags & ~Qt.FramelessWindowHint
                    if(checked)
                        nws.enabled = false
                    else
                        nws.enabled = true
                        toggletimer.stop()
                }

                }
            MenuItem {
                text: qsTr("Refresh")
                onTriggered: nws.reload()
            }
            MenuItem {
                text: qsTr("Quit")
                onTriggered: Qt.quit()
            }
        }
    }



    Rectangle {
        id: main
        width: parent.width
        height: parent.height
        visible: true
        color: "#323232"
        //border.color: "#323232"
        //border.width: 6
        radius: 8

        MouseArea {
            acceptedButtons: Qt.RightButton|Qt.LeftButton
            anchors.fill: parent
            onPressed: { pos = Qt.point(mouse.x, mouse.y) }
            onPositionChanged: {
                var diff = Qt.point(mouse.x - pos.x, mouse.y - pos.y)
                ApplicationWindow.window.x += diff.x
                ApplicationWindow.window.y += diff.y
            }
            onDoubleClicked: {
                toggletimer.start()
                nws.enabled = true;
            }


            property point pos
        }


        WebEngineView {
            id: nws
            //visible: false
            width: main.width-8
            height: main.height-8
            anchors.centerIn: main
            enabled: false //toggle clickable
            Timer {
                id: refreshtimer
                interval: 300000; running: true; repeat: true
                onTriggered: nws.reload()
            }
            Timer {
                id: toggletimer
                interval: 10000; running: false; repeat: false
                onTriggered: nws.enabled = false;
            }
            url: "http://radar.weather.gov"
            Settings {
                property alias url: nws.url
            }

        }
    }


}
