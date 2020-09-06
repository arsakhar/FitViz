from PyQt5.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout, QWidget, QLabel, QLineEdit
from PyQt5.QtWidgets import QPushButton, QListWidget, QStackedLayout
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QIcon

from scripts.UI.MeasurementsPanel import MeasurementsPanel
from scripts.Helper.Resources import *

"""
Widget that displays udp panel
"""
class UdpPanel(QWidget):
    START_BUTTON_INDEX = 0
    PAUSE_BUTTON_INDEX = 1

    def __init__(self, parent):
        super().__init__(parent)

        self.initUI()

    def initUI(self):
        self.centralFrame = QFrame(self)
        self.centralFrame.setFrameShape(QFrame.NoFrame)
        self.centralFrame.setFrameShadow(QFrame.Raised)
        self.centralFrame.setContentsMargins(0, 0, 0, 0)
        self.centralFrame.setStyleSheet("background-color: rgb(27, 29, 35);"
                                        "border: none;")

        self.contentFrame = QFrame(self.centralFrame)
        self.contentFrame.setFrameShape(QFrame.NoFrame)
        self.contentFrame.setFrameShadow(QFrame.Raised)
        self.contentFrame.setContentsMargins(0, 0, 0, 0)
        self.contentFrame.setStyleSheet("border: none;")

        self.udpFrame = QFrame(self.contentFrame)
        self.udpFrame.setFrameShape(QFrame.NoFrame)
        self.udpFrame.setFrameShadow(QFrame.Raised)
        self.udpFrame.setContentsMargins(0, 0, 0, 0)

        self.measurementsFrame = QFrame(self.udpFrame)
        self.measurementsFrame.setFrameShape(QFrame.NoFrame)
        self.measurementsFrame.setFrameShadow(QFrame.Raised)
        self.measurementsFrame.setContentsMargins(0, 0, 0, 0)
        self.measurementsFrame.setStyleSheet("border: none;")

        self.measurementsPanel = MeasurementsPanel(self.measurementsFrame)
        self.activeMeasurements = self.measurementsPanel.activeMeasurements
        self.addBtn = self.measurementsPanel.addBtn
        self.removeBtn = self.measurementsPanel.removeBtn

        self.measurementsLayout = QVBoxLayout(self.measurementsFrame)
        self.measurementsLayout.addWidget(self.measurementsPanel)
        self.measurementsLayout.setContentsMargins(0, 0, 0, 0)

        self.configurationFrame = QFrame(self.udpFrame)
        self.configurationFrame.setFrameShape(QFrame.NoFrame)
        self.configurationFrame.setFrameShadow(QFrame.Raised)
        self.configurationFrame.setContentsMargins(0, 0, 0, 0)
        self.configurationFrame.setStyleSheet("background: rgb(15,15,15);"
                                              "border: 1px solid gray;"
                                              "border-radius: 5px;")

        self.networkingFrame = QFrame(self.contentFrame)
        self.networkingFrame.setFrameShape(QFrame.NoFrame)
        self.networkingFrame.setFrameShadow(QFrame.Raised)
        self.networkingFrame.setContentsMargins(0, 0, 0, 0)
        self.networkingFrame.setStyleSheet("border: none;")

        self.ipAddressFrame = QFrame(self.networkingFrame)
        self.ipAddressFrame.setFrameShape(QFrame.NoFrame)
        self.ipAddressFrame.setFrameShadow(QFrame.Raised)
        self.ipAddressFrame.setContentsMargins(0, 0, 0, 0)
        self.ipAddressFrame.setStyleSheet("border: none;")

        self.ipAddressField = LineEdit(self.ipAddressFrame)
        self.ipAddressField.setInputMask("000.000.000.000;_")

        self.ipAddressLabel = Label(self.ipAddressFrame)
        self.ipAddressLabel.setText("IP Address: ")

        self.ipAddressLayout = QHBoxLayout(self.ipAddressFrame)
        self.ipAddressLayout.addWidget(self.ipAddressLabel, alignment=Qt.AlignRight | Qt.AlignVCenter)
        self.ipAddressLayout.addWidget(self.ipAddressField, alignment=Qt.AlignLeft | Qt.AlignVCenter)
        self.ipAddressLayout.setContentsMargins(0, 0, 0, 0)

        self.portFrame = QFrame(self.networkingFrame)
        self.portFrame.setFrameShape(QFrame.NoFrame)
        self.portFrame.setFrameShadow(QFrame.Raised)
        self.portFrame.setContentsMargins(0, 0, 0, 0)
        self.portFrame.setStyleSheet("border: none;")

        self.portField = LineEdit(self.portFrame)
        self.portField.setStyleSheet("QLineEdit{ "
                                     "border-width: 1px; "
                                     "border-style: solid; "
                                     "border-color: none none white none;"
                                     "border-radius: none"
                                     "}")

        self.portLabel = Label(self.portFrame)
        self.portLabel.setText("Port: ")

        self.portLayout = QHBoxLayout(self.portFrame)
        self.portLayout.addWidget(self.portLabel, alignment=Qt.AlignRight | Qt.AlignVCenter)
        self.portLayout.addWidget(self.portField, alignment=Qt.AlignLeft | Qt.AlignVCenter)
        self.portLayout.setContentsMargins(0, 0, 0, 0)

        self.networkingLayout = QHBoxLayout(self.networkingFrame)
        self.networkingLayout.addWidget(self.ipAddressFrame)
        self.networkingLayout.addWidget(self.portFrame)
        self.networkingLayout.setContentsMargins(0, 0, 0, 0)
        self.networkingLayout.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        self.controlsFrame = QFrame(self.configurationFrame)
        self.controlsFrame.setFrameShape(QFrame.NoFrame)
        self.controlsFrame.setFrameShadow(QFrame.Raised)
        self.controlsFrame.setContentsMargins(0, 0, 0, 0)
        self.controlsFrame.setStyleSheet("border: none;")

        self.runBtnsFrame = QFrame(self.controlsFrame)
        self.runBtnsFrame.setFrameShape(QFrame.NoFrame)
        self.runBtnsFrame.setFrameShadow(QFrame.Raised)
        self.runBtnsFrame.setContentsMargins(0, 0, 0, 0)
        self.runBtnsFrame.setStyleSheet("border: none;")

        self.startBtn = PushButton(self.runBtnsFrame)
        self.startBtn.setIcon(QIcon(resource_path("icons/cil-media-play")))

        self.pauseBtn = PushButton(self.runBtnsFrame)
        self.pauseBtn.setIcon(QIcon(resource_path("icons/cil-media-pause")))

        self.runBtnsLayout = QStackedLayout(self.runBtnsFrame)
        self.runBtnsLayout.addWidget(self.startBtn)
        self.runBtnsLayout.addWidget(self.pauseBtn)
        self.runBtnsLayout.setContentsMargins(0, 0, 0, 0)
        self.runBtnsLayout.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.runBtnsLayout.setCurrentIndex(self.START_BUTTON_INDEX)

        self.stopBtnFrame = QFrame(self.controlsFrame)
        self.stopBtnFrame.setFrameShape(QFrame.NoFrame)
        self.stopBtnFrame.setFrameShadow(QFrame.Raised)
        self.stopBtnFrame.setContentsMargins(0, 0, 0, 0)
        self.stopBtnFrame.setStyleSheet("border: none;")

        self.stopBtn = PushButton(self.stopBtnFrame)
        self.stopBtn.setIcon(QIcon(resource_path("icons/cil-media-stop")))

        self.stopBtnLayout = QStackedLayout(self.stopBtnFrame)
        self.stopBtnLayout.addWidget(self.stopBtn)
        self.stopBtnLayout.setContentsMargins(0, 0, 0, 0)
        self.stopBtnLayout.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        self.controlsLayout = QHBoxLayout(self.controlsFrame)
        self.controlsLayout.addWidget(self.runBtnsFrame, alignment=Qt.AlignRight)
        self.controlsLayout.addWidget(self.stopBtnFrame, alignment=Qt.AlignRight)
        self.controlsLayout.setContentsMargins(0, 0, 0, 0)
        self.controlsLayout.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self.configurationLayout = QHBoxLayout(self.configurationFrame)
        self.configurationLayout.addWidget(self.networkingFrame, alignment=Qt.AlignLeft)
        self.configurationLayout.addWidget(self.controlsFrame, alignment=Qt.AlignRight)
        self.configurationLayout.setContentsMargins(10, 10, 10, 10)
        self.configurationLayout.setAlignment(Qt.AlignVCenter)

        self.udpLayout = QVBoxLayout(self.udpFrame)
        self.udpLayout.addWidget(self.measurementsFrame)
        self.udpLayout.addWidget(self.configurationFrame)
        self.udpLayout.setContentsMargins(10, 10, 10, 10)
        self.udpLayout.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        self.contentLayout = QVBoxLayout(self.contentFrame)
        self.contentLayout.addWidget(self.udpFrame, alignment=Qt.AlignTop)
        self.contentLayout.setContentsMargins(0, 0, 0, 0)
        self.contentLayout.setAlignment(Qt.AlignTop)

        self.centralLayout = QHBoxLayout(self.centralFrame)
        self.centralLayout.addWidget(self.contentFrame)
        self.centralLayout.setContentsMargins(0, 0, 0, 0)

        self.uiLayout = QHBoxLayout(self)
        self.uiLayout.addWidget(self.centralFrame)
        self.uiLayout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(self.uiLayout)
        self.setContentsMargins(0, 0, 0, 0)


