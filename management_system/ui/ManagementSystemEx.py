from management_system.ui.ManagementSystem import Ui_MainWindow

class ManagementSystemEx(Ui_MainWindow):
    def __init__(self):
        super().__init__()
    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow
    def show(self):
        self.MainWindow.show()