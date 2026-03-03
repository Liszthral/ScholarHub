"""
    CopyRight: Liszthral
    Email: 2239288228@qq.com
    Project: ScholarHub - UI - TeachingAIDSWindow
    Version: Alpha 1.0.1
    UpdateTime: 2026-0211-2118
"""

import csv
import os.path
from main import MAIN_PATH
from Utils import FileVerify, FloatMessage

import matplotlib

matplotlib.use('Qt5Agg')  # 使用 PyQt5 后端（兼容 PyQt6）
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from PyQt6.QtCore import Qt, QRegularExpression
from PyQt6.QtGui import QRegularExpressionValidator
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QMessageBox, QLabel, QDialog, QTreeWidget,
     QTreeWidgetItem, QPushButton, QGridLayout, QComboBox, QHBoxLayout, QSpinBox, QScrollArea,
     QLineEdit, QTableWidget, QTableWidgetItem, QHeaderView)


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

    def initUI(self):
        """ <1> Top information bar. """
        self.Layout.addWidget(self.UI.turnWidgetButton('HomeWindow'))
        self.TopDirTree = QTreeWidget()
        """ <2> Iterate and render classification based on the corresponding directory. """
        self.renderDirTree()
        self.Layout.addWidget(self.TopDirTree)
        self.Layout.addStretch()

    def renderDirTree(self):
        """ <1> Render the first level directory and display the top-level classification. """
        self.TopDirTree.setHeaderLabel('选择呈式的项目')
        for path in os.listdir('TeachingAIDS'):
            ParentItem = QTreeWidgetItem(self.TopDirTree, [path])
            data = os.listdir(MAIN_PATH / 'TeachingAIDS' / path)
            for filename in data:
                filename = filename[:-4]
                QTreeWidgetItem(ParentItem, [filename])
        """ <2> How to bind items in a double-click <TopDirTree>. """
        self.TopDirTree.itemDoubleClicked.connect(self.turnShow)
        self.TopDirTree.expandAll()
        self.UI.logger.info('TeachingAIDSWindow - renderDirTree successful.')

    def turnShow(self, item):
        """ <1> Determine the type of double-click item. """
        result = self.judgeLayer(item)
        if result:  # It is the item corresponding to the <CSV file>.
            path = MAIN_PATH / 'TeachingAIDS' / result[0] / f'{result[1]}.csv'
            getIndex = self.UI.getStackIndex(f'{result[0]}-{result[1]}')  # Confirm if the page exists.
            if getIndex == 0:  # This page cannot be found, index=0 corresponds to the <HomeWindow>
                page = ShowAIDSInfo(path, self.UI)
                page.name = str(f'{result[0]}-{result[1]}')
                index = self.UI.registerStack(page)
                page.index = index
                self.UI.UIObject.append(page)  # Important: It must be manually added to UIObject, otherwise the <UI.toPage> cannot find the corresponding index.
                self.UI.toPage(page.index)
            else:  # index != 0， The page already exists and can be directly redirected.
                self.UI.toPage(getIndex)
            self.UI.logger.info(f'TeachingAIDSWindow - turnShow render and config successful.')
        self.UI.logger.info(f'TeachingAIDSWindow - Double clicked on the top-level path.')

    def judgeLayer(self, item):
        if item.parent() is None:  # Top level.
            self.addCSVItem(item.text(0))
            return False
        else:  # Corresponding to the <CSV file>
            ParentText = item.parent().text(0)
            ItemText = item.text(0)
            return ParentText, ItemText

    def addCSVItem(self, parent):
        """ <1> Create a modal window for relevant configuration information -> <QDialog>. """
        self.AddCSVItem = QDialog(self)
        self.AddCSVItem.setWindowTitle('ScholarHub - TeachingAIDSWindow - AddCSVItem')
        self.AddCSVItem.setObjectName('AIDS_AddCSVItem')
        self.AddCSVItem.resize(300, 80)
        """ <2> Create central control. """
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.AddCSVItem.setLayout(layout)
        """ <3> Display the kind of the selected file. """
        Layer1 = QHBoxLayout()
        KindHeadLabel = QLabel('所选分类：')
        KindHeadLabel.setMaximumWidth(80)
        KindBodyLabel = QLabel(str(parent))
        Layer1.addWidget(KindHeadLabel)
        Layer1.addStretch()
        Layer1.addWidget(KindBodyLabel)
        layout.addLayout(Layer1)
        """ <4> Display the total number of page numbers. """
        Layer2 = QHBoxLayout()
        SonItemHeadLabel = QLabel('新建子项：')
        SonItemHeadLabel.setMaximumWidth(80)
        # Preventing illegal paths, including "." to prevent path traversal.
        Ban = QRegularExpression(rf'^[^{FileVerify.ILLEGAL_CHARS}.\']*$')
        SonItemBodyText = QLineEdit()
        SonItemBodyText.setMaxLength(80)
        SonItemBodyText.setValidator(QRegularExpressionValidator(Ban))
        Layer2.addWidget(SonItemHeadLabel)
        Layer2.addStretch()
        Layer2.addWidget(SonItemBodyText)
        layout.addLayout(Layer2)
        """ <5> Related operation buttons. """
        Layer3 = QHBoxLayout()
        CommitButton = QPushButton('提交')
        CommitButton.setObjectName('AIDS_CommitButton')
        CommitButton.clicked.connect(lambda: self.handleAddSonItem(parent=parent, ItemName=SonItemBodyText.text()))
        CancelButton = QPushButton('取消')
        CancelButton.clicked.connect(lambda: self.AddCSVItem.close())
        Layer3.addStretch()
        Layer3.addWidget(CommitButton)
        Layer3.addStretch()
        Layer3.addWidget(CancelButton)
        layout.addLayout(Layer3)
        Layer3.addStretch()
        """ <6> Start the modal window and block the main thread. """
        self.AddCSVItem.exec()
        self.UI.logger.info(f'ShowAIDSInfo - Render <AddSonItem> dialog successfully.')

    def handleAddSonItem(self, parent, ItemName):
        """ <1> Check whether the naming is legal. """
        Bool, Info = FileVerify.verifyFileName(ItemName)
        if not Bool:
            FloatMessage.FloatMessage('文件命名不符合规范，不可含有保留关键字', bg_color='#ff2020', text_color='#000000')
            self.UI.logger.info(f'ShowAIDSInfo - handleAddSonItem -> {ItemName} - {Info}.')
            return False
        """ <2> Create a new CSV file in the specified path. """
        path = MAIN_PATH / 'TeachingAIDS' / str(parent) / (str(ItemName) + '.csv')
        with open(path, 'w', encoding='utf-8-sig', newline=''): pass
        FloatMessage.FloatMessage(f'新建项目{parent}-{ItemName}完成', bg_color='#33cc33', text_color='#000000')
        self.UI.logger.info(f'ShowAIDSInfo - handleAddSonItem -> Create NewItem <{parent}-{ItemName}>.')
        """ <3> Resubmit the first level directory. """
        self.TopDirTree.clear()
        self.renderDirTree()
        self.update()
        return True