"""
Widget to create label
"""
class Label(QLabel):
    def __init__(self, parent):
        super().__init__(parent)

        self.initUI()

    def initUI(self):
        font = QFont()
        font.setBold(True)
        font.setPointSize(10)
        self.setFont(font)


class LineEdit(QLineEdit):
    def __init__(self, parent):
        super().__init__(parent)

        self.initUI()

    def initUI(self):
        self.show()


class PushButton(QPushButton):
    def __init__(self, parent):
        super().__init__(parent)

        self.initUI()

    def initUI(self):
        self.setIconSize(QSize(40, 40))

        self.setStyleSheet(u"QPushButton {"
                           "border: none;"
                           "background-color: transparent;"
                           "}"
                           "QPushButton:hover {"
                           "background-color: rgb(85, 170, 255);"
                           "}"
                           "QPushButton:pressed {"
                           "background-color: rgb(85, 170, 255);"
                           "}"
                           "QPushButton:checked {"
                           "background-color: rgb(85, 170, 255);"
                           "}"
                           "QToolTip {"
                           "color:white;"
                           "background-color: black;"
                           "border: black solid 1px;"
                           "}")


"""
Widget to create listbox
"""
class ListBox(QListWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.initUI()

    def initUI(self):
        self.setMinimumSize(200, 50)

        self.setStyleSheet(
            "background-color: rgb(27, 29, 35);"
            "border: 1px solid gray;"
            "border-radius: 5px;"
        )
