import sys
import os
import json
import pandas as pd

from matplotlib import pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar

from PyQt6.QtWidgets import QMainWindow

from Final_Report.ui.Statistics.StatisticsMainWindow import Ui_StatisticsWindow


def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)

    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(current_dir, "..", ".."))

    return os.path.join(project_root, relative_path.replace("Final_Report/", ""))

def get_data_path(filename):
    base = resource_path("Final_Report/PawsResQ")
    os.makedirs(base, exist_ok=True)
    return os.path.join(base, filename)


def ensure_file(filename):
    data_path = get_data_path(filename)

    if not os.path.exists(data_path):
        source = resource_path(f"Final_Report/datasets/{filename}")

        if os.path.exists(source):
            import shutil
            shutil.copy(source, data_path)
        else:
            with open(data_path, "w", encoding="utf-8") as f:
                json.dump({}, f)

    return data_path

class StatisticsMainWindowEx(QMainWindow, Ui_StatisticsWindow):

    def __init__(self):
        super().__init__()

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)

        self.MainWindow = MainWindow

        self.setupPlot()

        self.pushButtonBack.clicked.connect(self.go_back)

        self.showLinePlotChart()

        self.MainWindow.setStyleSheet("""
        QPushButton {
            background-color: #2e7d32;
            color: white;
            padding: 10px;
            border-radius: 8px;
        }
        QPushButton#pushButtonBack {
            background-color: #c62828;
        }
        """)

    def setupPlot(self):

        self.figure = plt.figure()

        self.canvas = FigureCanvas(self.figure)

        self.toolbar = NavigationToolbar(self.canvas, self.MainWindow)

        self.verticalLayout.addWidget(self.toolbar)
        self.verticalLayout.addWidget(self.canvas)

    def loadData(self):
        pets_path = ensure_file("pets.json")
        adopters_path = ensure_file("adopters.json")

        with open(pets_path, "r", encoding="utf-8") as f:
            pets_data = json.load(f)

        pets = pd.DataFrame(pets_data["pets"])

        with open(adopters_path, "r", encoding="utf-8") as f:
            adopters_data = json.load(f)

        adopters = pd.DataFrame(adopters_data["adopters"])

        pets["rescue_date"] = pd.to_datetime(pets["rescue_date"])
        pets["Year"] = pets["rescue_date"].dt.year

        adopters["adopted_date"] = pd.to_datetime(adopters["adopted_date"])
        adopters["Year"] = adopters["adopted_date"].dt.year

        rescued = pets.groupby("Year").size().reset_index(name="Rescued")
        adopted = adopters.groupby("Year").size().reset_index(name="Adopted")

        df = pd.merge(rescued, adopted, on="Year", how="outer").fillna(0)

        return df

    def showLinePlotChart(self):

        df = self.loadData()

        df["Year"] = df["Year"].astype(int)

        self.figure.clear()

        ax = self.figure.add_subplot(111)

        ax.grid()

        ax.plot(df["Year"], df["Rescued"],
                marker='o', linestyle='-', color='orange', label='Rescued')

        ax.plot(df["Year"], df["Adopted"],
                marker='o', linestyle='-', color='blue', label='Adopted')

        ax.set_xticks(df["Year"])
        ax.set_xlabel("Year")
        ax.set_ylabel("Number")
        ax.set_title("Annual Rescued vs Adopted Pets")

        ax.legend()

        self.canvas.draw()

    def go_back(self):

        if hasattr(self, 'previous_window') and self.previous_window:
            self.previous_window.show()

        self.MainWindow.close()