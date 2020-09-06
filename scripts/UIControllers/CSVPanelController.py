import time
from time import strftime
import csv

from scripts.UIControllers.MeasurementsPanelController import MeasurementsPanelController


class CSVPanelController:
    def __init__(self, ui_csvPanel, ui_logPanel, antPanelController):
        self.ui_csvPanel = ui_csvPanel
        self.ui_logPanel = ui_logPanel

        self.antPanelController = antPanelController

        self.measurementsPanel = self.ui_csvPanel.measurementsPanel
        self.measurementsPanelController = MeasurementsPanelController(self.measurementsPanel, self.antPanelController)

        self.csvWriterActive = False
        self.csvFile = None
        self.csvWriter = None
        self.csvStartTime = None

        self.controlsFrame = self.ui_csvPanel.controlsFrame
        self.saveFrame = self.ui_csvPanel.saveFrame

        self.saveDialog = self.ui_csvPanel.saveDialog
        self.saveField = self.ui_csvPanel.saveField
        self.saveBtn = self.ui_csvPanel.saveBtn

        self.startBtn = self.ui_csvPanel.startBtn
        self.pauseBtn = self.ui_csvPanel.pauseBtn
        self.stopBtn = self.ui_csvPanel.stopBtn

        self.controlsFrame.setEnabled(False)
        self.saveFrame.setEnabled(False)
        self.stopBtn.setEnabled(False)

        self.saveBtn.clicked.connect(self.saveSelected)
        self.startBtn.clicked.connect(self.startSelected)
        self.pauseBtn.clicked.connect(self.pauseSelected)
        self.stopBtn.clicked.connect(self.stopSelected)

    def messageReceived(self, profileMessage):
        self.updateMeasurementsData(profileMessage)

        if self.csvWriterActive:
            self.updateCSV()

        else:
            self.updateConfigUIState()

    def updateConfigUIState(self):
        if self.measurementsPanel.activeMeasurements.count() == 0:
            self.controlsFrame.setEnabled(False)
            self.saveFrame.setEnabled(False)

        else:
            self.controlsFrame.setEnabled(True)
            self.saveFrame.setEnabled(True)

        if self.saveField.text():
            self.startBtn.setEnabled(True)
        else:
            self.startBtn.setEnabled(False)

    def openWriter(self):
        self.ui_csvPanel.runBtnsLayout.setCurrentIndex(self.ui_csvPanel.PAUSE_BUTTON_INDEX)

        self.measurementsPanel.setEnabled(False)
        self.saveField.setEnabled(False)
        self.saveBtn.setEnabled(False)
        self.stopBtn.setEnabled(True)

        self.csvFile = open(self.saveField.text(), 'w', newline='')

        self.csvWriter = csv.writer(self.csvFile)

        header = [_data.pageMeasurement for _data in self.measurementsPanelController.measurementsData]
        header.insert(0, "Time (s)")

        self.csvWriter.writerow(header)

        self.csvFile.flush()

        self.csvWriterActive = True
        self.csvStartTime = time.time()

        self.ui_logPanel.append(strftime("%a, %d %b %Y %H:%M:%S %p", time.localtime())
                                + ': Opening CSV Writer')

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
        self.ui_csvPanel.runBtnsLayout.setCurrentIndex(self.ui_csvPanel.PAUSE_BUTTON_INDEX)

        self.csvWriterActive = True

        self.ui_logPanel.append(strftime("%a, %d %b %Y %H:%M:%S %p", time.localtime())
                                + ': Resuming CSV Writer')

    def pauseWriter(self):
        self.ui_csvPanel.runBtnsLayout.setCurrentIndex(self.ui_csvPanel.START_BUTTON_INDEX)

        self.csvWriterActive = False

        self.ui_logPanel.append(strftime("%a, %d %b %Y %H:%M:%S %p", time.localtime())
                                + ': Pausing CSV Writer')

    def closeWriter(self):
        self.measurementsPanel.setEnabled(True)
        self.saveField.setEnabled(True)
        self.saveBtn.setEnabled(True)

        self.ui_csvPanel.runBtnsLayout.setCurrentIndex(self.ui_csvPanel.START_BUTTON_INDEX)

        self.csvFile.close()

        self.csvFile = None
        self.csvWriter = None
        self.csvWriterActive = False

        self.stopBtn.setEnabled(False)

        self.ui_logPanel.append(strftime("%a, %d %b %Y %H:%M:%S %p", time.localtime())
                                + ': Closing CSV Writer')

    def updateMeasurementsData(self, profileMessage):
        self.measurementsPanelController.updateMeasurementsData(profileMessage)

    def updateCSV(self):
        payload = [_data.measurementValue for _data in self.measurementsPanelController.measurementsData]
        currTime = time.time()

        runningTime = currTime - self.csvStartTime
        runningTime = round(runningTime, 2)
        payload.insert(0, runningTime)

        self.csvWriter.writerow(payload)

        self.csvFile.flush()

        # self.ui_logPanel.append(strftime("%a, %d %b %Y %H:%M:%S %p", time.localtime())
        #                         + ': Updating CSV - Payload ' + '[' + ', '.join(payload) + ']')

    def saveSelected(self):
        fileName, _ = self.saveDialog.getSaveFileName(None,
                                                      "Select Save Path",
                                                      "",
                                                      "Comma Separated Values (*.csv)",
                                                      options=self.saveDialog.options)

        if not fileName:
            return

        fileName = fileName.split('.')[0]

        self.saveField.setText(fileName + '.csv')

    def startSelected(self):
        if self.csvWriter is None:
                self.openWriter()

        else:
            self.resumeWriter()

    def pauseSelected(self):
        self.pauseWriter()

    def stopSelected(self):
        self.closeWriter()

    def clear(self):
        if self.csvWriterActive:
            self.closeWriter()

        self.measurementsPanelController.clear()
        self.saveField.setText('')
