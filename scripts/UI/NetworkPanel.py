from PyQt5.QtWidgets import QFrame, QVBoxLayout, QWidget, QLabel, QHBoxLayout, QListWidget, QPushButton, QTextEdit
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QIcon, QPixmap
from PyQt5 import QtCore

from scripts.Helper.Resources import *

"""
Widget that displays file panel
"""
class NetworkPanel(QWidget):
    def __init__(self, parent):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.centralFrame = QFrame(self)
        self.centralFrame.setFrameShape(QFrame.NoFrame)
        self.centralFrame.setFrameShadow(QFrame.Raised)
        self.centralFrame.setContentsMargins(0, 0, 0, 0)
        self.centralFrame.setStyleSheet("background: black;"
                                        "border: 1px solid gray;"
                                        "border-radius: 5px;")

        self.contentFrame = QFrame(self.centralFrame)
        self.contentFrame.setFrameShape(QFrame.NoFrame)
        self.contentFrame.setFrameShadow(QFrame.Raised)
        self.contentFrame.setContentsMargins(10, 10, 10, 10)
        self.contentFrame.setStyleSheet("border: none;")

        self.networkFrame = QFrame(self.contentFrame)
        self.networkFrame.setFrameShape(QFrame.NoFrame)
        self.networkFrame.setFrameShadow(QFrame.Raised)
        self.networkFrame.setContentsMargins(0, 0, 0, 0)
        self.networkFrame.setStyleSheet("border: none;")

        self.controlFrame = QFrame(self.networkFrame)
        self.controlFrame.setFrameShape(QFrame.NoFrame)
        self.controlFrame.setFrameShadow(QFrame.Raised)
        self.controlFrame.setContentsMargins(0, 0, 0, 0)
        self.controlFrame.setStyleSheet("border: none;")

        self.controlLabelFrame = QFrame(self.controlFrame)
        self.controlLabelFrame.setFrameShape(QFrame.NoFrame)
        self.controlLabelFrame.setFrameShadow(QFrame.Raised)
        self.controlLabelFrame.setContentsMargins(0, 0, 0, 0)
        self.controlLabelFrame.setStyleSheet("border: none;")

        self.controlLabel = Label(self.controlLabelFrame)
        self.controlLabel.setText("Network Controls")

        self.controlLabelLayout = QHBoxLayout(self.controlLabelFrame)
        self.controlLabelLayout.addWidget(self.controlLabel)
        self.controlLabelLayout.setContentsMargins(0, 0, 0, 0)
        self.controlLabelLayout.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        self.controlBtnsFrame = QFrame(self.controlFrame)
        self.controlBtnsFrame.setFrameShape(QFrame.NoFrame)
        self.controlBtnsFrame.setFrameShadow(QFrame.Raised)
        self.controlBtnsFrame.setContentsMargins(0, 0, 0, 0)
        self.controlBtnsFrame.setStyleSheet(
            "background-color: rgb(27, 29, 35);"
            "border: 1px solid gray;"
            "border-radius: 5px;"
        )

        self.connectBtn = PushButton(self.controlBtnsFrame)
        self.connectBtn.setIcon(QIcon(resource_path("icons/cil-media-play")))
        self.connectBtn.setIconSize(QSize(50, 50))
        self.connectBtn.setToolTip("Scan for ANT+ devices")

        self.disconnectBtn = PushButton(self.controlBtnsFrame)
        self.disconnectBtn.setIcon(QIcon(resource_path("icons/cil-media-stop")))
        self.disconnectBtn.setIconSize(QSize(50, 50))
        self.disconnectBtn.setToolTip("Stop ANT+ connection")

        self.resetBtn = PushButton(self.controlBtnsFrame)
        self.resetBtn.setIcon(QIcon(resource_path("icons/cil-reload")))
        self.resetBtn.setIconSize(QSize(50, 50))
        self.resetBtn.setToolTip("Reset ANT+ session")

        self.controlBtnsLayout = QHBoxLayout(self.controlBtnsFrame)
        self.controlBtnsLayout.addWidget(self.connectBtn, alignment=Qt.AlignRight)
        self.controlBtnsLayout.addWidget(self.disconnectBtn, alignment=Qt.AlignRight)
        self.controlBtnsLayout.addWidget(self.resetBtn, alignment=Qt.AlignRight)
        self.controlBtnsLayout.setContentsMargins(5, 0, 0, 0)
        self.controlBtnsLayout.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        self.controlLayout = QVBoxLayout(self.controlFrame)
        self.controlLayout.addWidget(self.controlLabelFrame)
        self.controlLayout.addWidget(self.controlBtnsFrame)
        self.controlLayout.setContentsMargins(0, 0, 0, 0)

        self.devicesFrame = QFrame(self.contentFrame)
        self.devicesFrame.setFrameShape(QFrame.NoFrame)
        self.devicesFrame.setFrameShadow(QFrame.Raised)
        self.devicesFrame.setContentsMargins(0, 0, 0, 0)
        self.devicesFrame.setStyleSheet("border: none;")

        self.devicesListBox = ListBox(self.devicesFrame)
        self.devicesListBox.setStyleSheet(
            "background-color: rgb(27, 29, 35);"
            "border: 1px solid gray;"
            "border-radius: 5px;"
        )

        self.devicesLabelFrame = QFrame(self.devicesFrame)
        self.devicesLabelFrame.setFrameShape(QFrame.NoFrame)
        self.devicesLabelFrame.setFrameShadow(QFrame.Raised)
        self.devicesLabelFrame.setContentsMargins(0, 0, 0, 0)
        self.devicesLabelFrame.setStyleSheet("border: none;")

        self.devicesLabel = Label(self.devicesLabelFrame)
        self.devicesLabel.setText("Broadcasting Devices")
        self.devicesLabel.setStyleSheet("border: none;")

        self.devicesLabelLayout = QHBoxLayout(self.devicesLabelFrame)
        self.devicesLabelLayout.addWidget(self.devicesLabel, alignment=Qt.AlignLeft)
        self.devicesLabelLayout.setContentsMargins(0, 0, 0, 0)
        self.devicesLabelLayout.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)

        self.devicesLayout = QVBoxLayout(self.devicesFrame)
        self.devicesLayout.addWidget(self.devicesLabelFrame)
        self.devicesLayout.addWidget(self.devicesListBox)
        self.devicesLayout.setContentsMargins(0, 0, 0, 0)
        self.devicesLayout.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        self.sessionFrame = QFrame(self.contentFrame)
        self.sessionFrame.setFrameShape(QFrame.NoFrame)
        self.sessionFrame.setFrameShadow(QFrame.Raised)
        self.sessionFrame.setContentsMargins(0, 0, 0, 0)
        self.sessionFrame.setStyleSheet("border: none;")

        self.sessionLabelFrame = QFrame(self.sessionFrame)
        self.sessionLabelFrame.setFrameShape(QFrame.NoFrame)
        self.sessionLabelFrame.setFrameShadow(QFrame.Raised)
        self.sessionLabelFrame.setContentsMargins(0, 0, 0, 0)
        self.sessionLabelFrame.setStyleSheet("border: none;")

        self.sessionLabel = Label(self.sessionLabelFrame)
        self.sessionLabel.setText("Network Statistics")
        self.sessionLabel.setStyleSheet("border: none;")

        self.sessionLabelLayout = QHBoxLayout(self.sessionLabelFrame)
        self.sessionLabelLayout.addWidget(self.sessionLabel, alignment=Qt.AlignLeft)
        self.sessionLabelLayout.setContentsMargins(0, 0, 0, 0)
        self.sessionLabelLayout.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)

        self.sessionTextFrame = QFrame(self.sessionFrame)
        self.sessionTextFrame.setFrameShape(QFrame.NoFrame)
        self.sessionTextFrame.setFrameShadow(QFrame.Raised)
        self.sessionTextFrame.setContentsMargins(0, 0, 0, 0)
        self.sessionTextFrame.setStyleSheet(
            "background-color: rgb(27, 29, 35);"
            "border: 1px solid gray;"
            "border-radius: 5px;"
        )

        self.sessionText = TextEdit(self.sessionTextFrame)

        self.sessionTextLayout = QHBoxLayout(self.sessionTextFrame)
        self.sessionTextLayout.addWidget(self.sessionText)
        self.sessionTextLayout.setContentsMargins(0, 0, 0, 0)
        self.sessionTextLayout.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        self.sessionLayout = QVBoxLayout(self.sessionFrame)
        self.sessionLayout.addWidget(self.sessionLabelFrame)
        self.sessionLayout.addWidget(self.sessionTextFrame)
        self.sessionLayout.setContentsMargins(0, 0, 0, 0)
        self.sessionLayout.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        self.networkLayout = QVBoxLayout(self.networkFrame)
        self.networkLayout.addWidget(self.controlFrame)
        self.networkLayout.addWidget(self.devicesFrame)
        self.networkLayout.addWidget(self.sessionFrame)
        self.networkLayout.setContentsMargins(0, 0, 0, 0)

        self.infoFrame = QFrame(self.contentFrame)
        self.infoFrame.setFrameShape(QFrame.NoFrame)
        self.infoFrame.setFrameShadow(QFrame.Raised)
        self.infoFrame.setContentsMargins(0, 0, 0, 0)
        self.infoFrame.setStyleSheet("border: none;")

        self.graphicsFrame = QFrame(self.infoFrame)
        self.graphicsFrame.setFrameShape(QFrame.NoFrame)
        self.graphicsFrame.setFrameShadow(QFrame.Raised)
        self.graphicsFrame.setContentsMargins(0, 0, 0, 0)
        self.graphicsFrame.setStyleSheet("border: none;")

        self.fitnessGraphics = FitnessGraphics(self.graphicsFrame)

        self.graphicsLayout = QVBoxLayout(self.graphicsFrame)
        self.graphicsLayout.addWidget(self.fitnessGraphics)
        self.graphicsLayout.setContentsMargins(0, 0, 0, 0)

        self.infoLayout = QVBoxLayout(self.infoFrame)
        self.infoLayout.addWidget(self.graphicsFrame)
        self.infoLayout.setContentsMargins(0, 0, 0, 0)
        self.infoLayout.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        self.contentLayout = QHBoxLayout(self.contentFrame)
        self.contentLayout.addWidget(self.networkFrame, stretch=1)
        self.contentLayout.addWidget(self.infoFrame, stretch=1)
        self.contentLayout.setContentsMargins(0, 0, 0, 0)

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


class TextEdit(QTextEdit):
    def __init__(self, parent):
        super().__init__(parent)

        self.initUI()

    def initUI(self):
        font = self.font()
        font.setPointSize(10)
        self.setFont(font)

        self.setReadOnly(True)

        self.setStyleSheet("border: none;")


class FitnessGraphics(QLabel):
    def __init__(self, parent):
        super().__init__(parent)

        self.initUI()

    def initUI(self):
        self.pixmap = QPixmap(resource_path('icons/fitness-icon.png'))
        self.pixmap = self.pixmap.scaled(200, 200, QtCore.Qt.KeepAspectRatio)
        self.setPixmap(self.pixmap)
