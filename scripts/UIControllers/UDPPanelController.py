from PyQt5.QtNetwork import QHostAddress
import time
from time import strftime
import socket

from scripts.UIControllers.MeasurementsPanelController import MeasurementsPanelController


class UDPPanelController:
    def __init__(self, ui_udpPanel, ui_logPanel, antPanelController):
        self.ui_udpPanel = ui_udpPanel
        self.ui_logPanel = ui_logPanel

        self.antPanelController = antPanelController

        self.measurementsPanel = self.ui_udpPanel.measurementsPanel
        self.measurementsPanelController = MeasurementsPanelController(self.measurementsPanel, self.antPanelController)

        self.udpWriterActive = False
        self.udpWriter = None

        self.networkingFrame = self.ui_udpPanel.networkingFrame
        self.controlsFrame = self.ui_udpPanel.controlsFrame

        self.ipAddressField = self.ui_udpPanel.ipAddressField
        self.portField = self.ui_udpPanel.portField

        self.ipAddress = None
        self.port = None

        self.startBtn = self.ui_udpPanel.startBtn
        self.pauseBtn = self.ui_udpPanel.pauseBtn
        self.stopBtn = self.ui_udpPanel.stopBtn

        self.controlsFrame.setEnabled(False)

        self.stopBtn.setEnabled(False)

        self.ipAddressField.textChanged.connect(self.ipAddressFieldUpdated)
        self.portField.textChanged.connect(self.portFieldUpdated)

        self.startBtn.clicked.connect(self.startSelected)
        self.pauseBtn.clicked.connect(self.pauseSelected)
        self.stopBtn.clicked.connect(self.stopSelected)

    def messageReceived(self, profileMessage):
        self.updateMeasurementsData(profileMessage)

        if self.udpWriterActive:
            self.writeToUDP()

        else:
            self.updateConfigUIState()

    def updateConfigUIState(self):
        if self.measurementsPanel.activeMeasurements.count() == 0:
            self.controlsFrame.setEnabled(False)
            self.networkingFrame.setEnabled(False)

        else:
            self.controlsFrame.setEnabled(True)
            self.networkingFrame.setEnabled(True)

        if (self.ipAddress is not None) & (self.port is not None):
            self.startBtn.setEnabled(True)
        else:
            self.startBtn.setEnabled(False)

    def openWriter(self):
        self.networkingFrame.setEnabled(False)

        self.ui_udpPanel.runBtnsLayout.setCurrentIndex(self.ui_udpPanel.PAUSE_BUTTON_INDEX)

        self.measurementsPanel.setEnabled(False)
        self.stopBtn.setEnabled(True)

        self.udpWriter = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.udpWriterActive = True

        self.ui_logPanel.append(strftime("%a, %d %b %Y %H:%M:%S %p", time.localtime())
                                + ': Opening UDP Writer')

        for _data in self.measurementsPanelController.measurementsData:
            dataString = _data.deviceName \
                         + "->" + _data.profileName \
                         + "->" + _data.dataPageName \
                         + "->" + _data.pageMeasurement

            self.ui_logPanel.append(strftime("%a, %d %b %Y %H:%M:%S %p", time.localtime())
                                    + ': Writing ' + dataString)


        payloadString = [_data.pageMeasurement for _data in self.measurementsPanelController.measurementsData]
        payloadString = ";".join(str(x) for x in payloadString)

        self.ui_logPanel.append(strftime("%a, %d %b %Y %H:%M:%S %p", time.localtime())
                                + ': Payload Format - ' + '[' + payloadString + ']')

    def resumeWriter(self):
        self.ui_udpPanel.runBtnsLayout.setCurrentIndex(self.ui_udpPanel.PAUSE_BUTTON_INDEX)

        self.udpWriterActive = True

        self.ui_logPanel.append(strftime("%a, %d %b %Y %H:%M:%S %p", time.localtime())
                                + ': Resuming UDP Writer')

    def pauseWriter(self):
        self.ui_udpPanel.runBtnsLayout.setCurrentIndex(self.ui_udpPanel.START_BUTTON_INDEX)

        self.udpWriterActive = False

        self.ui_logPanel.append(strftime("%a, %d %b %Y %H:%M:%S %p", time.localtime())
                                + ': Pausing UDP Writer')

    def closeWriter(self):
        self.measurementsPanel.setEnabled(True)

        self.ui_udpPanel.runBtnsLayout.setCurrentIndex(self.ui_udpPanel.START_BUTTON_INDEX)

        self.udpWriter = None
        self.udpWriterActive = False

        self.stopBtn.setEnabled(False)

        self.ui_logPanel.append(strftime("%a, %d %b %Y %H:%M:%S %p", time.localtime())
                                + ': Closing UDP Writer')

    def updateMeasurementsData(self, profileMessage):
        self.measurementsPanelController.updateMeasurementsData(profileMessage)

    def writeToUDP(self):
        payload = [_data.measurementValue for _data in self.measurementsPanelController.measurementsData]

        # we deliver the payload as var1; var2; var3; var4 as a bytearray
        # the receiving end should decode the byte array back into a string
        payload = ";".join(str(x) for x in payload)

        payload = bytearray(payload, "utf-8")

        self.udpWriter.sendto(payload, (self.ipAddress, self.port))

        # self.ui_logPanel.append(strftime("%a, %d %b %Y %H:%M:%S %p", time.localtime())
        #                         + ': Writing UDP - Payload ' + '[' + payload.decode() + ']')

    def startSelected(self):
        if self.udpWriter is None:
            self.openWriter()

        else:
            self.resumeWriter()

    def pauseSelected(self):
        self.pauseWriter()

    def stopSelected(self):
        self.closeWriter()

    def ipAddressFieldUpdated(self):
        hostAddress = QHostAddress()

        if hostAddress.setAddress(self.ipAddressField.text()):
            self.ipAddress = self.ipAddressField.text()
        else:
            self.ipAddress = None

    def portFieldUpdated(self):
        try:
            self.port = int(self.portField.text())
        except:
            self.port = None

    def clear(self):
        if self.udpWriterActive:
            self.closeWriter()

        self.ipAddressField.setText('')
        self.portField.setText('')
        self.measurementsPanelController.clear()
