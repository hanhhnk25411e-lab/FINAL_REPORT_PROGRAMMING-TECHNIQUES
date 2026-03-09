from PyQt6.QtWidgets import QApplication, QMainWindow
from ui.WebPage.WebPageMainWindownEx import WebPageMainWindownEx

app=QApplication([])
gui=WebPageMainWindownEx()
gui.setupUi(QMainWindow())
gui.showWindow()
app.exec()