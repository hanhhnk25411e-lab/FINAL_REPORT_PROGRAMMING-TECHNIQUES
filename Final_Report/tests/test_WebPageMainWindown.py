import os
import sys

from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QFontDatabase

from Final_Report.ui.WebPage.WebPageMainWindowEx import WebPageMainWindowEx


def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def load_fonts():
    font_dir = resource_path("Final_Report/fonts")

    if not os.path.exists(font_dir):
        print("Font folder not found:", font_dir)
        return

    for file in os.listdir(font_dir):
        if file.endswith(".ttf") or file.endswith(".otf"):
            path = os.path.join(font_dir, file)
            font_id = QFontDatabase.addApplicationFont(path)

            if font_id != -1:
                families = QFontDatabase.applicationFontFamilies(font_id)
                print(f"{file} → {families}")
            else:
                print(f"load fail: {file}")

def main():
    os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "1"
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    os.environ["QT_SCALE_FACTOR"] = "1.5"

    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    load_fonts()
    window = WebPageMainWindowEx()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()