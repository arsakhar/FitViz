from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtGui import QIcon
import time

from scripts.UIControllers.ViewPanelController import ViewPanelController
from scripts.UIControllers.WritePanelController import WritePanelController
from scripts.UIControllers.NetworkPanelController import NetworkPanelController, ANTDevice
from scripts.UI.ANTPanel import ComboBox
from scripts.Helper.Resources import *


class UIController(QObject):
    scanSignal = pyqtSignal()
    listenSignal = pyqtSignal()

    def __init__(self, ui_main):
        super().__init__()

        self.ui_main = ui_main

        self.ui_titleBar = self.ui_main.ui_titleBar
        self.ui_sideMenu = self.ui_main.ui_sideMenu
        self.ui_scanPanel = self.ui_main.ui_scanPanel
        self.ui_viewPanels = self.ui_main.ui_viewPanels
        self.ui_writePanel = self.ui_main.ui_writePanel
        self.ui_logPanel = self.ui_writePanel.logPanel

        self.childControllers = []

        self.networkListener = None
        self.networkPanelController = self.spawnNetworkPanelController()

        self.ui_titleBar.closeBtn.clicked.connect(self.closeClicked)

    def spawnNetworkPanelController(self):
        networkPanelController = NetworkPanelController(self.ui_scanPanel)
        networkPanelController.devicesBroadcastingSignal.connect(self.spawnControllers)
        networkPanelController.stopSignal.connect(self.resetControllers)

        self.networkListener = networkPanelController.listenWorker

        return networkPanelController

    def spawnControllers(self, devices):
        if not devices:
            return

        self.ui_sideMenu.networkBtn.setIcon(QIcon(resource_path("icons/cil-wifi-signal-1-connected")))

        self.spawnViewPanelControllers(devices)
        self.spawnWritePanelControllers(devices)

    def resetControllers(self):
        self.ui_sideMenu.networkBtn.setIcon(QIcon(resource_path("icons/cil-wifi-signal-1")))

        for index, child in enumerate(self.childControllers):
            child.clear()
            del child

        self.childControllers = []

        self.networkPanelController.clear()
        self.networkListener = None
        self.spawnNetworkPanelController()

    def spawnViewPanelControllers(self, devices):
        for device in devices:
            _device = ANTDevice(device.name, device.number)

            for ui_viewPanel in self.ui_viewPanels:
                if type(ui_viewPanel.antPanel.devices) == ComboBox:
                    ui_viewPanel.antPanel.devices.addItem(_device.name, _device.number)
                else:
                    ui_viewPanel.antPanel.devices.addItem(_device)

                viewPanelController = ViewPanelController(ui_viewPanel, self.ui_logPanel)
                self.networkListener.messageReceived.connect(viewPanelController.messageReceived)

                self.childControllers.append(viewPanelController)

    def spawnWritePanelControllers(self, devices):
        for device in devices:
            _device = ANTDevice(device.name, device.number)

            if type(self.ui_writePanel.antPanel.devices) == ComboBox:
                self.ui_writePanel.antPanel.devices.addItem(_device.name, _device.number)
            else:
                self.ui_writePanel.antPanel.devices.addItem(_device)

            writePanelController = WritePanelController(self.ui_writePanel, self.ui_logPanel)
            self.networkListener.messageReceived.connect(writePanelController.messageReceived)

            self.childControllers.append(writePanelController)

    def closeClicked(self):
        if self.networkPanelController:
            self.networkPanelController.disconnect()

        time.sleep(.1)

        self.ui_main.close()
