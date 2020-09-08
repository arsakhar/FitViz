from PyQt5.QtWidgets import QFrame, QSizePolicy, QHBoxLayout, QPushButton, QWidget, QVBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize, Qt
from scripts.UI.Logo import Logo

from scripts.Helper.Resources import *

# creates a side menu located on left side of main window
class SideMenu(QWidget):
    SCAN_BUTTON = 0
    VIEW_BUTTON = 1
    WRITE_BUTTON = 2

    def __init__(self, parent):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.centralFrame = QFrame(self)

        self.sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.sizePolicy.setHorizontalStretch(0)
        self.sizePolicy.setVerticalStretch(0)
        self.sizePolicy.setHeightForWidth(self.centralFrame.sizePolicy().hasHeightForWidth())

        self.centralFrame.setSizePolicy(self.sizePolicy)
        self.centralFrame.setFrameShape(QFrame.NoFrame)
        self.centralFrame.setFrameShadow(QFrame.Raised)
        self.centralFrame.setMinimumSize(QSize(70, 0))
        self.centralFrame.setMaximumSize(QSize(70, 16777215))
        self.centralFrame.setLayoutDirection(Qt.LeftToRight)
        self.centralFrame.setStyleSheet(u"background-color: rgb(27, 29, 35);")

        self.logoFrame = QFrame(self.centralFrame)
        self.logoFrame.setFrameShape(QFrame.NoFrame)
        self.logoFrame.setFrameShadow(QFrame.Raised)
        self.logoFrame.setContentsMargins(0, 0, 0, 0)
        self.logoFrame.setStyleSheet("border: none;")

        self.logoWidget = Logo(self.logoFrame)

        self.logoLayout = QHBoxLayout(self.logoFrame)
        self.logoLayout.setAlignment(Qt.AlignCenter)
        self.logoLayout.addWidget(self.logoWidget)

        self.btnsFrame = QFrame(self.centralFrame)
        self.btnsFrame.setFrameShape(QFrame.NoFrame)
        self.btnsFrame.setFrameShadow(QFrame.Raised)
        self.btnsFrame.setContentsMargins(0, 0, 0, 0)
        self.btnsFrame.setStyleSheet("border: none;")

        self.networkBtn = MenuButton(self.btnsFrame)
        self.networkBtn.setIcon(QIcon(resource_path("icons/cil-wifi-signal-1")))
        self.networkBtn.setToolTip("Scan for Devices")

        self.viewBtn = MenuButton(self.btnsFrame)
        self.viewBtn.setIcon(QIcon(resource_path("icons/cil-speedometer")))
        self.viewBtn.setToolTip("View Device Measurements")

        self.writeBtn = MenuButton(self.btnsFrame)
        self.writeBtn.setIcon(QIcon(resource_path("icons/cil-transfer")))
        self.writeBtn.setToolTip("Output Device Measurements")

        self.btnsLayout = QVBoxLayout(self.btnsFrame)
        self.btnsLayout.addWidget(self.networkBtn)
        self.btnsLayout.addWidget(self.viewBtn)
        self.btnsLayout.addWidget(self.writeBtn)
        self.btnsLayout.setContentsMargins(0, 0, 0, 0)

        self.centralLayout = QVBoxLayout(self.centralFrame)
        self.centralLayout.addWidget(self.logoFrame, stretch=.5, alignment=Qt.AlignTop)
        self.centralLayout.addWidget(self.btnsFrame, stretch=4, alignment=Qt.AlignTop)
        self.centralLayout.setContentsMargins(0, 0, 0, 0)

        self.uiLayout = QHBoxLayout(self)
        self.uiLayout.addWidget(self.centralFrame)
        self.uiLayout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(self.uiLayout)


class MenuButton(QPushButton):
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
