from PyQt5.QtWidgets import QWidget, QFileSystemModel, QTreeView
from PyQt5.QtCore import pyqtSignal
import os


"""
Widget used as a container for the file system and tree view.
"""
class FileSystem(QWidget):
    def __init__(self, mainWindow):
        super().__init__(mainWindow)
        self.mainWindow = mainWindow

        self.model = FileSystemModel(self)
        self.tree = TreeView(self)

        self.initUI()

    def initUI(self):
        self.setWindowTitle('fileSystem')

        self.tree.setModel(self.model)

        self.tree.resize(self.frameGeometry().width(), self.frameGeometry().height())
        self.tree.adjustColumnWidths()

        self.setContentsMargins(0, 0, 0, 0)


"""
Creates a QFileSystemModel. This is along with QTreeView creates a file system that can be browsed within the widget.
"""
class FileSystemModel(QFileSystemModel):
    def __init__(self, parent):
        super().__init__(parent)

        self.setNameFilterDisables(False)


"""
Creates a QTreeView. This is used to display the file system tree.
"""
class TreeView(QTreeView):
    def __init__(self, parent):
        super().__init__(parent)

        self.setAnimated(False)
        self.setIndentation(20)
        self.setSortingEnabled(True)

        self.initUI()

    def initUI(self):
        self.setContentsMargins(0, 0, 0, 0)
        self.setStyleSheet()

    def adjustColumnWidths(self):
        self.setColumnWidth(0,self.frameGeometry().width() * .5)
        self.setColumnWidth(1,self.frameGeometry().width() * .1)
        self.setColumnWidth(2,self.frameGeometry().width() * .2)
        self.setColumnWidth(3,self.frameGeometry().width() * .2 - 5)

    def setStyleSheet(self):
        super().setStyleSheet("QTreeView::item{\n"
                              "	border-color: rgb(44, 49, 60);\n"
                              "	padding-left: 5px;\n"
                              "	padding-right: 5px;\n"
                              "	gridline-color: rgb(44, 49, 60);\n"
                              "}\n"
                              "QTreeView::item:selected{\n"
                              "	background-color: rgb(85, 170, 255);\n"
                              "}\n"
                              "QTreeView::branch:selected{\n"
                              "	background-color: rgb(85, 170, 255);\n"
                              "}\n"
                              "QHeaderView::section{\n"
                              "	Background-color: rgb(39, 44, 54);\n"
                              "	max-width: 30px;\n"
                              "	border: 1px solid rgb(44, 49, 60);\n"
                              "	border-style: none;\n"
                              "    border-bottom: 1px solid rgb(44, 49, 60);\n"
                              "    border-right: 1px solid rgb(44, 49, 60);\n"
                              "}\n"
                              ""
                              "QTreeView::horizontalHeader {	\n"
                              "	background-color: rgb(81, 255, 0);\n"
                              "}\n"
                              "QHeaderView::section:horizontal\n"
                              "{\n"
                              "    border: 1px solid rgb(32, 34, 42);\n"
                              "	background-color: rgb(27, 29, 35);\n"
                              "	padding: 3px;\n"
                              "}\n"
                              "QHeaderView::section:vertical\n"
                              "{\n"
                              "    border: 1px solid rgb(44, 49, 60);\n"
                              "}\n"
                              "")
