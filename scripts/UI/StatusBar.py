from PyQt5.QtWidgets import QFrame, QHBoxLayout, QLabel, QWidget, QSizeGrip
from PyQt5.QtGui import QFont, QPalette, QBrush, QPixmap
from PyQt5.QtCore import QSize, Qt

from scripts.Helper.Resources import *

"""
Creates a status bar for main window
"""
class StatusBar(QWidget):
    def __init__(self, parent):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.centralFrame = QFrame(self)
        self.centralFrame.setFrameShape(QFrame.NoFrame)
        self.centralFrame.setFrameShadow(QFrame.Raised)
        self.centralFrame.setContentsMargins(0, 0, 0, 0)
        self.centralFrame.setStyleSheet("border: none;")

        self.uiFrame = QFrame(self.centralFrame)
        self.uiFrame.setFrameShape(QFrame.NoFrame)
        self.uiFrame.setFrameShadow(QFrame.Raised)
        self.uiFrame.setMinimumSize(QSize(0, 25))
        self.uiFrame.setMaximumSize(QSize(16777215, 25))
        self.uiFrame.setContentsMargins(0, 0, 0, 0)
        self.uiFrame.setStyleSheet(u"background-color: rgb(27, 29, 35);")

        self.labelsFrame = QFrame(self.uiFrame)
        self.labelsFrame.setFrameShape(QFrame.NoFrame)
        self.labelsFrame.setFrameShadow(QFrame.Raised)
        self.labelsFrame.setContentsMargins(0, 0, 0, 0)
        self.labelsFrame.setStyleSheet("border: none;")

        self.developerLabel = Label(self.labelsFrame)
        self.developerLabel.setText("Ashwin Sakhare")

        self.instituteLabel = Label(self.labelsFrame)
        self.instituteLabel.setText("Stevens Neuroimaging and Informatics Institute")

        self.universityLabel = Label(self.labelsFrame)
        self.universityLabel.setText("University of Southern California")

        self.labelsLayout = QHBoxLayout(self.labelsFrame)
        self.labelsLayout.addWidget(self.developerLabel)
        self.labelsLayout.addWidget(self.instituteLabel)
        self.labelsLayout.addWidget(self.universityLabel)
        self.labelsLayout.setSpacing(50)
        self.labelsLayout.setContentsMargins(10, 0, 0, 0)

        self.labelsLayout.setAlignment(Qt.AlignLeft)

        self.versionFrame = QFrame(self.uiFrame)
        self.versionFrame.setFrameShape(QFrame.NoFrame)
        self.versionFrame.setFrameShadow(QFrame.Raised)
        self.versionFrame.setContentsMargins(0, 0, 0, 0)
        self.versionFrame.setStyleSheet("border: none;")

        self.versionLabel = Label(self.labelsFrame)
        self.versionLabel.setText("v1.0.0 alpha")

        self.versionLayout = QHBoxLayout(self.versionFrame)
        self.versionLayout.addWidget(self.versionLabel)
        self.versionLayout.setAlignment(Qt.AlignRight)
        self.versionLayout.setContentsMargins(0, 0, 20, 0)

        self.gripFrame = QFrame(self.uiFrame)
        self.gripFrame.setFrameShape(QFrame.NoFrame)
        self.gripFrame.setFrameShadow(QFrame.Raised)
        self.gripFrame.setMaximumSize(QSize(20, 20))
        self.gripFrame.setContentsMargins(0, 0, 0, 0)
        self.gripFrame.setStyleSheet("border: none;")

        path = resource_path('icons/cil-size-grip.png')
        self.gripFrame.setStyleSheet("background-image: url(" + str(path) + "); \n"
                                     "background-position: center; \n"
                                     "background-repeat: no repeat")


        self.ui_sizeGrip = QSizeGrip(self.gripFrame)
        self.ui_sizeGrip.setStyleSheet("width: 20px; height: 20px; margin 0px; padding: 0px;")

        self.uiLayout = QHBoxLayout(self.uiFrame)
        self.uiLayout.addWidget(self.labelsFrame)
        self.uiLayout.addWidget(self.versionFrame)
        self.uiLayout.addWidget(self.gripFrame)
        self.uiLayout.setSpacing(0)
        self.uiLayout.setContentsMargins(0, 0, 0, 0)

        self.centralLayout = QHBoxLayout(self.centralFrame)
        self.centralLayout.addWidget(self.uiFrame)
        self.centralLayout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(self.centralLayout)


class Label(QLabel):
    def __init__(self, parent):
        super().__init__(parent)

        self.initUI()

    def initUI(self):
        font = QFont()
        font.setFamily(u"Segoe UI")

        self.setFont(font)
        self.setStyleSheet(u"color: rgb(98, 103, 111);")