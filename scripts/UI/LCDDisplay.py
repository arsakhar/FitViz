from PyQt5.QtWidgets import QLCDNumber, QSizePolicy,  QLabel
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QFont


"""
Widget to create LCD number
"""
class LCDDisplay(QLCDNumber):
    def __init__(self, parent):
        super().__init__(parent)

        self.initUI()

    def initUI(self):
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setMinimumSize(QSize(150, 150))
        self.setMaximumSize(QSize(200, 200))
        self.setBaseSize(QSize(175, 175))

        self.setStyleSheet("QLCDNumber { color: rgb(0, 255, 0) }")

        self.clear()


    def clear(self):
        self.setDigitCount(3)
        self.display('0')

"""
Widget to create LCD number
"""
class LCDDisplayUnits(QLabel):
    def __init__(self, parent):
        super().__init__(parent)

        self.initUI()

    def initUI(self):
        font = QFont()
        font.setFamily(u"Segoe UI")
        font.setPointSize(50)
        self.setFont(font)

        self.setStyleSheet("color: rgb(0, 255, 0)")

        self.clear()

    def clear(self):
        self.setText('')
