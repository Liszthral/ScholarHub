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
        with open("Configuration/MainConfig.json", 'r', encoding='utf-8-sig') as f:
            self.config = json.load(f)

    def get(self, kind, *args):
        result = self.config.get(kind)
        for arg in args:
            if (isinstance(result, dict)) and (arg in result):
                result = result[arg]
            else:
                return None
        return result





if __name__ == '__main__':

    Configuration = Configuration()
    print(Configuration.get('ProgramInformation', 'Version'))


    app = QApplication(sys.argv)

    Window = QWidget()
    Window.setWindowTitle('StudyHub - Liszthral')
    Window.resize(800, 600)
    Window.setWindowIcon(QIcon('MediaFile/Icon/StudyHub.ico'))
    Window.show()
    Window.show()

    sys.exit(app.exec())





