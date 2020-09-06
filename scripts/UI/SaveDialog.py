from PyQt5.QtWidgets import QFileDialog


"""
Widget used to save files. When called, a dialog box pops up.
"""
class SaveDialog(QFileDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

        self.options = self.Options()
        self.options |= self.DontUseNativeDialog

    def initUI(self):
        self.setWindowTitle('File Dialog')
        self.setGeometry(10, 10, 640, 480)  # left, top, width, height
