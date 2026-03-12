from PyQt6.QtWidgets import QApplication, QMainWindow

from Final_Report.ui.UserSystemMainWindow.UserSystemMainWindowEx import MainWindowInterfaceEx

app=QApplication([])
gui=MainWindowInterfaceEx()
gui.setupUi(QMainWindow())
gui.showWindow()
app.exec()