from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QMainWindow, QStackedLayout, QFrame
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QGridLayout
from PyQt5.QtCore import Qt

from scripts.UI.ViewPanel import ViewPanel
from scripts.UI.TitleBar import TitleBar
from scripts.UI.SideMenu import SideMenu
from scripts.UI.StatusBar import StatusBar
from scripts.UI.WritePanel import WritePanel
from scripts.UI.NetworkPanel import NetworkPanel


"""
Widget containing the main window (everything the user sees)
"""
class MainWindow(QMainWindow):
    def __init__(self, app):
        super().__init__()

        # UI Title Bar
        self.ui_titleBar = TitleBar(self)

        # UI Status Bar. Add grip to status bar to allow for resizing window
        self.ui_statusBar = StatusBar(self)

        # UI Side Menu
        self.ui_sideMenu = SideMenu(self)

        # UI View Panels
        self.ui_viewPanels = [ViewPanel(self),
                              ViewPanel(self),
                              ViewPanel(self),
                              ViewPanel(self)]

        # UI UDP/CSV Panel
        self.ui_writePanel = WritePanel(self)

        # UI ANT+ Scan Panel
        self.ui_scanPanel = NetworkPanel(self)

        self.initUI()

        self.ui_sideMenu.networkBtn.clicked.connect(lambda:
                                                   self.contentLayout.setCurrentIndex(self.ui_sideMenu.SCAN_BUTTON))

        self.ui_sideMenu.viewBtn.clicked.connect(lambda:
                                                 self.contentLayout.setCurrentIndex(self.ui_sideMenu.VIEW_BUTTON))
        self.ui_sideMenu.writeBtn.clicked.connect(lambda:
                                                   self.contentLayout.setCurrentIndex(self.ui_sideMenu.WRITE_BUTTON))

    def initUI(self):
        self.setObjectName("mainWindow")

        self.resize(1000,800)

        # self.centralWidget = QtWidgets.QWidget(self)
        # self.centralWidget.setObjectName("centralWidget")

        self.uiFrame = QFrame(self)
        self.uiFrame.setFrameShape(QFrame.NoFrame)
        self.uiFrame.setFrameShadow(QFrame.Raised)
        self.uiFrame.setContentsMargins(0, 0, 0, 0)

        self.centralFrame = QFrame(self.uiFrame)
        self.centralFrame.setFrameShape(QFrame.NoFrame)
        self.centralFrame.setFrameShadow(QFrame.Raised)
        self.centralFrame.setContentsMargins(0, 0, 0, 0)

        self.spacerFrame = QFrame(self.centralFrame)
        self.spacerFrame.setFrameShape(QFrame.NoFrame)
        self.spacerFrame.setFrameShadow(QFrame.Raised)
        self.spacerFrame.setContentsMargins(0, 0, 0, 0)

        self.contentFrame = QFrame(self.spacerFrame)
        self.contentFrame.setFrameShape(QFrame.NoFrame)
        self.contentFrame.setFrameShadow(QFrame.Raised)
        self.contentFrame.setContentsMargins(0, 0, 0, 0)

        self.scanFrame = QFrame(self.contentFrame)
        self.scanFrame.setFrameShape(QFrame.NoFrame)
        self.scanFrame.setFrameShadow(QFrame.Raised)
        self.scanFrame.setContentsMargins(0, 0, 0, 0)
        self.scanFrame.setStyleSheet('border: 1px black')

        self.scanLayout = QHBoxLayout(self.scanFrame)
        self.scanLayout.setContentsMargins(0, 0, 0, 0)
        self.scanLayout.addWidget(self.ui_scanPanel)

        self.viewFrame = QFrame(self.contentFrame)
        self.viewFrame.setFrameShape(QFrame.NoFrame)
        self.viewFrame.setFrameShadow(QFrame.Raised)
        self.viewFrame.setContentsMargins(0, 0, 0, 0)
        self.viewFrame.setStyleSheet('border: 1px black')

        # Create grid of view panels
        self.viewLayout = QGridLayout(self.viewFrame)
        self.viewLayout.addWidget(self.ui_viewPanels[0], 1, 1)
        self.viewLayout.addWidget(self.ui_viewPanels[1], 1, 2)
        self.viewLayout.addWidget(self.ui_viewPanels[2], 2, 1)
        self.viewLayout.addWidget(self.ui_viewPanels[3], 2, 2)
        self.viewLayout.setContentsMargins(0, 0, 0, 0)
        self.viewLayout.setColumnMinimumWidth(1, 300)
        self.viewLayout.setRowMinimumHeight(1, 300)
        self.viewLayout.setColumnMinimumWidth(2, 300)
        self.viewLayout.setRowMinimumHeight(2, 300)

        self.writeFrame = QFrame(self.contentFrame)
        self.writeFrame.setFrameShape(QFrame.NoFrame)
        self.writeFrame.setFrameShadow(QFrame.Raised)
        self.writeFrame.setContentsMargins(0, 0, 0, 0)
        self.writeFrame.setStyleSheet('border: 1px black')

        self.writeLayout = QHBoxLayout(self.writeFrame)
        self.writeLayout.setContentsMargins(0, 0, 0, 0)
        self.writeLayout.addWidget(self.ui_writePanel)

        self.contentLayout = QStackedLayout(self.contentFrame)
        self.contentLayout.addWidget(self.scanFrame)
        self.contentLayout.addWidget(self.viewFrame)
        self.contentLayout.addWidget(self.writeFrame)
        self.contentLayout.setContentsMargins(0, 0, 0, 0)
        self.contentLayout.setCurrentIndex(self.ui_sideMenu.SCAN_BUTTON)

        self.spacerLayout = QVBoxLayout(self.spacerFrame)
        self.spacerLayout.addWidget(self.contentFrame)
        self.spacerLayout.setContentsMargins(5, 5, 5, 5)

        self.centralLayout = QVBoxLayout(self.centralFrame)
        self.centralLayout.addWidget(self.ui_titleBar, alignment=Qt.AlignTop)
        self.centralLayout.addWidget(self.spacerFrame)
        self.centralLayout.addWidget(self.ui_statusBar)
        self.centralLayout.setContentsMargins(0, 0, 0, 0)

        self.uiLayout = QHBoxLayout(self.uiFrame)
        self.uiLayout.addWidget(self.ui_sideMenu)
        self.uiLayout.addWidget(self.centralFrame)
        self.uiLayout.setSpacing(0)
        self.uiLayout.setContentsMargins(0, 0, 0, 0)

        self.setCentralWidget(self.uiFrame)
        self.centralWidget().setLayout(self.uiLayout)

        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)

        self.show()

    def moveWindow(self, ev):
        if ev.buttons() == Qt.LeftButton:
            self.move(self.pos() + ev.globalPos() - self.dragPos)
            self.dragPos = ev.globalPos()
            ev.accept()

    def mousePressEvent(self, ev):
        self.dragPos = ev.globalPos()
