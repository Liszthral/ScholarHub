"""
    CopyRight: Liszthral
    Email: 2239288228@qq.com
    Project: ScholarHub
    Version: Alpha 1.0.0
    UpdateTime: 2025-1221-2239
"""

# import pyttsx3 as speaker
# from docx import Document
# import logger as log

from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtGui import QIcon
import sys
import json



class Configuration:

    def __init__(self):
        try:
            with open("Configuration/MainConfig.json", 'r', encoding='utf-8-sig') as f:
                self.config = json.load(f)
        except FileNotFoundError:  # 少了log
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
        with open("Configuration/MainConfig.json", 'w', encoding='utf-8-sig') as f:
            json.dump(self.config, f, ensure_ascii=False, indent=4)


def ExitProgram():
    Configuration.save()




if __name__ == '__main__':

    Configuration = Configuration()

    app = QApplication(sys.argv)
    app.aboutToQuit.connect(ExitProgram)

    Window = QWidget()
    Window.setWindowTitle(Configuration.get("ProgramInformation", "Name"))
    Window.resize(800, 600)
    Window.setWindowIcon(QIcon(Configuration.get("ProgramInformation", "IconPath")))
    Window.show()
    Window.show()

    sys.exit(app.exec())





