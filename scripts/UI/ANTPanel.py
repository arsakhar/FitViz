from PyQt5.QtWidgets import QFrame, QVBoxLayout, QWidget, QLabel, QGridLayout, QHBoxLayout
from PyQt5.QtWidgets import QComboBox, QListView, QListWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


"""
Widget that displays view panels
"""
class ANTPanel(QWidget):
    ALIGN_VERTICAL = 0
    ALIGN_HORIZONTAL = 1
    ALIGN_GRID = 2

    LIST_BOX = 0
    COMBO_BOX = 1

    def __init__(self, parent, alignment=ALIGN_VERTICAL, devicesStyle=COMBO_BOX):

        super().__init__(parent)

        self.alignment = alignment

        self.devicesStyle = devicesStyle

        self.initUI()

    def initUI(self):
        self.centralFrame = QFrame(self)
        self.centralFrame.setFrameShape(QFrame.NoFrame)
        self.centralFrame.setFrameShadow(QFrame.Raised)
        self.centralFrame.setContentsMargins(0, 0, 0, 0)
        self.centralFrame.setStyleSheet("border: none;")

        self.devicesFrame = QFrame(self.centralFrame)
        self.devicesFrame.setFrameShape(QFrame.NoFrame)
        self.devicesFrame.setFrameShadow(QFrame.Raised)
        self.devicesFrame.setContentsMargins(0, 0, 0, 0)
        self.devicesFrame.setStyleSheet("border: none;")

        if self.devicesStyle == self.COMBO_BOX:
            self.devices = ComboBox(self.devicesFrame)
        else:
            self.devices = ListBox(self.devicesFrame)

        self.devicesLabel = Label(self.devicesFrame)
        self.devicesLabel.setText("Devices")

        self.devicesLayout = QVBoxLayout(self.devicesFrame)
        self.devicesLayout.addWidget(self.devicesLabel)
        self.devicesLayout.addWidget(self.devices)
        self.devicesLayout.setContentsMargins(0, 0, 0, 0)
        self.devicesLayout.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        self.profilesFrame = QFrame(self.centralFrame)
        self.profilesFrame.setFrameShape(QFrame.NoFrame)
        self.profilesFrame.setFrameShadow(QFrame.Raised)
        self.profilesFrame.setContentsMargins(0, 0, 0, 0)
        self.profilesFrame.setStyleSheet("border: none;")

        self.profiles = ListBox(self.profilesFrame)

        self.profilesLabel = Label(self.profilesFrame)
        self.profilesLabel.setText("Profiles")

        self.profilesLayout = QVBoxLayout(self.profilesFrame)
        self.profilesLayout.addWidget(self.profilesLabel)
        self.profilesLayout.addWidget(self.profiles)
        self.profilesLayout.setContentsMargins(0, 0, 0, 0)
        self.profilesLayout.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        self.dataPagesFrame = QFrame(self.centralFrame)
        self.dataPagesFrame.setFrameShape(QFrame.NoFrame)
        self.dataPagesFrame.setFrameShadow(QFrame.Raised)
        self.dataPagesFrame.setContentsMargins(0, 0, 0, 0)
        self.dataPagesFrame.setStyleSheet("border: none;")

        self.dataPages = ListBox(self.dataPagesFrame)

        self.dataPagesLabel = Label(self.dataPagesFrame)
        self.dataPagesLabel.setText("Data Pages")

        self.dataPagesLayout = QVBoxLayout(self.dataPagesFrame)
        self.dataPagesLayout.addWidget(self.dataPagesLabel)
        self.dataPagesLayout.addWidget(self.dataPages)
        self.dataPagesLayout.setContentsMargins(0, 0, 0, 0)
        self.dataPagesLayout.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        self.pageMeasurementsFrame = QFrame(self.centralFrame)
        self.pageMeasurementsFrame.setFrameShape(QFrame.NoFrame)
        self.pageMeasurementsFrame.setFrameShadow(QFrame.Raised)
        self.pageMeasurementsFrame.setContentsMargins(0, 0, 0, 0)
        self.pageMeasurementsFrame.setStyleSheet("border: none;")

        self.pageMeasurements = ListBox(self.pageMeasurementsFrame)

        self.pageMeasurementsLabel = Label(self.pageMeasurementsFrame)
        self.pageMeasurementsLabel.setText("Page Measurements")

        self.pageMeasurementsLayout = QVBoxLayout(self.pageMeasurementsFrame)
        self.pageMeasurementsLayout.addWidget(self.pageMeasurementsLabel)
        self.pageMeasurementsLayout.addWidget(self.pageMeasurements)
        self.pageMeasurementsLayout.setContentsMargins(0, 0, 0, 0)
        self.pageMeasurementsLayout.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        if self.alignment == self.ALIGN_GRID:
            self.centralLayout = QGridLayout(self.centralFrame)
            self.centralLayout.addWidget(self.devicesFrame, 1, 1)
            self.centralLayout.addWidget(self.profilesFrame, 1, 2)
            self.centralLayout.addWidget(self.dataPagesFrame, 2, 1)
            self.centralLayout.addWidget(self.pageMeasurementsFrame, 2, 2)

        else:
            if self.alignment == self.ALIGN_VERTICAL:
                self.centralLayout = QVBoxLayout(self.centralFrame)
            else:
                self.centralLayout = QHBoxLayout(self.centralFrame)

            self.centralLayout.addWidget(self.devicesFrame)
            self.centralLayout.addWidget(self.profilesFrame)
            self.centralLayout.addWidget(self.dataPagesFrame)
            self.centralLayout.addWidget(self.pageMeasurementsFrame)
            self.centralLayout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(self.centralLayout)


"""
Widget to create combobox (unused)
"""
class ComboBox(QComboBox):
    def __init__(self, parent):
        super().__init__(parent)

        self.initUI()

    def initUI(self):
        view = ListView(self)

        self.setView(view)

        self.setMinimumSize(200, 20)

        self.setStyleSheet(
            "background-color: rgb(27, 29, 35);"
            "border: 1px solid gray;"
            "border-radius: 5px;"
        )

        self.addItem("")

    def clear(self):
        super().clear()

        self.addItem("")


"""
Widget to create combobox list view (unused)
"""
class ListView(QListView):
    def __init__(self, parent):
        super().__init__(parent)

        self.initUI()

    def initUI(self):
        self.setMinimumSize(200, 20)
        self.setStyleSheet("QListView::item:hover {"
                           "background-color: rgb(85, 170, 255); }"
                           )


"""
Widget to create listbox
"""
class ListBox(QListWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.initUI()

    def initUI(self):
        self.setMinimumSize(200, 50)

        self.setStyleSheet(
            "background-color: rgb(27, 29, 35);"
            "border: 1px solid gray;"
            "border-radius: 5px;"
        )


"""
Widget to create label
"""
class Label(QLabel):
    def __init__(self, parent):
        super().__init__(parent)

        self.initUI()

    def initUI(self):
        font = QFont()
        font.setBold(True)
        font.setPointSize(10)
        self.setFont(font)

