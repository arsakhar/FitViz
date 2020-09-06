from PyQt5.QtWidgets import QFrame, QHBoxLayout, QWidget, QStackedLayout, QVBoxLayout
from PyQt5.QtCore import Qt
from scripts.UI.AnalogGauge import AnalogGaugeWidget
from scripts.UI.ANTPanel import ANTPanel
from scripts.UI.LCDDisplay import LCDDisplay, LCDDisplayUnits


"""
Widget that displays view panels
"""
class ViewPanel(QWidget):
    GAUGE_READOUT = 0
    DIGITAL_READOUT = 1

    def __init__(self, parent):
        super().__init__()

        self.active = False

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
        self.antPanelFrame.setContentsMargins(10, 10, 10, 10)
        self.antPanelFrame.setStyleSheet("border: none;")

        self.antPanel = ANTPanel(self.antPanelFrame)

        self.antPanelLayout = QHBoxLayout(self.antPanelFrame)
        self.antPanelLayout.addWidget(self.antPanel)
        self.antPanelLayout.setContentsMargins(0, 0, 0, 0)

        self.readoutFrame = QFrame(self.contentFrame)
        self.readoutFrame.setFrameShape(QFrame.NoFrame)
        self.readoutFrame.setFrameShadow(QFrame.Raised)
        self.readoutFrame.setContentsMargins(10, 10, 10, 10)
        self.readoutFrame.setStyleSheet("border: none;")

        self.gaugeReadoutFrame = QFrame(self.readoutFrame)
        self.gaugeReadoutFrame.setFrameShape(QFrame.NoFrame)
        self.gaugeReadoutFrame.setFrameShadow(QFrame.Raised)
        self.gaugeReadoutFrame.setContentsMargins(0, 0, 0, 0)
        self.gaugeReadoutFrame.setStyleSheet("border: none;")

        self.gaugeReadout = AnalogGaugeWidget(self.gaugeReadoutFrame)

        self.gaugeReadoutLayout = QVBoxLayout(self.gaugeReadoutFrame)
        self.gaugeReadoutLayout.addWidget(self.gaugeReadout)
        self.gaugeReadoutLayout.setContentsMargins(0, 0, 0, 0)
        self.gaugeReadoutLayout.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        self.digitalReadoutFrame = QFrame(self.readoutFrame)
        self.digitalReadoutFrame.setFrameShape(QFrame.NoFrame)
        self.digitalReadoutFrame.setFrameShadow(QFrame.Raised)
        self.digitalReadoutFrame.setContentsMargins(0, 0, 0, 0)
        self.digitalReadoutFrame.setStyleSheet("border: none;")

        self.digitalReadout = LCDDisplay(self.digitalReadoutFrame)
        self.digitalReadoutUnits = LCDDisplayUnits(self.digitalReadoutFrame)
        self.digitalReadoutUnits.setAlignment(Qt.AlignHCenter | Qt.AlignBottom)

        self.digitalReadoutLayout = QHBoxLayout(self.digitalReadoutFrame)
        self.digitalReadoutLayout.addWidget(self.digitalReadout)
        self.digitalReadoutLayout.addWidget(self.digitalReadoutUnits, alignment=Qt.AlignBottom)
        self.digitalReadoutLayout.setContentsMargins(0, 0, 0, 0)
        self.digitalReadoutLayout.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        self.readoutLayout = QStackedLayout(self.readoutFrame)
        self.readoutLayout.addWidget(self.gaugeReadoutFrame)
        self.readoutLayout.addWidget(self.digitalReadoutFrame)
        self.readoutLayout.setContentsMargins(0, 0, 0, 0)

        self.contentLayout = QHBoxLayout(self.contentFrame)
        self.contentLayout.addWidget(self.antPanelFrame, stretch=1)
        self.contentLayout.addWidget(self.readoutFrame, stretch=3)
        self.contentLayout.setContentsMargins(0, 0, 0, 0)

        self.centralLayout = QHBoxLayout(self.centralFrame)
        self.centralLayout.addWidget(self.contentFrame)
        self.centralLayout.setContentsMargins(0, 0, 0, 0)

        self.uiLayout = QHBoxLayout(self)
        self.uiLayout.addWidget(self.centralFrame)
        self.uiLayout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(self.uiLayout)
        self.setContentsMargins(0, 0, 0, 0)
