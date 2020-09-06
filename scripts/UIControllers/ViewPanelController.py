from scripts.ANT.ANTConstants import *
from scripts.UIControllers.ANTPanelController import ANTPanelController


class ViewPanelController(ANTPanelController):
    GAUGE_READOUT = 0
    DIGITAL_READOUT = 1

    def __init__(self, ui_viewPanel, ui_logPanel):
        self.ui_viewPanel = ui_viewPanel

        self.ui_antPanel = self.ui_viewPanel.antPanel
        self.ui_logPanel = ui_logPanel

        super().__init__(self.ui_antPanel, self.ui_logPanel)

    def messageReceived(self, profileMessage):
        super().messageReceived(profileMessage)

        if profileMessage is None:
            return

        if profileMessage.msg.deviceNumber != self.selectedDevice:
            return

        self.profileMessage = profileMessage

        if self.profileMessage.msg.deviceType == self.selectedProfile:
            if self.profileMessage.dataPageNumber == self.selectedDataPage:
                if self.selectedPageMeasurement is not None:
                    self.updateReadout()

        if any(selection is None for selection in [self.selectedDevice, self.selectedProfile,
                                                   self.selectedDataPage, self.selectedPageMeasurement]):

            self.clearReadout()

    def clearReadout(self):
        if self.ui_viewPanel.readoutLayout.currentIndex() == self.DIGITAL_READOUT:
            self.ui_viewPanel.digitalReadoutUnits.setText('')
            self.ui_viewPanel.digitalReadout.display(0)
            self.ui_viewPanel.digitalReadout.repaint()
        elif self.ui_viewPanel.readoutLayout.currentIndex() == self.GAUGE_READOUT:
            self.ui_viewPanel.gaugeReadout.setGaugeValueUnits('')
            self.ui_viewPanel.gaugeReadout.updateGaugeValue(0)

    def updateReadout(self):
        readoutType = self.getReadoutType()
        measurement = self.getMeasurement()

        if readoutType == self.DIGITAL_READOUT:
            self.ui_viewPanel.readoutLayout.setCurrentIndex(self.DIGITAL_READOUT)
            measurement = str(int(measurement))
            measurementLength = len(measurement)
            self.ui_viewPanel.digitalReadoutUnits.setText(pageMeasurementUnits[self.selectedPageMeasurement])
            self.ui_viewPanel.digitalReadout.setDigitCount(measurementLength)
            self.ui_viewPanel.digitalReadout.display(measurement)
            self.ui_viewPanel.digitalReadout.repaint()

        elif readoutType == self.GAUGE_READOUT:
            self.ui_viewPanel.readoutLayout.setCurrentIndex(self.GAUGE_READOUT)

            measurement = int(measurement)
            minValue =  pageMeasurementBounds[self.selectedPageMeasurement][0]
            maxValue = pageMeasurementBounds[self.selectedPageMeasurement][1]
            self.ui_viewPanel.gaugeReadout.setGaugeValueUnits(pageMeasurementUnits[self.selectedPageMeasurement])
            self.ui_viewPanel.gaugeReadout.setMinGaugeValue(minValue)
            self.ui_viewPanel.gaugeReadout.setMaxGaugeValue(maxValue)
            self.ui_viewPanel.gaugeReadout.updateGaugeValue(measurement)

    def getMeasurement(self):
        if self.selectedPageMeasurement in self.pageMeasurements:
            measurement = self.pageMeasurements[self.selectedPageMeasurement]()

        else:
            measurement = 0

        return measurement

    def getReadoutType(self):
        readout = self.GAUGE_READOUT

        pageMeasurements = {
                            ELAPSED_TIME_MEASUREMENT: self.DIGITAL_READOUT,
                            DISTANCE_TRAVELED_MEASUREMENT: self.DIGITAL_READOUT,
                            INSTANTANEOUS_CADENCE_MEASUREMENT: self.GAUGE_READOUT,
                            INSTANTANEOUS_POWER_MEASUREMENT: self.GAUGE_READOUT,
                            PEDAL_POWER_MEASUREMENT: self.GAUGE_READOUT,
                            AVERAGE_POWER_MEASUREMENT: self.GAUGE_READOUT,
                            INSTANTANEOUS_SPEED_MEASUREMENT: self.GAUGE_READOUT,
                            AVERAGE_CADENCE_MEASUREMENT: self.GAUGE_READOUT,
                            AVERAGE_SPEED_MEASUREMENT: self.GAUGE_READOUT
                            }

        if self.selectedPageMeasurement in pageMeasurements:
            readout = pageMeasurements[self.selectedPageMeasurement]

        return readout

    def clear(self):
        self.ui_antPanel.devices.clear()
        self.ui_antPanel.profiles.clear()
        self.ui_antPanel.dataPages.clear()
        self.ui_antPanel.pageMeasurements.clear()
        self.clearReadout()
