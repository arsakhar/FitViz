from PyQt5.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout, QWidget, QLabel
from PyQt5.QtWidgets import QLineEdit, QPushButton, QListWidget, QTabWidget, QTextEdit
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QFont

from scripts.UI.ANTPanel import ANTPanel
from scripts.UI.UdpPanel import UdpPanel
from scripts.UI.CSVPanel import CSVPanel


"""
Widget that displays file panel
"""
class WritePanel(QWidget):
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
        self.contentFrame.setContentsMargins(0, 0, 0, 0)
        self.contentFrame.setStyleSheet("border: none;")

        self.antPanelFrame = QFrame(self.contentFrame)
        self.antPanelFrame.setFrameShape(QFrame.NoFrame)
        self.antPanelFrame.setFrameShadow(QFrame.Raised)
        self.antPanelFrame.setContentsMargins(0, 0, 0, 0)
        self.antPanelFrame.setStyleSheet("border: none;")

        self.antPanel = ANTPanel(self.antPanelFrame,
                                 alignment=ANTPanel.ALIGN_GRID,
                                 devicesStyle=ANTPanel.LIST_BOX)

        self.devices = self.antPanel.devices
        self.profiles = self.antPanel.profiles
        self.dataPages = self.antPanel.dataPages
        self.pageMeasurements = self.antPanel.pageMeasurements

        self.antPanelLayout = QHBoxLayout(self.antPanelFrame)
        self.antPanelLayout.addWidget(self.antPanel)
        self.antPanelLayout.setContentsMargins(0, 0, 0, 0)

        self.writerFrame = QFrame(self.contentFrame)
        self.writerFrame.setFrameShape(QFrame.NoFrame)
        self.writerFrame.setFrameShadow(QFrame.Raised)
        self.writerFrame.setContentsMargins(10, 10, 10, 10)
        self.writerFrame.setStyleSheet("border: none;")

        self.writerPanelFrame = QFrame(self.writerFrame)
        self.writerPanelFrame.setFrameShape(QFrame.NoFrame)
        self.writerPanelFrame.setFrameShadow(QFrame.Raised)
        self.writerPanelFrame.setContentsMargins(0, 0, 0, 0)
        self.writerPanelFrame.setStyleSheet("border: none;")

        self.udpPanel = UdpPanel(self.writerFrame)
        self.csvPanel = CSVPanel(self.writerFrame)

        self.writerPanel = QTabWidget(self.writerFrame)
        self.writerPanel.addTab(self.udpPanel, 'UDP')
        self.writerPanel.addTab(self.csvPanel, 'CSV')
        self.writerPanel.setContentsMargins(10, 10, 10, 10)
        self.writerPanel.setStyleSheet("QTabBar::tab { "
                                          "height: 30px; "
                                          "width: 100px; "
                                          "background-color: rgb(39, 44, 54);"
                                          "font: 14px;"
                                          "border-radius: 1px;"
                                          "}"
                                          "QTabBar::tab:selected { "
                                          "border: 1px solid gray;"
                                          "}"
                                          "QTabBar::tab:hover{"
                                          "background-color: rgb(85, 170, 255);"
                                          "}"
                                          "QTabWidget::pane {"
                                          "border: 1px solid gray;"
                                          "}")

        self.writerPanelLayout = QHBoxLayout(self.writerPanelFrame)
        self.writerPanelLayout.addWidget(self.writerPanel)
        self.writerPanelLayout.setContentsMargins(0, 0, 0, 0)

        self.logPanelFrame = QFrame(self.writerFrame)
        self.logPanelFrame.setFrameShape(QFrame.NoFrame)
        self.logPanelFrame.setFrameShadow(QFrame.Raised)
        self.logPanelFrame.setContentsMargins(0, 0, 0, 0)
        self.logPanelFrame.setStyleSheet("background: rgb(15,15,15);"
                                         "border: 1px solid gray;"
                                         )

        self.logPanel = QTextEdit(self.logPanelFrame)
        self.logPanel.setStyleSheet("border: none;")
        self.logPanel.setReadOnly(True)

        self.logPanelLayout = QHBoxLayout(self.logPanelFrame)
        self.logPanelLayout.addWidget(self.logPanel)
        self.logPanelLayout.setContentsMargins(0, 0, 0, 0)

        self.writerLayout = QVBoxLayout(self.writerFrame)
        self.writerLayout.addWidget(self.writerPanelFrame)
        self.writerLayout.addWidget(self.logPanelFrame)
        self.writerLayout.setContentsMargins(0, 0, 0, 0)

        self.contentLayout = QHBoxLayout(self.contentFrame)
        self.contentLayout.addWidget(self.antPanelFrame, stretch=1)
        self.contentLayout.addWidget(self.writerFrame, stretch=1)
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


"""
Widget to create header label
"""
class HeaderLabel(QLabel):
    def __init__(self, parent):
        super().__init__(parent)

        self.initUI()

    def initUI(self):
        font = QFont()
        font.setBold(True)
        font.setPointSize(30)
        self.setFont(font)


class LineEdit(QLineEdit):
    def __init__(self, parent):
        super().__init__(parent)

        self.initUI()

    def initUI(self):
        self.setReadOnly(True)
        self.setMinimumWidth(300)
        self.setMinimumSize(200, 20)

        self.setStyleSheet("background-color: white;"
                           "border: white solid 1px;"
                           "border-radius: 1 px;"
                           "color: black;")

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
