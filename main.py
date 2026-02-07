"""
    CopyRight: Liszthral
    Email: 2239288228@qq.com
    Project: ScholarHub
    Version: Alpha 1.0.0
    UpdateTime: 2025-1221-2239
"""
# from PyQt6.QtCore import QThread
# import pyttsx3 as speaker
# from docx import Document

from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QWidget, QVBoxLayout, QPushButton
from Utils import JsonReader, Logger
from PyQt6.QtGui import QIcon
from pathlib import Path
import sys, os, threading
from WindowsUI import (HomeWindow, SettingsWindow, TaskWindow, BufferWindow, DeviceMgrWindow, FocusWindow,
    GradeRecordWindow, VocabularyWindow, PoemWindow, TeachingAIDSWindow, PaperMgrWindow,
    LadderWindow, AchievementWindow, MusicWindow, PitchWindow, MusicalityWindow,
    AlarmWindow, FileProtectWindow)


MAIN_PATH = Path(__file__).resolve().parent

class UI(QMainWindow):

    stackCount = 0
    UIObject = []
    StackWidgets = {}

    def __init__(self):
        super().__init__()
        self.initUI()
        self.loadQSS(MAIN_PATH / mainCfg.get('ProgramInformation', 'QssFile'))

    def initUI(self):
        """ <1> Basic window construction information. """
        self.setObjectName('MainWindow')
        self.setWindowTitle(mainCfg.get('ProgramInformation', 'Name'))
        IconPath = str(MAIN_PATH / mainCfg.get('ProgramInformation', 'IconPath'))
        if os.path.exists(IconPath):
            self.setWindowIcon(QIcon(IconPath))
        else:
            logger.error("Not exist the program icon path.")
        self.resize(900, 600)
        """ <2> Create CentralWidget and Layout Pattern. """
        CentralWidget = QWidget()
        self.setCentralWidget(CentralWidget)
        MainLayout = QVBoxLayout(CentralWidget)
        MainLayout.setContentsMargins(0, 0, 0, 0)
        """ <3> Create StackWidget. """
        self.StackWidget = QStackedWidget()
        MainLayout.addWidget(self.StackWidget)
        """ <4> Create all window and add into StackWidget by index, connect the signal. """
        self.createWindow()
        self.addIntoStackWidget()
        self.connectSignals()

    def createWindow(self):
        """ <4.1> Create all window. """
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
        """ Add into UI.ObjectList """
        self.UIObject = [
            self.SettingsWindow, self.TaskWindow, self.BufferWindow, self.DeviceMgrWindow,
            self.FocusWindow, self.GradeRecordWindow, self.VocabularyWindow, self.PoemWindow,
            self.TeachingAIDSWindow, self.PaperMgrWindow, self.LadderWindow, self.AchievementWindow,
            self.MusicWindow, self.PitchWindow, self.MusicalityWindow, self.AlarmWindow, self.FileProtectWindow
        ]
        # The <HomeWindow> be created last, Otherwise it will not have the <self.UIObject> attribute.
        self.HomeWindow = HomeWindow.HomeWindow(self)

    def addIntoStackWidget(self):
        """ <4.2> Add all window into StackWidget and allot index. """
        self.registerStack(self.HomeWindow)
        for obj in self.UIObject:
            self.registerStack(obj)

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

    def registerStack(self, obj):
        self.StackWidget.addWidget(obj)
        self.StackWidgets[obj.name] = self.stackCount
        self.stackCount += 1
        return self.stackCount - 1

    def getStackIndex(self, name):
        return self.StackWidgets.get(name, 0)

    def toPage(self, index):
        index = int(index)
        if 0 <= index < self.StackWidget.count():
            try:
                self.StackWidget.setCurrentIndex(index)
                logger.info(f"Turn to window <{self.UIObject[index - 1].name}> Successfully.")
            except:  # NOQA
                logger.warning(f"Turn to window {self.UIObject[index - 1]} Successfully, but not has <object.name>.")
        else:
            self.toHomePage()
            logger.error(f"Not Found the window index at {index}.")

    def toHomePage(self):
        self.StackWidget.setCurrentIndex(self.getStackIndex('HomeWindow'))
        logger.info("Back to <HomeWindow> Successfully.")

    def turnWidgetButton(self, name) -> QPushButton:
        PushButton = QPushButton()
        PushButton.setText('返回')
        PushButton.setMaximumWidth(50)
        PushButton.setMinimumHeight(50)
        PushButton.setObjectName("turnWidgetButton")
        PushButton.clicked.connect(lambda: self.toPage(self.getStackIndex(name)))
        return PushButton

    def loadFont(self, path):
        pass

    def loadQSS(self, path):
        """:param path: Need to input absolute path."""
        try:
            with open(path, "r", encoding="utf-8") as f:
                logger.info(f"Loading QSS at <{path}>.")
                content = f.read()
                self.setStyleSheet(content)
                logger.info("Load QSS Successfully.")
        except FileNotFoundError:
            logger.error(f"Not found QSS file : <{path}>.")
        except Exception as e:
            logger.error(f"QSS load error : <{e}>.")


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
    mainCfg.save()
    logger.info("Exiting Program Normal.")
    logger.save_log()


if __name__ == '__main__':
    logger = Logger.Logger(MAIN_PATH / r"log/log.log")
    logger.info("Started Initialization.")

    mainCfg = JsonReader.JsonReader(MAIN_PATH / r"Configuration/MainConfig.json", logger)

    app = QApplication(sys.argv)
    app.aboutToQuit.connect(ExitProgram)

    process_manager = ProcessManager()

    window = UI()
    window.showMaximized()

    logger.info("Started Successfully.")
    sys.exit(app.exec())
