from ui.ManagementSystem.ManagementSystemMainWindow import Ui_MainWindow

class ManagementSystemMainWindowEx(Ui_MainWindow):
    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow=MainWindow
    def showWindow(self):
        self.MainWindow.show()

