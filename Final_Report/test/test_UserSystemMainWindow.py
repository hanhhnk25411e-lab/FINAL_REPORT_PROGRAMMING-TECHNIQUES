from PyQt6.QtWidgets import QApplication, QMainWindow

from Final_Report.ui.UserSystemMainWindow.UserSystemMainWindowEx import UserSystemMainWindowEx

app=QApplication([])
gui=UserSystemMainWindowEx()
gui.setupUi(QMainWindow())
gui.showWindow()
app.exec()
#