"""
    CopyRight: Liszthral
    Email: 2239288228@qq.com
    Project: ScholarHub
    Version: Alpha 1.0.0
    UpdateTime: 2025-1221-2239
"""
from PyQt6.QtCore import QThread
# import pyttsx3 as speaker
# from docx import Document

from PyQt6.QtWidgets import QApplication
from WindowsUI import MainWindow, EngSettingsWindow
from Utils import JsonReader, Logger
import sys, os, threading

TEMP = {"MAIN_PATH": os.path.dirname(os.path.realpath(__file__)) + "\\"}

class ProcessManager:
    _lock = threading.Lock()
    _instance = None
    _mutex = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._mutex:
                if cls._instance is None:
                    cls._instance = super(ProcessManager, cls).__new__(cls)
        return cls._instance

    def __copy__(self):
        return self

    def __deepcopy__(self, memo):
        memo[id(self)] = self
        return self

    def __init__(self):
        pass




def ExitProgram():

    MainConfig.save()
    logger.info("Exiting Program Normal")
    logger.save_log()


if __name__ == '__main__':

    logger = Logger.Logger(TEMP["MAIN_PATH"] + r"log\log.log")
    logger.info("Started Initialization")
    MainConfig = JsonReader.JsonReader(TEMP["MAIN_PATH"] + r"Configuration\MainConfig.json", logger)

    app = QApplication(sys.argv)
    app.aboutToQuit.connect(ExitProgram)
    TEMP["ScreenSize"] = app.primaryScreen().geometry().getRect()[2:]

    ProcessManager = ProcessManager()



    MainWindow = MainWindow.MainWindow(MainConfig, logger, TEMP)
    for i in range(18):
        MainWindow.AddFuncButton(f"TEST{i}", lambda: EngSettingsWindow.EngSettingsWindow())


    # Window.setWindowFlags(Qt.WindowType.FramelessWindowHint)
    # ui = uic.loadUi("untitled.ui")
    # ui.show()


    logger.info("Started Successfully")

    sys.exit(app.exec())
