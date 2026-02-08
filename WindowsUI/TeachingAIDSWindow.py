"""
    CopyRight: Liszthral
    Email: 2239288228@qq.com
    Project: ScholarHub - UI - TeachingAIDSWindow
    Version: Alpha 1.0.0
    UpdateTime: 2026-0110-1850
"""

import csv
import os.path
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QMessageBox,
                             QTreeWidget, QTreeWidgetItem, QPushButton, QGridLayout, QComboBox, QHBoxLayout)
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
            data = os.listdir(MAIN_PATH / 'TeachingAIDS' / path)
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
            getIndex = self.UI.getStackIndex(f'{result[0]}-{result[1]}')
            print('getIndex:', getIndex)
            if getIndex == 0:  # This page cannot be found, index=0 corresponds to the <HomeWindow>
                page = ShowAIDSInfo(path, self.UI)
                page.name = str(f'{result[0]}-{result[1]}')
                index = self.UI.registerStack(page)
                page.index = index
                self.UI.UIObject.append(page)  # Important: It must be manually added to UIObject, otherwise the <UI.toPage> cannot find the corresponding index.
                self.UI.toPage(page.index)
                print('if', self.UI.UIObject)
            else:
                print('else', self.UI.UIObject)
                self.UI.toPage(getIndex)
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
    FieldNames = ['page', 'state', 'remark']
    States = ['finished', 'unfinished', 'processing', 'doubting']
    data = {}
    PageObj = []

    def __init__(self, path, UI=None):
        super().__init__()
        self.UI = UI
        self.path = path
        self.setObjectName("ShowAIDSInfo")
        self.Layout = QVBoxLayout()
        self.setLayout(self.Layout)

        self.initUI()
        self.readerCSV(self.path)
        self.renderButton()

    def initUI(self):
        """ <1> Top information bar. """
        TopBar = QHBoxLayout()
        TopBar.addWidget(self.UI.turnWidgetButton('TeachingAIDSWindow'))
        TopBar.addStretch()
        # Operation status switching bar
        self.StateSwitch = QComboBox()
        self.StateSwitch.addItems(self.States)
        self.StateSwitch.currentTextChanged.connect(lambda: self.changeState(self.StateSwitch.currentText()))
        self.setObjectName('StateSwitch')
        TopBar.addWidget(self.StateSwitch)


        self.Layout.addLayout(TopBar)
        self.Layout.addStretch()

    def changeState(self, state):

        for obj in self.PageObj:
            obj.clicked.disconnect()
            obj.clicked.connect(lambda: obj.clickState(state))

    def readerCSV(self, path):
        with open(path, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f, fieldnames=self.FieldNames)
            self.data = list(reader)

    def renderButton(self):
        ButtonGrid = QGridLayout()
        ButtonGrid.setObjectName('AIDSButtonGrid')
        ButtonGrid.setContentsMargins(10, 10, 10, 10)
        x, y = 0, 0
        for metadata in self.data[1:]:
            if y >= 10: y = 0; x += 1
            button = PageButton(page=metadata['page'], state=metadata['state'], remark=metadata['remark'])
            ButtonGrid.addWidget(button, x, y)
            self.PageObj.append(button)
            y += 1
        self.Layout.addLayout(ButtonGrid)




class PageButton(QPushButton):

    def __init__(self, page, state, remark):
        super().__init__()
        self.page = page
        self.state = state
        self.remark = remark
        self.setObjectName(f'AIDSPageButton_{state}')
        self.initButton()

    def initButton(self):
        self.setText(self.page)
        self.setObjectName(f'AIDSPageButton_{self.state}')
        self.clicked.connect(lambda: self.clickState('finished'))

    def clickState(self, NewState):
        print(NewState)







