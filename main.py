"""
    CopyRight: Liszthral
    Email: 2239288228@qq.com
    Project: ScholarHub
    Version: Alpha 1.0.0
    UpdateTime: 2025-1221-2239
"""

# import pyttsx3 as speaker
# from docx import Document

from PyQt6.QtWidgets import QApplication
from WindowsUI import MainWindow
from Utils import JsonReader, Logger
import sys, os

MAIN_PATH = os.path.dirname(os.path.realpath(__file__)) + "\\"






def ExitProgram():

    MainConfig.save()
    logger.info("Exiting Program Normal")
    logger.save_log()


if __name__ == '__main__':

    logger = Logger.Logger(MAIN_PATH + r"log\log.log")
    MainConfig = JsonReader.JsonReader(MAIN_PATH + r"Configuration\MainConfig.json", logger)

    app = QApplication(sys.argv)
    app.aboutToQuit.connect(ExitProgram)

    MainWindow = MainWindow.MainWindow(MainConfig)

    # Window.setWindowFlags(Qt.WindowType.FramelessWindowHint)
    # ui = uic.loadUi("untitled.ui")
    # ui.show()


    logger.info("Started Successfully")

    sys.exit(app.exec())
