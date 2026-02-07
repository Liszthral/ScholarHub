"""
    CopyRight: Liszthral
    Email: 2239288228@qq.com
    Project: ScholarHub - UI - TeachingAIDSWindow
    Version: Alpha 1.0.0
    UpdateTime: 2026-0110-1850
"""
import os.path
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QMessageBox, QTreeWidget, QTreeWidgetItem
from main import MAIN_PATH


class TeachingAIDSWindow(QWidget):

    index = 9
    name = 'TeachingAIDSWindow'

    def __init__(self, UI=None):
        super().__init__()
        self.UI = UI
        self.setObjectName("TeachingAIDSWindow")
        self.Layout = QVBoxLayout()
        self.setLayout(self.Layout)
        self.initUI()
        self.Layout.addStretch()

    def initUI(self):
        """ <1> Top information bar. """
        self.Layout.addWidget(self.UI.turnWidgetButton('HomeWindow'))
        """ <2> Iterate and render classification based on the corresponding directory. """
        self.renderDirTree()

    def renderDirTree(self):
        self.TopDirTree = QTreeWidget()
        self.TopDirTree.setHeaderLabel('选择呈式的项目')
        for path in os.listdir('./TeachingAIDS'):
            ParentItem = QTreeWidgetItem(self.TopDirTree, [path])
            data = os.listdir(MAIN_PATH / './TeachingAIDS' / path)
            for filename in data:
                filename = filename[:-4]
                QTreeWidgetItem(ParentItem, [filename])
        self.TopDirTree.itemDoubleClicked.connect(self.turnShow)
        self.TopDirTree.expandAll()
        self.Layout.addWidget(self.TopDirTree)

    def turnShow(self, item):
        result = self.judgeLayer(item)
        if result:
            path = MAIN_PATH / './TeachingAIDS' / result[0] / f'{result[1]}.csv'

            page = ShowAIDSInfo(path, self.UI)
            page.index = self.UI.registerStack(page)

        else:
            msg = f"<{item.text(0)}> 是顶层分类，不支持直接操作"
            QMessageBox.information(self, f"ScholarHub - {self.name}", msg)

    def judgeLayer(self, item):
        if item.parent() is None:
            return False
        else:
            ParentText = item.parent().text(0)
            ItemText = item.text(0)
            return ParentText, ItemText


class ShowAIDSInfo(QWidget):

    index = None
    name = None

    def __init__(self, path, UI=None):
        super().__init__()
        self.UI = UI
        self.setObjectName("ShowAIDSInfo")
        self.Layout = QHBoxLayout()
        self.setLayout(self.Layout)


        self.initUI()
        self.readerCSV(path)


    def initUI(self):
        """ <1> Top information bar. """

        pass

        # self.UI.toPage(self.UI.getHomeButton(TeachingAIDSWindow.index))
        # self.Layout.addWidget()

    def readerCSV(self, path):
        pass




