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

from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QWidget, QVBoxLayout, QPushButton
from Utils import JsonReader, Logger
import sys, os, threading
from WindowsUI import (HomeWindow, SettingsWindow, TaskWindow, BufferWindow, DeviceMgrWindow, FocusWindow,
    GradeRecordWindow, VocabularyWindow, PoemWindow, TeachingAIDSWindow, PaperMgrWindow,
    LadderWindow, AchievementWindow, MusicWindow, PitchWindow, MusicalityWindow,
    AlarmWindow, FileProtectWindow)


TEMP = {"MAIN_PATH": os.path.dirname(os.path.realpath(__file__)) + "\\"}

class UI(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        """ <1> Basic window construction information. """
        self.setObjectName("MainWindow")
        self.setWindowTitle("ScholarHub")
        self.resize(900, 600)
        """ <2> Create CentralWidget and Layout Pattern. """
        CentralWidget = QWidget()
        self.setCentralWidget(CentralWidget)
        main_layout = QVBoxLayout(CentralWidget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        """ <3> Create StackWidget. """
        self.StackWidget = QStackedWidget()
        main_layout.addWidget(self.StackWidget)
        """ <4> Create all window and add into StackWidget by index, connect the signal. """
        self.createWindow()
        self.addIntoStackWidget()
        self.connectSignals()

    def createWindow(self):
        """ <4.1> Create all window. """
        self.HomeWindow = HomeWindow.HomeWindow()
        self.SettingsWindow = SettingsWindow.SettingsWindow(self)
        self.TaskWindow = TaskWindow.TaskWindow(self)
        self.BufferWindow = BufferWindow.BufferWindow(self)
        self.DeviceMgrWindow = DeviceMgrWindow.DeviceMgrWindow(self)
        self.FocusWindow = FocusWindow.FocusWindow(self)
        self.GradeRecordWindow = GradeRecordWindow.GradeRecordWindow(self)
        self.VocabularyWindow = VocabularyWindow.VocabularyWindow(self)
        self.PoemWindow = PoemWindow.PoemWindow(self)
        self.TeachingAIDSWindow = TeachingAIDSWindow.TeachingAIDSWindow(self)
        self.PaperMgrWindow = PaperMgrWindow.PaperMgrWindow(self)
        self.LadderWindow = LadderWindow.LadderWindow(self)
        self.AchievementWindow = AchievementWindow.AchievementWindow(self)
        self.MusicWindow = MusicWindow.MusicWindow(self)
        self.PitchWindow = PitchWindow.PitchWindow(self)
        self.MusicalityWindow = MusicalityWindow.MusicalityWindow(self)
        self.AlarmWindow = AlarmWindow.AlarmWindow(self)
        self.FileProtectWindow = FileProtectWindow.FileProtectWindow(self)

    def addIntoStackWidget(self):
        """ <4.2> Add all window into StackWidget and allot index. """
        self.StackWidget.addWidget(self.HomeWindow)         # HomeWindow.index =         00
        self.StackWidget.addWidget(self.SettingsWindow)     # SettingsWindow.index =     01
        self.StackWidget.addWidget(self.TaskWindow)         # TaskWindow.index =         02
        self.StackWidget.addWidget(self.BufferWindow)       # BufferWindow.index =       03
        self.StackWidget.addWidget(self.DeviceMgrWindow)    # DeviceMgrWindow.index =    04
        self.StackWidget.addWidget(self.FocusWindow)        # FocusWindow.index =        05
        self.StackWidget.addWidget(self.GradeRecordWindow)  # GradeRecordWindow.index =  06
        self.StackWidget.addWidget(self.VocabularyWindow)   # VocabularyWindow.index =   07
        self.StackWidget.addWidget(self.PoemWindow)         # PoemWindow.index =         08
        self.StackWidget.addWidget(self.TeachingAIDSWindow) # TeachingAIDSWindow.index = 09
        self.StackWidget.addWidget(self.PaperMgrWindow)     # PaperMgrWindow.index =     10
        self.StackWidget.addWidget(self.LadderWindow)       # LadderWindow.index =       11
        self.StackWidget.addWidget(self.AchievementWindow)  # AchievementWindow.index =  12
        self.StackWidget.addWidget(self.MusicWindow)        # MusicWindow.index =        13
        self.StackWidget.addWidget(self.PitchWindow)        # PitchWindow.index =        14
        self.StackWidget.addWidget(self.MusicalityWindow)   # MusicalityWindow.index =   15
        self.StackWidget.addWidget(self.AlarmWindow)        # AlarmWindow.index =        16
        self.StackWidget.addWidget(self.FileProtectWindow)  # FileProtectWindow.index =  17

        #
        # self.StackWidget.addWidget(self.HomeWindow)
        # self.StackWidget.addWidget(self.VocabularyWindow)  # EngSetWindow.index = 1
        # self.StackWidget.addWidget(self.AlarmWindow)  # AlarmWindow.index = 2

    def connectSignals(self):
        """ <4.3> Connect signal. """
        self.HomeWindow.gotoSettingsW.connect(lambda: self.toPage(1))
        self.HomeWindow.gotoTaskW.connect(lambda: self.toPage(2))
        self.HomeWindow.gotoBufferW.connect(lambda: self.toPage(3))
        self.HomeWindow.gotoDeviceMgrW.connect(lambda: self.toPage(4))
        self.HomeWindow.gotoFocusW.connect(lambda: self.toPage(5))
        self.HomeWindow.gotoGradeRecordW.connect(lambda: self.toPage(6))
        self.HomeWindow.gotoVocabularyW.connect(lambda: self.toPage(7))
        self.HomeWindow.gotoPoemW.connect(lambda: self.toPage(8))
        self.HomeWindow.gotoTeachingAIDSW.connect(lambda: self.toPage(9))
        self.HomeWindow.gotoPaperMgrW.connect(lambda: self.toPage(10))
        self.HomeWindow.gotoLadderW.connect(lambda: self.toPage(11))
        self.HomeWindow.gotoAchievementW.connect(lambda: self.toPage(12))
        self.HomeWindow.gotoMusicW.connect(lambda: self.toPage(13))
        self.HomeWindow.gotoPitchW.connect(lambda: self.toPage(14))
        self.HomeWindow.gotoMusicalityW.connect(lambda: self.toPage(15))
        self.HomeWindow.gotoAlarmW.connect(lambda: self.toPage(16))
        self.HomeWindow.gotoFileProtectW.connect(lambda: self.toPage(17))


        # self.HomeWindow.gotoGradeRecordW.connect(lambda: self.toPage(1))
        # self.HomeWindow.gotoAlarmW.connect(lambda: self.toPage(2))




        """ <6> Show HomeWindow. """
        self.toPage(0)



    def toPage(self, index):
        index = int(index)
        if 0 <= index < self.StackWidget.count():
            self.StackWidget.setCurrentIndex(index)
            logger.info(f"Turn to page {index} Successfully.")
        else:
            self.StackWidget.setCurrentIndex(0)
            logger.error(f"Not Found the page index at {index}.")

    def toHomePage(self):
        self.toPage(0)


    def turnPageButton(self, toIndex) -> QPushButton:
        PushButton = QPushButton()

        return PushButton


    def loadQSS(self, path):
        """:param path: Need to input absolute path."""
        try:
            with open(path, "r", encoding="utf-8") as f:
                logger.info(f"Start loading QSS at {path}.")
                content = f.read()
                self.setStyleSheet(content)
                logger.info("Load QSS Successfully.")
        except FileNotFoundError:
            logger.error(f"Not found QSS file : {path}.")


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
    logger.info("Started Initialization.")

    MainConfig = JsonReader.JsonReader(TEMP["MAIN_PATH"] + r"Configuration\MainConfig.json", logger)

    app = QApplication(sys.argv)
    app.aboutToQuit.connect(ExitProgram)

    process_manager = ProcessManager()

    window = UI()
    window.showMaximized()

    logger.info("Started Successfully.")
    sys.exit(app.exec())
