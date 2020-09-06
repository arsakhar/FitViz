from PyQt5.QtCore import QObject

from scripts.ANT.ANTConstants import *
from scripts.UI.ANTPanel import ComboBox


class ANTPanelController(QObject):
    def __init__(self, ui_antPanel, ui_logPanel):
        super().__init__()

        self.ui_antPanel = ui_antPanel
        self.ui_logPanel = ui_logPanel

        self.selectedDevice = None
        self.selectedProfile = None
        self.selectedDataPage = None
        self.selectedPageMeasurement = None

        self.listedDevices = []
        self.listedProfiles = []
        self.listedDataPages = []
        self.listedPageMeasurements = []
        self.profileMessage = None

        self.pageMeasurements = {PEDAL_POWER_MEASUREMENT: lambda: self.profileMessage.pedalPower,
                                 INSTANTANEOUS_POWER_MEASUREMENT: lambda: self.profileMessage.instantaneousPower,
                                 AVERAGE_POWER_MEASUREMENT: lambda: self.profileMessage.averagePower,
                                 INSTANTANEOUS_CADENCE_MEASUREMENT: lambda: self.profileMessage.instantaneousCadence,
                                 AVERAGE_CADENCE_MEASUREMENT: lambda: self.profileMessage.averageCadence,
                                 INSTANTANEOUS_SPEED_MEASUREMENT: lambda: self.profileMessage.instantaneousSpeed,
                                 AVERAGE_SPEED_MEASUREMENT: lambda: self.profileMessage.averageSpeed,
                                 DISTANCE_TRAVELED_MEASUREMENT: lambda: self.profileMessage.distanceTraveled,
                                 ELAPSED_TIME_MEASUREMENT: lambda: self.profileMessage.elapsedTime,
                                 HEART_RATE_MEASUREMENT: lambda: self.profileMessage.heartRate
                                 }

        if type(self.ui_antPanel.devices) == ComboBox:
            self.ui_antPanel.devices.activated.connect(self.deviceSelected)
        else:
            self.ui_antPanel.devices.itemClicked.connect(self.deviceSelected)

        self.ui_antPanel.profiles.itemClicked.connect(self.profileSelected)
        self.ui_antPanel.dataPages.itemClicked.connect(self.dataPageSelected)
        self.ui_antPanel.pageMeasurements.itemClicked.connect(self.pageMeasurementSelected)

    def messageReceived(self, profileMessage):
        # self.ui_logPanel.append(strftime("%a, %d %b %Y %H:%M:%S %p", time.localtime())
        #                         + ': ANT+ message received ' + str(profileMessage))

        if profileMessage is None:
            return

        if profileMessage.msg.deviceNumber != self.selectedDevice:
            return

        self.profileMessage = profileMessage

        self.updateProfileListBox()
        if self.profileMessage.msg.deviceType == self.selectedProfile:
            self.updateDataPageListBox()

    def deviceSelected(self, deviceIndex):
        if type(self.ui_antPanel.devices) == ComboBox:
            selectedDevice = self.ui_antPanel.devices.itemData(deviceIndex)
        else:
            selectedDevice = self.ui_antPanel.devices.currentItem().number

        if selectedDevice != self.selectedDevice:
            self.selectedDevice = selectedDevice
            self.selectedProfile = None
            self.selectedDataPage = None
            self.selectedPageMeasurement = None

            self.ui_antPanel.profiles.clear()
            self.ui_antPanel.dataPages.clear()
            self.ui_antPanel.pageMeasurements.clear()

            self.listedProfiles = []
            self.listedDataPages = []
            self.listedPageMeasurements = []

    def profileSelected(self):
        selectedProfile = self.ui_antPanel.profiles.currentItem().text()

        if not selectedProfile:
            return

        selectedProfile = ProfileName2Number[selectedProfile]

        if selectedProfile != self.selectedProfile:
            self.selectedProfile = selectedProfile
            self.selectedDataPage = None
            self.selectedPageMeasurement = None

            self.ui_antPanel.dataPages.clear()
            self.ui_antPanel.pageMeasurements.clear()

            self.listedDataPages = []
            self.listedPageMeasurements = []

    def dataPageSelected(self):
        selectedDataPage = self.ui_antPanel.dataPages.currentItem().text()

        if not selectedDataPage:
            return

        selectedDataPage = DataPageName2Number[selectedDataPage]

        if selectedDataPage != self.selectedDataPage:
            self.selectedDataPage = selectedDataPage
            self.selectedPageMeasurement = None

            self.ui_antPanel.pageMeasurements.clear()
            self.listedPageMeasurements = []

            self.updatePageMeasurementListBox()

    def pageMeasurementSelected(self):
        selectedPageMeasurement = self.ui_antPanel.pageMeasurements.currentItem().text()

        if not selectedPageMeasurement:
            return

        self.selectedPageMeasurement = selectedPageMeasurement

    def updateProfileListBox(self):
        profile = self.profileMessage.msg.deviceType

        if profile in self.listedProfiles:
            return

        self.listedProfiles.append(profile)

        if profile == FITNESS_EQUIPMENT_PROFILE:
            self.ui_antPanel.profiles.addItem(FITNESS_EQUIPMENT_PROFILE_STRING)

        elif profile == POWER_PROFILE:
            self.ui_antPanel.profiles.addItem(POWER_PROFILE_STRING)

        elif profile == SPEED_PROFILE:
            self.ui_antPanel.profiles.addItem(SPEED_PROFILE_STRING)

        elif profile == CADENCE_PROFILE:
            self.ui_antPanel.profiles.addItem(CADENCE_PROFILE_STRING)

        elif profile == SPEED_CADENCE_PROFILE:
            self.ui_antPanel.profiles.addItem(SPEED_CADENCE_PROFILE_STRING)

    def updateDataPageListBox(self):
        dataPage = self.profileMessage.dataPageNumber

        if dataPage in self.listedDataPages:
            return

        self.listedDataPages.append(dataPage)

        if self.selectedProfile == FITNESS_EQUIPMENT_PROFILE:
            if dataPage == TRAINER_TORQUE_DATA:
                self.ui_antPanel.dataPages.addItem(TRAINER_TORQUE_DATA_STRING)

            if dataPage == GENERAL_FE_DATA:
                self.ui_antPanel.dataPages.addItem(GENERAL_FE_DATA_STRING)

            if dataPage == TRAINER_BIKE_DATA:
                self.ui_antPanel.dataPages.addItem(TRAINER_BIKE_DATA_STRING)

        elif self.selectedProfile == POWER_PROFILE:
            if dataPage == STANDARD_POWER_DATA:
                self.ui_antPanel.dataPages.addItem(STANDARD_POWER_DATA_STRING)

            if dataPage == WHEEL_TORQUE_DATA:
                self.ui_antPanel.dataPages.addItem(WHEEL_TORQUE_DATA_STRING)

        elif self.selectedProfile == SPEED_PROFILE:
            if dataPage == SPEED_DEFAULT_DATA:
                self.ui_antPanel.dataPages.addItem(SPEED_DEFAULT_DATA_STRING)

        elif self.selectedProfile == CADENCE_PROFILE:
            if dataPage == CADENCE_DEFAULT_DATA:
                self.ui_antPanel.dataPages.addItem(CADENCE_DEFAULT_DATA_STRING)

        elif self.selectedProfile == SPEED_CADENCE_PROFILE:
            if dataPage == SC_DEFAULT_DATA:
                self.ui_antPanel.dataPages.addItem(SC_DEFAULT_DATA_STRING)

    def updatePageMeasurementListBox(self):
        self.ui_antPanel.pageMeasurements.clear()
        self.listedPageMeasurements = []

        if self.selectedDataPage is None:
            return

        if self.selectedProfile == FITNESS_EQUIPMENT_PROFILE:
            if self.selectedDataPage == TRAINER_TORQUE_DATA:
                self.listedPageMeasurements.extend((INSTANTANEOUS_SPEED_MEASUREMENT,
                                                    DISTANCE_TRAVELED_MEASUREMENT,
                                                    AVERAGE_TORQUE_MEASUREMENT,
                                                    AVERAGE_POWER_MEASUREMENT))

            elif self.selectedDataPage == GENERAL_FE_DATA:
                self.listedPageMeasurements.extend((ELAPSED_TIME_MEASUREMENT,
                                                    DISTANCE_TRAVELED_MEASUREMENT,
                                                    INSTANTANEOUS_SPEED_MEASUREMENT,
                                                    HEART_RATE_MEASUREMENT))

            elif self.selectedDataPage == TRAINER_BIKE_DATA:
                self.listedPageMeasurements.extend((INSTANTANEOUS_CADENCE_MEASUREMENT,
                                                    INSTANTANEOUS_POWER_MEASUREMENT,
                                                    AVERAGE_POWER_MEASUREMENT))

        elif self.selectedProfile == POWER_PROFILE:
            if self.selectedDataPage == STANDARD_POWER_DATA:
                self.listedPageMeasurements.extend((PEDAL_POWER_MEASUREMENT,
                                                    INSTANTANEOUS_CADENCE_MEASUREMENT,
                                                    INSTANTANEOUS_POWER_MEASUREMENT,
                                                    AVERAGE_POWER_MEASUREMENT))

            elif self.selectedDataPage == WHEEL_TORQUE_DATA:
                self.listedPageMeasurements.extend((INSTANTANEOUS_SPEED_MEASUREMENT,
                                                    DISTANCE_TRAVELED_MEASUREMENT,
                                                    AVERAGE_TORQUE_MEASUREMENT,
                                                    AVERAGE_POWER_MEASUREMENT))

        elif self.selectedProfile == SPEED_PROFILE:
            if self.selectedDataPage == SPEED_DEFAULT_DATA:
                self.listedPageMeasurements.extend((INSTANTANEOUS_SPEED_MEASUREMENT,
                                                    DISTANCE_TRAVELED_MEASUREMENT,
                                                    AVERAGE_SPEED_MEASUREMENT))

        elif self.selectedProfile == CADENCE_PROFILE:
            if self.selectedDataPage == CADENCE_DEFAULT_DATA:
                self.listedPageMeasurements.extend((INSTANTANEOUS_CADENCE_MEASUREMENT,
                                                    DISTANCE_TRAVELED_MEASUREMENT,
                                                    AVERAGE_CADENCE_MEASUREMENT))

        elif self.selectedProfile == SPEED_CADENCE_PROFILE:
            if self.selectedDataPage == SC_DEFAULT_DATA:
                self.listedPageMeasurements.extend((INSTANTANEOUS_SPEED_MEASUREMENT,
                                                    DISTANCE_TRAVELED_MEASUREMENT,
                                                    INSTANTANEOUS_CADENCE_MEASUREMENT,
                                                    AVERAGE_CADENCE_MEASUREMENT,
                                                    AVERAGE_SPEED_MEASUREMENT))

        for pageMeasurement in self.listedPageMeasurements:
            self.ui_antPanel.pageMeasurements.addItem(pageMeasurement)
