from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal


class ScanWorker(QObject):
    devicesFound = pyqtSignal(object)

    def __init__(self, antDriver):
        super().__init__()

        self.antDriver = antDriver

    @pyqtSlot()
    def scan(self):
        self.antDriver.scan(self.devicesCallback)

    def devicesCallback(self, devices):
        self.devicesFound.emit(devices)


class ListenWorker(QObject):
    messageReceived = pyqtSignal(object)

    def __init__(self, antDriver):
        super().__init__()

        self.antDriver = antDriver

    @pyqtSlot()
    def listen(self):
        self.antDriver.listen(self.messageCallback)

    def messageCallback(self, msg):
        self.messageReceived.emit(msg)