class ShowAIDSInfo(QWidget):

    index = None
    name = None
    FieldNames = ['page', 'state', 'remark']
    States = ['finished', 'unfinished', 'processing', 'doubting']

    def __init__(self, path, UI=None):
        super().__init__()
        """ <1> Initialize parameters. """
        # Must be an instance property, not a class property.
        self.data = []
        self.PageObj = []
        self.row, self.col = 0, 0
        """ <2> Render basic UI config. """
        self.UI = UI
        self.path = path
        self.setObjectName("ShowAIDSInfo")
        self.Layout = QVBoxLayout()
        self.setLayout(self.Layout)
        self.OverView = QWidget()
        """ <3> Rendering page UI elements. """
        self.initUI()
        self.readerCSV(self.path)
        self.renderButton()
        self.UI.logger.info('ShowAIDSInfo - Render successful.')

    def initUI(self):
        """ <1> Top information bar. """
        TopBar = QHBoxLayout(self)
        TopBar.addWidget(self.UI.turnWidgetButton('TeachingAIDSWindow'))
        TopBar.addStretch()
        """ <2> Page operation related functions. """
        # Delete program.
        self.OverViewButton = QPushButton('OverView')
        self.OverViewButton.setObjectName('OverViewButton')
        self.OverViewButton.clicked.connect(self.overviewData)
        TopBar.addWidget(self.OverViewButton)
        # Delete program.
        self.DeleteButton = QPushButton('Delete')
        self.DeleteButton.setObjectName('DeleteButton')
        self.DeleteButton.clicked.connect(self.deleteProgram)
        TopBar.addWidget(self.DeleteButton)
        # Change page settings.
        self.ConfigButton = QPushButton('Configure')
        self.ConfigButton.setObjectName('ConfigButton')
        self.ConfigButton.clicked.connect(self.configInfo)
        TopBar.addWidget(self.ConfigButton)
        # Save file to local.
        self.SaveButton = QPushButton('SaveFile')
        self.SaveButton.setObjectName('SaveButton')
        self.SaveButton.clicked.connect(lambda: self.saveCSV(showMsg=True))
        TopBar.addWidget(self.SaveButton)
        # Operation status switching bar.
        self.StateSwitch = QComboBox()
        self.StateSwitch.addItems(self.States)
        self.StateSwitch.currentTextChanged.connect(lambda: self.changeState(self.StateSwitch.currentText()))
        self.setObjectName('StateSwitch')
        TopBar.addWidget(self.StateSwitch)
        self.Layout.addLayout(TopBar)
        self.Layout.addStretch()
        self.UI.logger.info('ShowAIDSInfo - Render TopBar successful.')
        """ <3> Pre-generated grid control for carrying buttons. """
        self.ButtonWidget = QWidget()
        self.ButtonGrid = QGridLayout(self.ButtonWidget)
        self.ButtonGrid.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.ButtonGrid.setObjectName('AIDSButtonGrid')
        self.ButtonGrid.setContentsMargins(10, 10, 10, 10)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(self.ButtonWidget)
        self.Layout.addWidget(scroll)

    def changeState(self, state):
        """
            When the operation state selected by<self. StateSwitch>changes,
            rebind the state change function corresponding to the page button.
        """
        for obj in self.PageObj:
            obj.clicked.disconnect()
            obj.clicked.connect(lambda checked, o=obj, s=state: o.clickState(s))  # Important: Closure trap!
        self.UI.logger.info(f'ShowAIDSInfo - Batch-change <obj.button> state -> <{state}>.')

    def readerCSV(self, path):
        try:
            with open(path, 'r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f, fieldnames=self.FieldNames)
                self.data = list(reader)
            self.UI.logger.info(f'ShowAIDSInfo - Load <CSV File> -> <{path}> successful.')
        except FileNotFoundError:
            FloatMessage.FloatMessage(f'路径不存在：path={path}', bg_color='#ff2020', text_color='#000000')
            self.UI.logger.error(f'ShowAIDSInfo - Not found <CSV File> -> <{path}>.')
        except Exception as e:
            FloatMessage.FloatMessage(f'发生未知错误：INFO={e}', bg_color='#ff2020', text_color='#000000')
            self.UI.logger.error(f'ShowAIDSInfo - Error occurred while reading <CSV File> -> <{path}>, info={e}.')

    def renderButton(self):
        """ <1> Ensure initialization parameters and re-render buttons. """
        self.PageObj = []
        self.clearButtonGrid()
        self.row, self.col = 0, 0
        # Read data from <self.data> and generate corresponding page numbers button.
        for metadata in self.data[1:]:
            if self.col >= 10: self.col = 0; self.row += 1
            button = PageButton(page=metadata['page'], state=metadata['state'], remark=metadata['remark'])
            self.ButtonGrid.addWidget(button, self.row, self.col)
            self.PageObj.append(button)
            self.col += 1
        self.Layout.addLayout(self.ButtonGrid)
        self.UI.logger.info(f'ShowAIDSInfo - Successfully rendered page button {len(self.PageObj)}.')

    def saveCSV(self, showMsg=False):
        """ Retrieve the latest metadata from the page number button object and save it to a local file. """
        self.data.clear()
        for obj in self.PageObj:
            self.data.append(obj.getMetadata())
        try:
            with open(self.path, 'w', encoding='utf-8-sig', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=self.FieldNames)
                writer.writeheader()
                writer.writerows(self.data)
            self.UI.logger.info(f'ShowAIDSInfo - saveCSV - Successfully saved to <{self.path}>.')
            if showMsg: FloatMessage.FloatMessage('文件更改保存成功', bg_color='#33cc33', text_color='#000000')
        except FileNotFoundError:
            FloatMessage.FloatMessage(f'路径不存在：path={self.path}', bg_color='#ff2020', text_color='#000000')
            self.UI.logger.error(f'ShowAIDSInfo - Not found <CSV File> -> <{self.path}>.')
        except Exception as e:
            print(e)
            FloatMessage.FloatMessage(f'发生未知错误：INFO={e}', bg_color='#ff2020', text_color='#000000')
            self.UI.logger.error(f'ShowAIDSInfo - Error occurred while saving <CSV File> -> <{self.path}>, info={e}.')

    def deleteProgram(self):
        """删除当前教学项目（CSV文件），并返回上一级目录"""
        # 1. 确认对话框
        reply = QMessageBox.question(
            self,
            '确认删除',
            f'确定要永久删除项目文件“{self.path}”吗？\n此操作不可撤销。',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        if reply != QMessageBox.StandardButton.Yes:
            return

        # 2. 尝试删除文件
        try:
            os.remove(self.path)
            self.UI.logger.info(f'ShowAIDSInfo - Deleted file: {self.path}')
        except FileNotFoundError:
            FloatMessage.FloatMessage('文件不存在，可能已被删除', bg_color='#ff2020', text_color='#000000')
            self.UI.logger.error(f'ShowAIDSInfo - File not found when deleting: {self.path}')
            # 文件已不存在，继续清理UI
        except Exception as e:
            FloatMessage.FloatMessage(f'删除文件时发生错误：{e}', bg_color='#ff2020', text_color='#000000')
            self.UI.logger.error(f'ShowAIDSInfo - Error deleting file {self.path}: {e}')
            return

        # 3. 从 UI 中移除自身（彻底清理）
        # 3.1 从 QStackedWidget 中移除
        index = self.UI.StackWidget.indexOf(self)
        if index != -1:
            self.UI.StackWidget.removeWidget(self)
            self.UI.logger.info(f'ShowAIDSInfo - Removed self from StackWidget at index {index}')

        # 3.2 从 UI.UIObject 列表中移除
        if self in self.UI.UIObject:
            self.UI.UIObject.remove(self)
            self.UI.logger.info(f'ShowAIDSInfo - Removed self from UIObject')

        # 3.3 从 UI.StackWidgets 字典中删除该窗口的 name 映射
        if self.name in self.UI.StackWidgets:
            del self.UI.StackWidgets[self.name]
            self.UI.logger.info(f'ShowAIDSInfo - Removed self from StackWidgets dict')

        # 4. 切换到 TeachingAIDSWindow 并刷新目录树
        self.UI.toPage(self.UI.getStackIndex('TeachingAIDSWindow'))
        teaching_aids_window = self.UI.TeachingAIDSWindow  # main.py 中已将该窗口保存为属性
        teaching_aids_window.TopDirTree.clear()
        teaching_aids_window.renderDirTree()
        teaching_aids_window.update()

        # 5. 提示成功
        FloatMessage.FloatMessage('项目已删除', bg_color='#33cc33', text_color='#000000')

    def configInfo(self):
        """ <1> Create a modal window for relevant configuration information -> <QDialog>. """
        self.ConfigPanel = QDialog(self)
        self.ConfigPanel.setWindowTitle('ScholarHub - TeachingAIDSWindow - ConfigInfo')
        self.ConfigPanel.setObjectName('AIDS_ConfigPanel')
        self.ConfigPanel.resize(300, 80)
        """ <2> Create central control. """
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.ConfigPanel.setLayout(layout)
        """ <3> Display the path of the selected file. """
        Layer1 = QHBoxLayout()
        PathHeadLabel = QLabel('文件路径：')
        PathHeadLabel.setMaximumWidth(80)
        PathBodyLabel = QLabel(repr(str(self.path)))
        Layer1.addWidget(PathHeadLabel)
        Layer1.addStretch()
        Layer1.addWidget(PathBodyLabel)
        layout.addLayout(Layer1)
        """ <4> Display the total number of page numbers. """
        Layer2 = QHBoxLayout()
        PageNumHeadLabel = QLabel('页码总数：')
        PageNumHeadLabel.setMaximumWidth(80)
        PageNumBodySpinBox = QSpinBox()
        PageNumBodySpinBox.setRange(0, 500)
        PageNumBodySpinBox.setSingleStep(1)
        lines = len(self.data) - 1 if len(self.data) else 50  # <len(self.data) - 1> -> Clear the DictHeader.
        PageNumBodySpinBox.setValue(lines)
        Layer2.addWidget(PageNumHeadLabel)
        Layer2.addStretch()
        Layer2.addWidget(PageNumBodySpinBox)
        layout.addLayout(Layer2)
        """ <5> Related operation buttons. """
        Layer3 = QHBoxLayout()
        CommitButton = QPushButton('提交')
        CommitButton.setObjectName('AIDS_CommitButton')
        CommitButton.clicked.connect(lambda: self.updateConfig(NewLines=int(PageNumBodySpinBox.text())))
        CancelButton = QPushButton('取消')
        CancelButton.setObjectName('AIDS_CancelButton')
        CancelButton.clicked.connect(lambda: self.ConfigPanel.close())
        Layer3.addStretch()
        Layer3.addWidget(CommitButton)
        Layer3.addStretch()
        Layer3.addWidget(CancelButton)
        layout.addLayout(Layer3)
        Layer3.addStretch()
        """ <6> Start the modal window and block the main thread. """
        self.ConfigPanel.exec()  # Modal window uses exec() to block the main process.
        self.UI.logger.info(f'ShowAIDSInfo - Render configuration change page successfully.')

    def clearButtonGrid(self):
        """ Clear all child controls in the button control. """
        if self.ButtonGrid is not None:
            while self.ButtonGrid.count() > 0:
                item = self.ButtonGrid.takeAt(0)
                if item.widget():
                    item.widget().deleteLater()
                elif item.layout():
                    item.layout().deleteLater()
                elif item.spacerItem():
                    del item
        self.UI.logger.info(f'ShowAIDSInfo - Clean all Widget in <ButtonGrid> successfully.')

    def updateConfig(self, NewLines) -> bool:
        """ <echo-self.initUI-ConfigButton> Apply changes and save configuration. """
        lines = len(self.data) - 1 if len(self.data) != 0 else 0
        if NewLines == lines:  # The number of page numbers has not changed.
            FloatMessage.FloatMessage('新旧数据重复，无需更改', bg_color='#ffffff', text_color='#000000')
            self.UI.logger.info(f'ShowAIDSInfo-updateConfig: Duplicate old and new data.')
            return True
        elif NewLines > lines:
            for i in range(lines + 1, NewLines + 1):
                metadata = {
                    'page': str(i),
                    'state': 'unfinished',
                    'remark': 'null'
                }
                if self.col >= 10: self.col = 0; self.row += 1
                button = PageButton(page=metadata['page'], state=metadata['state'], remark=metadata['remark'])
                self.ButtonGrid.addWidget(button, self.row, self.col)
                self.PageObj.append(button)
                self.col += 1
            self.saveCSV()
            self.readerCSV(self.path)
            self.update()
            FloatMessage.FloatMessage('页码扩展更改成功', bg_color='#33cc33', text_color='#000000')
            self.UI.logger.info(f'ShowAIDSInfo-updateConfig: Increase the number of pages to {len(self.data) - 1} successfully.')
            return True
        elif NewLines < lines:
            self.PageObj = self.PageObj[:NewLines]
            self.saveCSV()
            self.readerCSV(self.path)
            self.clearButtonGrid()
            self.renderButton()
            self.update()
            FloatMessage.FloatMessage('页码缩减更改成功', bg_color='#33cc33', text_color='#000000')
            self.UI.logger.info(f'ShowAIDSInfo-updateConfig: Decrease the number of pages to {len(self.data) - 1} successfully.')
            return True
        else:
            QMessageBox.warning(self,
                        'ScholarHub - TeachingAIDSWindow - UpdateConfig',
                        '这是什么奇妙的操作？')
            self.UI.logger.warning(f'ShowAIDSInfo-updateConfig: Unknown operation, NewLines={NewLines}.')
            return False

    def overviewData(self):
        """生成统计概览：饼状图 + 表格，显示各状态页码数量"""
        # 1. 统计各状态数量
        state_count = {state: 0 for state in self.States}
        for button in self.PageObj:
            if button.state in state_count:
                state_count[button.state] += 1

        # 2. 创建模态对话框
        dialog = QDialog(self)
        dialog.setWindowTitle('ScholarHub - 教学概览')
        dialog.setObjectName('AIDS_OverviewDialog')
        dialog.resize(800, 500)

        # 3. 主布局：水平排列
        main_layout = QHBoxLayout(dialog)

        # 4. 左侧：matplotlib 画布（饼图）
        fig = Figure(figsize=(5, 4), dpi=100)
        canvas = FigureCanvas(fig)
        main_layout.addWidget(canvas, stretch=2)

        # 绘制饼图
        ax = fig.add_subplot(111)
        labels = list(state_count.keys())
        sizes = list(state_count.values())
        # 过滤掉数量为0的状态，避免饼图显示0%
        non_zero = [(l, s) for l, s in zip(labels, sizes) if s > 0]
        if non_zero:
            labels, sizes = zip(*non_zero)
        else:
            labels, sizes = ['无数据'], [1]  # 无数据时显示占位

        # 设置中文字体（若系统支持）
        try:
            matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'WenQuanYi Micro Hei']
            matplotlib.rcParams['axes.unicode_minus'] = False
        except:
            pass

        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')  # 保证饼图是圆形
        ax.set_title('页码状态分布')

        # 5. 右侧：表格显示详细数量
        table = QTableWidget()
        table.setObjectName('AIDS_OverviewTable')
        table.setColumnCount(2)
        table.setHorizontalHeaderLabels(['状态', '数量'])
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        table.setRowCount(len(self.States))

        for i, state in enumerate(self.States):
            item_state = QTableWidgetItem(state)
            item_count = QTableWidgetItem(str(state_count[state]))
            table.setItem(i, 0, item_state)
            table.setItem(i, 1, item_count)

        main_layout.addWidget(table, stretch=1)

        # 6. 显示对话框（模态）
        dialog.exec()
        self.UI.logger.info('ShowAIDSInfo - Overview dialog displayed.')


class PageButton(QPushButton):

    def __init__(self, page, state, remark):
        super().__init__()
        self.page = page
        self.state = state
        self.remark = remark
        # Init UI config.
        self.setObjectName(f'AIDSPageButton_{state}')
        self.setProperty("state", self.state)
        self.initButton()

    def initButton(self):
        self.setText(self.page)
        self.setObjectName(f'AIDSPageButton_{self.state}')
        self.clicked.connect(lambda: self.clickState('finished'))

    def clickState(self, NewState):
        if NewState in ShowAIDSInfo.States:
            self.state = NewState
            self.setObjectName(f'AIDSPageButton_{self.state}')
            self.setProperty("state", NewState)
            # Important: QSS style must be manually cleared and reloaded, QT will not process automatically.
            self.style().unpolish(self)
            self.style().polish(self)

    def getMetadata(self) -> dict:
        content = {
            'page': self.page,
            'state': self.state,
            'remark': self.remark,
        }
        return content
