from PyQt5.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout, QWidget, QLabel, QPushButton, QListWidget
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QIcon

from scripts.Helper.Resources import *

class MeasurementsPanel(QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.initUI()

    def initUI(self):
        self.centralFrame = QFrame(self)
        self.centralFrame.setFrameShape(QFrame.NoFrame)
        self.centralFrame.setFrameShadow(QFrame.Raised)
        self.centralFrame.setContentsMargins(0, 0, 0, 0)
        self.centralFrame.setStyleSheet("border: none;")

        self.displayFrame = QFrame(self.centralFrame)
        self.displayFrame.setFrameShape(QFrame.NoFrame)
        self.displayFrame.setFrameShadow(QFrame.Raised)
        self.displayFrame.setContentsMargins(0, 0, 0, 0)
        self.displayFrame.setStyleSheet("border: none;")

        self.displayDataFrame = QFrame(self.displayFrame)
        self.displayDataFrame.setFrameShape(QFrame.NoFrame)
        self.displayDataFrame.setFrameShadow(QFrame.Raised)
        self.displayDataFrame.setContentsMargins(0, 0, 0, 0)
        self.displayDataFrame.setStyleSheet("border: none;")

        self.activeMeasurements = ListBox(self.displayDataFrame)
        self.activeMeasurements.setStyleSheet("background: rgb(15,15,15);"
                                              "border: 1px solid gray;"
                                              "border-radius: 5px;")

        self.displayDataLayout = QVBoxLayout(self.displayDataFrame)
        self.displayDataLayout.addWidget(self.activeMeasurements)
        self.displayDataLayout.setContentsMargins(0, 0, 0, 0)
        self.displayDataLayout.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        self.displayToolsFrame = QFrame(self.displayFrame)
        self.displayToolsFrame.setFrameShape(QFrame.NoFrame)
        self.displayToolsFrame.setFrameShadow(QFrame.Raised)
        self.displayToolsFrame.setContentsMargins(0, 0, 0, 0)
        self.displayToolsFrame.setStyleSheet("border: none;")

        self.displayLabelFrame = QFrame(self.displayToolsFrame)
        self.displayLabelFrame.setFrameShape(QFrame.NoFrame)
        self.displayLabelFrame.setFrameShadow(QFrame.Raised)
        self.displayLabelFrame.setContentsMargins(0, 0, 0, 0)
        self.displayLabelFrame.setStyleSheet("border: none;")

        self.displayLabel = Label(self.displayLabelFrame)
        self.displayLabel.setText("Active Measurements")

        self.displayLabelLayout = QHBoxLayout(self.displayLabelFrame)
        self.displayLabelLayout.addWidget(self.displayLabel, alignment=Qt.AlignLeft)
        self.displayLabelLayout.setContentsMargins(0, 0, 0, 0)
        self.displayLabelLayout.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)

        self.displayBtnsFrame = QFrame(self.displayToolsFrame)
        self.displayBtnsFrame.setFrameShape(QFrame.NoFrame)
        self.displayBtnsFrame.setFrameShadow(QFrame.Raised)
        self.displayBtnsFrame.setContentsMargins(0, 0, 0, 0)
        self.displayBtnsFrame.setStyleSheet("border: none;")

        self.addBtn = PushButton(self.displayBtnsFrame)
        self.addBtn.setIcon(QIcon(resource_path("icons/cil-plus")))
        self.addBtn.setIconSize(QSize(20, 20))
        self.removeBtn = PushButton(self.displayBtnsFrame)
        self.removeBtn.setIcon(QIcon(resource_path("icons/cil-minus")))
        self.removeBtn.setIconSize(QSize(20, 20))

        self.displayBtnsLayout = QHBoxLayout(self.displayBtnsFrame)
        self.displayBtnsLayout.addWidget(self.addBtn, alignment=Qt.AlignRight)
        self.displayBtnsLayout.addWidget(self.removeBtn, alignment=Qt.AlignRight)
        self.displayBtnsLayout.setContentsMargins(0, 0, 0, 0)
        self.displayBtnsLayout.setAlignment(Qt.AlignVCenter | Qt.AlignRight)

        self.displayToolsLayout = QHBoxLayout(self.displayToolsFrame)
        self.displayToolsLayout.addWidget(self.displayLabelFrame, alignment=Qt.AlignLeft)
        self.displayToolsLayout.addWidget(self.displayBtnsFrame, alignment=Qt.AlignRight)
        self.displayToolsLayout.setContentsMargins(0, 0, 0, 0)
        self.displayToolsLayout.setAlignment(Qt.AlignVCenter)

        self.displayLayout = QVBoxLayout(self.displayFrame)
        self.displayLayout.addWidget(self.displayToolsFrame)
        self.displayLayout.addWidget(self.displayDataFrame)
        self.displayLayout.setContentsMargins(0, 0, 0, 0)

        self.centralLayout = QHBoxLayout(self.centralFrame)
        self.centralLayout.addWidget(self.displayFrame)
        self.centralLayout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(self.centralLayout)


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

