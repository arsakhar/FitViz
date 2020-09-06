from scripts.UIControllers.ANTPanelController import ANTPanelController
from scripts.UIControllers.UDPPanelController import UDPPanelController
from scripts.UIControllers.CSVPanelController import CSVPanelController


class WritePanelController:
    def __init__(self, ui_writePanel, ui_logPanel):
        self.ui_writePanel = ui_writePanel

        self.ui_logPanel = ui_logPanel

        self.ui_antPanel = self.ui_writePanel.antPanel
        self.antPanelController = ANTPanelController(self.ui_antPanel, self.ui_logPanel)

        self.ui_udpPanel = ui_writePanel.udpPanel
        self.udpPanelController = UDPPanelController(self.ui_udpPanel, self.ui_logPanel, self.antPanelController)

        self.ui_csvPanel = ui_writePanel.csvPanel
        self.csvPanelController = CSVPanelController(self.ui_csvPanel, self.ui_logPanel, self.antPanelController)

    def messageReceived(self, profileMessage):
        if profileMessage is None:
            return

        self.antPanelController.messageReceived(profileMessage)
        self.udpPanelController.messageReceived(profileMessage)
        self.csvPanelController.messageReceived(profileMessage)

    def clear(self):
        self.ui_antPanel.devices.clear()
        self.ui_antPanel.profiles.clear()
        self.ui_antPanel.dataPages.clear()
        self.ui_antPanel.pageMeasurements.clear()
        self.csvPanelController.clear()
        self.udpPanelController.clear()
        self.ui_writePanel.logPanel.clear()
