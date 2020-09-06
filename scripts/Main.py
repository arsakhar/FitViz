from scripts.UI.Application import Application
from scripts.UI.MainWindow import MainWindow
from scripts.UIControllers.UIController import UIController

import sys

class FitViz():
    def __init__(self):
        pass

    def run(self):
        self.app = Application(sys)
        self.ui_main = MainWindow(self.app)

        self.ui_controller = UIController(self.ui_main)

        sys.exit(self.app.exec_())

if __name__ == '__main__':
    FitViz().run()
