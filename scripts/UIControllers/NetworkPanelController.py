from PyQt5.QtCore import QObject, QThread, pyqtSignal
from PyQt5.QtWidgets import QListWidgetItem, QInputDialog

import time
from scripts.ANT.ANTDriver import ANTDriver
from scripts.Helper.Workers import ScanWorker, ListenWorker
from scripts.ANT import ANTConstants
from scripts.Helper.XMLHandler import XMLWriter, XMLReader


class NetworkPanelController(QObject):
    scanSignal = pyqtSignal()
    listenSignal = pyqtSignal()
    stopSignal = pyqtSignal()
    devicesBroadcastingSignal = pyqtSignal(object)

    def __init__(self, ui_scanPanel):
        super().__init__()

        self.ui_scanPanel = ui_scanPanel

        self.ui_connectBtn = ui_scanPanel.connectBtn
        self.ui_connectBtn.clicked.connect(self.scan)

        self.ui_disconnectBtn = ui_scanPanel.disconnectBtn
        self.ui_disconnectBtn.clicked.connect(self.disconnect)

        self.ui_resetBtn = ui_scanPanel.resetBtn
        self.ui_resetBtn.clicked.connect(self.reset)

        self.ui_devicesListBox = ui_scanPanel.devicesListBox
        self.ui_devicesListBox.itemDoubleClicked.connect(self.renameDevice)

        self.ui_sessionText = ui_scanPanel.sessionText

        self.antDriver = ANTDriver()

        self.scanWorker = ScanWorker(self.antDriver)
        self.scanThread = QThread()
        self.scanWorker.moveToThread(self.scanThread)

        self.scanWorker.devicesFound.connect(self.devicesFound)
        self.scanSignal.connect(self.scanWorker.scan)

        self.listenWorker = ListenWorker(self.antDriver)
        self.listenThread = QThread()
        self.listenWorker.moveToThread(self.listenThread)
        self.listenWorker.messageReceived.connect(self.updateNetworkStatistics)

        self.listenSignal.connect(self.listenWorker.listen)

        self.broadcastingDevices = []
        self.broadcastingProfiles = []
        self.sessionTime = 0
        self.sessionStartTime = 0
        self.numMessagesReceived = 0
        self.messageFrequency = 0

        self.ui_connectBtn.setEnabled(True)
        self.ui_disconnectBtn.setEnabled(False)
        self.ui_resetBtn.setEnabled(False)

    def scan(self):
        self.ui_connectBtn.setEnabled(False)
        self.ui_disconnectBtn.setEnabled(False)
        self.ui_resetBtn.setEnabled(False)

        self.broadcastingDevices = []

        if not self.scanThread.isRunning():
            self.scanThread.start()

        self.scanSignal.emit()

    def disconnect(self):
        self.ui_connectBtn.setEnabled(True)
        self.ui_disconnectBtn.setEnabled(False)
        self.ui_resetBtn.setEnabled(False)

        self.antDriver.disconnect()
        self.listenWorker.messageReceived.disconnect(self.updateNetworkStatistics)

        if self.scanThread.isRunning():
            self.scanThread.exit()

        if self.listenThread.isRunning():
            self.listenThread.exit()

        self.clear()

        self.stopSignal.emit()

    def reset(self):
        self.ui_connectBtn.setEnabled(False)
        self.ui_disconnectBtn.setEnabled(True)
        self.ui_resetBtn.setEnabled(True)
        self.sessionTime = 0
        self.sessionStartTime = time.time()
        self.messageFrequency = 0
        self.numMessagesReceived = 0

        self.antDriver.reset()

    def renameDevice(self, selectedDevice):
        if selectedDevice is None:
            return

        if not selectedDevice.name:
            return

        inputDialog = InputDialog()

        name, okSelected = inputDialog.getText(inputDialog, 'Rename Device', 'Enter Desired Device Name:')

        if okSelected:
            xmlWriter = XMLWriter()
            xmlWriter.addDevice(name, selectedDevice.number)

    def clear(self):
        self.ui_devicesListBox.clear()
        self.ui_sessionText.clear()
        self.sessionTime = 0
        self.messageFrequency = 0
        self.numMessagesReceived = 0
        self.broadcastingDevices = []

    def devicesFound(self, devices):
        if self.scanThread.isRunning():
            self.scanThread.exit()

        if not devices:
            self.ui_connectBtn.setEnabled(True)
            self.ui_disconnectBtn.setEnabled(False)
            self.ui_resetBtn.setEnabled(False)

            return

        self.sessionStartTime = time.time()

        self.ui_connectBtn.setEnabled(False)
        self.ui_disconnectBtn.setEnabled(True)
        self.ui_resetBtn.setEnabled(True)

        if not self.listenThread.isRunning():
            self.listenThread.start()

        self.listenSignal.emit()

        xmlReader = XMLReader()
        deviceNumber2Name = xmlReader.getDeviceNumber2Name()

        for deviceNumber in devices:
            deviceName = "Unknown Device" + str(deviceNumber)

            if deviceNumber in deviceNumber2Name:
                deviceName = deviceNumber2Name[deviceNumber]

            elif deviceNumber in ANTConstants.DeviceNumber2Name:
                deviceName = ANTConstants.DeviceNumber2Name[deviceNumber]

            antDevice = ANTDevice(deviceName, deviceNumber)
            self.broadcastingDevices.append(antDevice)

            antDevice.setText(antDevice.name)

            self.ui_devicesListBox.addItem(antDevice)

        self.devicesBroadcastingSignal.emit(self.broadcastingDevices)

    def updateNetworkStatistics(self, profileMessage):
        if profileMessage.msg.deviceType not in self.broadcastingProfiles:
            self.broadcastingProfiles.append(profileMessage.msg.deviceType)

        self.sessionTime = time.time() - self.sessionStartTime
        self.numMessagesReceived += 1
        self.messageFrequency = self.numMessagesReceived / self.sessionTime
        self.ui_sessionText.setText('Connection Duration (s): ' + str(round(self.sessionTime)))
        self.ui_sessionText.append('Devices Broadcasting: ' + str(len(self.broadcastingDevices)))
        self.ui_sessionText.append('Profiles Received: ' + str(len(self.broadcastingProfiles)))
        self.ui_sessionText.append('Messages Received: ' + str(self.numMessagesReceived))
        self.ui_sessionText.append('Message Frequency (Hz): ' + str(round(self.messageFrequency)))


class ANTDevice(QListWidgetItem):
    def __init__(self, name, number):
        super().__init__()

        self.name = name
        self.number = number

        self.initUI()

    def initUI(self):
        self.setText(self.name)
        font = self.font()
        font.setPointSize(10)
        self.setFont(font)


class InputDialog(QInputDialog):
    def __init__(self):
        super().__init__()
