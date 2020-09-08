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
        self.centralFrame.setFrameShape(QFrame.NoFrame)
        self.centralFrame.setFrameShadow(QFrame.Raised)
        self.centralFrame.setContentsMargins(0, 0, 0, 0)
        self.centralFrame.setStyleSheet("border: none;")

        self.sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.sizePolicy.setHorizontalStretch(0)
        self.sizePolicy.setVerticalStretch(0)
        self.sizePolicy.setHeightForWidth(self.centralFrame.sizePolicy().hasHeightForWidth())

        self.uiFrame = QFrame(self.centralFrame)
        self.uiFrame.setSizePolicy(self.sizePolicy)
        self.uiFrame.setFrameShape(QFrame.NoFrame)
        self.uiFrame.setFrameShadow(QFrame.Raised)
        self.uiFrame.setMinimumSize(QSize(70, 0))
        self.uiFrame.setMaximumSize(QSize(70, 16777215))
        self.uiFrame.setLayoutDirection(Qt.LeftToRight)
        self.uiFrame.setStyleSheet(u"background-color: rgb(27, 29, 35);")

        self.logoFrame = QFrame(self.uiFrame)
        self.logoFrame.setFrameShape(QFrame.NoFrame)
        self.logoFrame.setFrameShadow(QFrame.Raised)
        self.logoFrame.setContentsMargins(0, 0, 0, 0)
        self.logoFrame.setStyleSheet("border: none;")

        self.logoWidget = Logo(self.logoFrame)

        self.logoLayout = QHBoxLayout(self.logoFrame)
        self.logoLayout.setAlignment(Qt.AlignCenter)
        self.logoLayout.addWidget(self.logoWidget)

        self.btnsFrame = QFrame(self.uiFrame)
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

        self.uiLayout = QVBoxLayout(self.uiFrame)
        self.uiLayout.addWidget(self.logoFrame, stretch=.5, alignment=Qt.AlignTop)
        self.uiLayout.addWidget(self.btnsFrame, stretch=4, alignment=Qt.AlignTop)
        self.uiLayout.setContentsMargins(0, 0, 0, 0)

        self.centralLayout = QHBoxLayout(self.centralFrame)
        self.centralLayout.addWidget(self.uiFrame)
        self.centralLayout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(self.centralLayout)


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
