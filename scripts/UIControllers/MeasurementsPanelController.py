class MeasurementsPanelController:
    def __init__(self, measurementsPanel, antPanelController):
        self.measurementsPanel = measurementsPanel
        self.antPanelController = antPanelController

        self.measurementsData = []

        self.ui_antPanel = self.antPanelController.ui_antPanel
        self.activeMeasurements = self.measurementsPanel.activeMeasurements
        self.addBtn = self.measurementsPanel.addBtn
        self.removeBtn = self.measurementsPanel.removeBtn

        self.measurementsPanel.addBtn.clicked.connect(self.addSelected)
        self.measurementsPanel.removeBtn.clicked.connect(self.removeSelected)

    def addSelected(self):
        selectedDevice = self.antPanelController.selectedDevice
        selectedProfile = self.antPanelController.selectedProfile
        selectedDataPage = self.antPanelController.selectedDataPage
        selectedPageMeasurement = self.antPanelController.selectedPageMeasurement

        if selectedPageMeasurement is None:
            return

        for _data in self.measurementsData:
            deviceMatch = (selectedDevice == _data.device)
            profileMatch = (selectedProfile == _data.profile)
            dataPageMatch = (selectedDataPage == _data.dataPage)
            pageMeasurementMatch = (selectedPageMeasurement == _data.pageMeasurement)

            if deviceMatch & profileMatch & dataPageMatch & pageMeasurementMatch:
                return

        _data = MeasurementsData()
        _data.device = selectedDevice
        _data.deviceName = self.ui_antPanel.devices.currentItem().text()
        _data.profile = selectedProfile
        _data.profileName = self.ui_antPanel.profiles.currentItem().text()
        _data.dataPage = selectedDataPage
        _data.dataPageName = self.ui_antPanel.dataPages.currentItem().text()
        _data.pageMeasurement = selectedPageMeasurement

        self.measurementsData.append(_data)

        activeMeasurement = self.ui_antPanel.devices.currentItem().text() + "->" \
                            + self.ui_antPanel.profiles.currentItem().text() + "->" \
                            + self.ui_antPanel.dataPages.currentItem().text() + "->" \
                            + self.ui_antPanel.pageMeasurements.currentItem().text()

        self.activeMeasurements.addItem(activeMeasurement)

    def removeSelected(self):
        if self.activeMeasurements.count() == 0:
            return

        selectedActiveMeasurementItem = self.activeMeasurements.currentItem()

        if not selectedActiveMeasurementItem:
            return

        self.activeMeasurements.takeItem(self.activeMeasurements.row(selectedActiveMeasurementItem))

        selectedMeasurement = selectedActiveMeasurementItem.text().split('->')[-1]

        for _data in self.measurementsData:
            if _data.pageMeasurement == selectedMeasurement:
                self.measurementsData.remove(_data)

    def updateMeasurementsData(self, profileMessage):
        for _data in self.measurementsData:
            if profileMessage.msg.deviceNumber == _data.device:
                if profileMessage.msg.deviceType == _data.profile:
                    if profileMessage.dataPageNumber == _data.dataPage:
                        if _data.pageMeasurement in self.antPanelController.pageMeasurements:
                            _data.measurementValue = self.antPanelController.pageMeasurements[_data.pageMeasurement]()

    def clear(self):
        self.measurementsData = None
        self.activeMeasurements.clear()


class MeasurementsData:
    def __init__(self):
        self.device = None
        self.deviceName = None
        self.profile = None
        self.profileName = None
        self.dataPage = None
        self.dataPageName = None
        self.pageMeasurement = None
        self.measurementValue = None
