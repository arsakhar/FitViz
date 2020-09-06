from PyQt5.QtWidgets import QApplication
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import QPalette


"""
UI Application
"""
class Application(QApplication):
    def __init__(self, sys):
        super().__init__(sys.argv)

        self.initUI()

    def initUI(self):
        self.setStyle('fusion')

        palette = QPalette()
        palette.setColor(palette.Window, QtGui.QColor(52, 59, 72))
        palette.setColor(palette.WindowText, QtCore.Qt.white)
        palette.setColor(palette.Base, QtGui.QColor(15, 15, 15))
        palette.setColor(palette.AlternateBase, QtGui.QColor(52, 59, 72))
        palette.setColor(palette.ToolTipBase, QtCore.Qt.white)
        palette.setColor(palette.ToolTipText, QtCore.Qt.white)
        palette.setColor(palette.Text, QtCore.Qt.white)
        palette.setColor(palette.Button, QtGui.QColor(52, 59, 72))
        palette.setColor(palette.ButtonText, QtCore.Qt.white)
        palette.setColor(palette.BrightText, QtCore.Qt.red)
        palette.setColor(palette.Highlight, QtGui.QColor(85, 170, 255).lighter())
        palette.setColor(palette.HighlightedText, QtCore.Qt.black)

        self.setPalette(palette)
