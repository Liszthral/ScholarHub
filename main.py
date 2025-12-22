"""
    CopyRight: Liszthral
    Email: 2239288228@qq.com
    Project: ScholarHub
    Version: Alpha 1.0.0
    UpdateTime: 2025-1221-2239
"""

# import pyttsx3 as speaker
# from docx import Document

from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtGui import QIcon
import sys
import json
import os
import time

MAIN_PATH = os.path.dirname(os.path.realpath(__file__)) + "\\"

class Configuration:

    def __init__(self, path):
        try:
            self.path = path
            with open(f"{self.path}", 'r', encoding='utf-8-sig') as f:
                self.config = json.load(f)
        except FileNotFoundError:
            logger.error("Not found file -> MainConfig.json")
            self.config = {}

    def get(self, kind, *args):
        # 完全保留你原始的get逻辑，无修改
        result = self.config.get(kind)
        for arg in args:
            if (isinstance(result, dict)) and (arg in result):
                result = result[arg]
            else:
                return None
        return result

    def configuration(self, kind, aim, *args):
        if kind not in self.config:
            return None
        parent = self.config[kind]
        if len(args) == 0:
            self.config[kind] = aim
            return True
        for arg in args[:-1]:
            if (isinstance(parent, dict)) and (arg in parent):
                parent = parent[arg]
            else:
                return None
        target = args[-1]
        if isinstance(parent, dict):
            parent[target] = aim
            return True
        else:
            return None

    def save(self):
        with open(f"{self.path}", 'w', encoding='utf-8-sig') as f:
            json.dump(self.config, f, ensure_ascii=False, indent=4)

class Logger:

    LogTemp = """"""

    def __init__(self, APath):
        """
        :param APath: The absolute path of the program whose logs are being recorded.
        """
        if not os.path.exists(APath):
            os.makedirs(APath)
        self.APath = APath

    def reset(self, path):
        if not os.path.exists(path):
            os.makedirs(path)
        self.APath = path

    def info(self, msg):
        content = self.get_time() + " [INFO] " + str(msg) + "\n"
        self.LogTemp += content

    def error(self, msg):
        content = self.get_time() + " [ERROR] " + str(msg) + "\n"
        self.LogTemp += content

    def warning(self, msg):
        content = self.get_time() + " [WARNING] " + str(msg) + "\n"
        self.LogTemp += content

    def critical(self, msg):
        content = self.get_time() + " [CRITICAL] " + str(msg) + "\n"
        self.LogTemp += content

    def save_log(self):
        with open(self.APath, "a+", encoding="utf-8") as f:
            for i in self.LogTemp.split("\n"):
                f.write(i + "\n")

    @staticmethod
    def get_time():
        RecordTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        return RecordTime


def ExitProgram():

    Configuration.save()

    logger.info("Exiting Program Normal")
    logger.save_log()




if __name__ == '__main__':

    logger = Logger(MAIN_PATH + r"Configuration\log\log.log")

    Configuration = Configuration(MAIN_PATH + r"Configuration\MainConfig.json")

    app = QApplication(sys.argv)
    app.aboutToQuit.connect(ExitProgram)

    Window = QWidget()
    Window.setWindowTitle(Configuration.get("ProgramInformation", "Name"))
    Window.resize(800, 600)
    Window.setWindowIcon(QIcon(Configuration.get("ProgramInformation", "IconPath")))
    Window.show()
    Window.show()

    logger.info("Started Successfully")

    sys.exit(app.exec())





