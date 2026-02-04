from uiBIAWEB.BIAWEB import Ui_MainWindow


class BIAWEBEx(Ui_MainWindow):
    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow=MainWindow
    def showWindow(self):
        self.MainWindow.show()