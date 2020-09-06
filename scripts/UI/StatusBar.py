from PyQt5.QtWidgets import QFrame, QHBoxLayout, QLabel, QWidget
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
        self.centralFrame.setMinimumSize(QSize(0, 25))
        self.centralFrame.setMaximumSize(QSize(16777215, 25))

        self.centralFrame.setStyleSheet(u"background-color: rgb(27, 29, 35);")
        self.centralFrame.setFrameShape(QFrame.NoFrame)
        self.centralFrame.setFrameShadow(QFrame.Raised)

        self.centralLayout = QHBoxLayout(self.centralFrame)
        self.centralLayout.setSpacing(0)
        self.centralLayout.setContentsMargins(0, 0, 0, 0)

        self.labelsFrame = QFrame(self.centralFrame)
        self.labelsFrame.setFrameShape(QFrame.NoFrame)
        self.labelsFrame.setFrameShadow(QFrame.Raised)

        self.developerLabel = Label(self.labelsFrame)
        self.developerLabel.setText("Ashwin Sakhare")

        self.instituteLabel = Label(self.labelsFrame)
        self.instituteLabel.setText("Stevens Neuroimaging and Informatics Institute")

        self.universityLabel = Label(self.labelsFrame)
        self.universityLabel.setText("University of Southern California")

        self.labelsLayout = QHBoxLayout(self.labelsFrame)
        self.labelsLayout.setSpacing(50)
        self.labelsLayout.setContentsMargins(10, 0, 0, 0)
        self.labelsLayout.addWidget(self.developerLabel)
        self.labelsLayout.addWidget(self.instituteLabel)
        self.labelsLayout.addWidget(self.universityLabel)
        self.labelsLayout.setAlignment(Qt.AlignLeft)

        self.versionFrame = QFrame(self.centralFrame)
        self.versionFrame.setFrameShape(QFrame.NoFrame)
        self.versionFrame.setFrameShadow(QFrame.Raised)

        self.versionLabel = Label(self.labelsFrame)
        self.versionLabel.setText("v1.0.0 alpha")

        self.versionLayout = QHBoxLayout(self.versionFrame)
        self.versionLayout.addWidget(self.versionLabel)
        self.versionLayout.setAlignment(Qt.AlignRight)
        self.versionLayout.setContentsMargins(0, 0, 20, 0)

        self.gripFrame = QFrame(self.centralFrame)
        self.gripFrame.setMaximumSize(QSize(20, 20))

        path = resource_path('icons/cil-size-grip.png')
        self.gripFrame.setStyleSheet("background-image: url(" + str(path) + "); \n"
                                     "background-position: center; \n"
                                     "background-repeat: no repeat")

        self.gripFrame.setFrameShape(QFrame.NoFrame)
        self.gripFrame.setFrameShadow(QFrame.Raised)

        self.centralLayout.addWidget(self.labelsFrame)
        self.centralLayout.addWidget(self.versionFrame)
        self.centralLayout.addWidget(self.gripFrame)

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.centralFrame)
        self.setLayout(layout)


class Label(QLabel):
    def __init__(self, parent):
        super().__init__(parent)

        self.initUI()

    def initUI(self):
        font = QFont()
        font.setFamily(u"Segoe UI")

        self.setFont(font)
        self.setStyleSheet(u"color: rgb(98, 103, 111);")