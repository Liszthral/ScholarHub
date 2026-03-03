"""
    CopyRight: Liszthral
    Email: 2239288228@qq.com
    Project: ScholarHub - UI - TaskWindow
    Version: Alpha 1.0.3
    UpdateTime: 2026-0303-1630
"""

import csv
import time
from main import MAIN_PATH
from Utils import FloatMessage

from PyQt6.QtCore import Qt, QDateTime
from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QGridLayout, QScrollArea, QFrame, QDialog, QLineEdit,
    QComboBox, QDateTimeEdit, QFormLayout, QDialogButtonBox,
    QMessageBox
)


class TaskWindow(QWidget):
    """任务管理主窗口：四象限法则展示任务"""

    index = 2
    name = 'TaskWindow'

    def __init__(self, UI=None):
        super().__init__()
        self.UI = UI
        self.setObjectName("TaskWindow")

        # 存储每个象限的任务控件列表（大驼峰命名）
        self.UrgentImportant = []      # 重要且紧急
        self.UrgentNotImportant = []   # 紧急不重要
        self.NotUrgentImportant = []   # 重要不紧急
        self.NotUrgentNotImportant = [] # 不重要不紧急

        self.Layout = QVBoxLayout()
        self.setLayout(self.Layout)

        self.initUI()
        self.loadLocalTask()

    def initUI(self):
        """初始化界面：返回主页按钮 + 新增任务按钮 + 保存按钮 + 四象限网格"""
        # 顶部工具栏
        topBar = QHBoxLayout()
        topBar.addWidget(self.UI.turnWidgetButton('HomeWindow'))

        # 新增任务按钮
        self.AddButton = QPushButton("新增任务")
        self.AddButton.setObjectName("AddTaskButton")
        self.AddButton.clicked.connect(self.addTask)
        topBar.addWidget(self.AddButton)

        # 手动保存按钮
        self.SaveButton = QPushButton("保存")
        self.SaveButton.setObjectName("SaveTaskButton")
        self.SaveButton.clicked.connect(lambda: self.saveToCSV(showMsg=True))
        topBar.addWidget(self.SaveButton)

        topBar.addStretch()
        self.Layout.addLayout(topBar)

        # 初始化四象限
        self.initQUAD()

    def initQUAD(self):
        """创建四个象限的滚动区域和布局"""
        # 四个象限的容器
        self.Quad1 = QWidget()  # 重要且紧急
        self.Quad2 = QWidget()  # 重要不紧急
        self.Quad3 = QWidget()  # 不重要但紧急
        self.Quad4 = QWidget()  # 不重要不紧急

        # 布局
        self.Quad1Layout = QVBoxLayout(self.Quad1)
        self.Quad2Layout = QVBoxLayout(self.Quad2)
        self.Quad3Layout = QVBoxLayout(self.Quad3)
        self.Quad4Layout = QVBoxLayout(self.Quad4)

        # 设置对象名用于 QSS
        self.Quad1.setObjectName("QUAD1")
        self.Quad2.setObjectName("QUAD2")
        self.Quad3.setObjectName("QUAD3")
        self.Quad4.setObjectName("QUAD4")

        # 为每个象限添加标题
        self.Quad1Layout.addWidget(QLabel("【重要且紧急】"))
        self.Quad2Layout.addWidget(QLabel("【重要不紧急】"))
        self.Quad3Layout.addWidget(QLabel("【不重要但紧急】"))
        self.Quad4Layout.addWidget(QLabel("【不重要不紧急】"))

        # 创建滚动区域
        self.Scroll1 = QScrollArea()
        self.Scroll2 = QScrollArea()
        self.Scroll3 = QScrollArea()
        self.Scroll4 = QScrollArea()

        for scroll in (self.Scroll1, self.Scroll2, self.Scroll3, self.Scroll4):
            scroll.setWidgetResizable(True)
            scroll.setFrameShape(QFrame.Shape.NoFrame)

        self.Scroll1.setWidget(self.Quad1)
        self.Scroll2.setWidget(self.Quad2)
        self.Scroll3.setWidget(self.Quad3)
        self.Scroll4.setWidget(self.Quad4)

        # 网格布局放置四个象限
        grid = QGridLayout()
        grid.addWidget(self.Scroll1, 0, 0)
        grid.addWidget(self.Scroll2, 0, 1)
        grid.addWidget(self.Scroll3, 1, 0)
        grid.addWidget(self.Scroll4, 1, 1)
        grid.setRowStretch(0, 1)
        grid.setRowStretch(1, 1)
        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(1, 1)

        self.Layout.addLayout(grid)

        # 在每个象限布局末尾添加伸缩，使内容靠上排列
        for layout in (self.Quad1Layout, self.Quad2Layout, self.Quad3Layout, self.Quad4Layout):
            layout.addStretch()

    def loadLocalTask(self):
        """从 CSV 加载任务，并按紧急/重要分配到对应象限（CSV 使用分号分隔）"""
        csvPath = MAIN_PATH / 'Data' / 'TaskWindow' / 'Task.csv'
        if not csvPath.exists():
            # 若文件不存在，创建带表头的空文件
            csvPath.parent.mkdir(parents=True, exist_ok=True)
            with open(csvPath, 'w', encoding='utf-8-sig', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=['Content', 'CreateTime', 'EndTime',
                                                        'FinishTime', 'LoopMode', 'SonTask',
                                                        'Urgent', 'Important'], delimiter=';')
                writer.writeheader()
            self.UI.logger.info(f"TaskWindow - 创建空任务文件 {csvPath}")
            return

        try:
            with open(csvPath, 'r', encoding='utf-8-sig') as f:
                # 指定分隔符为分号
                reader = csv.DictReader(f, delimiter=';')
                for row in reader:
                    # 转换紧急/重要字段为布尔值（兼容字符串表示）
                    urgent = row.get('Urgent', '').lower() in ('true', '1', 'yes')
                    important = row.get('Important', '').lower() in ('true', '1', 'yes')

                    # 创建任务控件
                    task = TaskWidget(
                        content=row['Content'],
                        createTime=int(row['CreateTime']) if row['CreateTime'] else int(time.time()),
                        endTime=int(row['EndTime']) if row['EndTime'] else int(time.time()),
                        finishTime=int(row['FinishTime']) if row['FinishTime'] else None,
                        loopMode=row.get('LoopMode', 'once'),
                        sonTask=row.get('SonTask', ''),
                        urgent=urgent,
                        important=important,
                        parentWindow=self
                    )

                    # 根据分类添加到对应列表和布局
                    if urgent and important:
                        self.UrgentImportant.append(task)
                        layout = self.Quad1Layout
                    elif urgent and not important:
                        self.UrgentNotImportant.append(task)
                        layout = self.Quad2Layout
                    elif not urgent and important:
                        self.NotUrgentImportant.append(task)
                        layout = self.Quad3Layout
                    else:
                        self.NotUrgentNotImportant.append(task)
                        layout = self.Quad4Layout

                    # 插入到伸缩之前（最后一个索引是伸缩项）
                    layout.insertWidget(layout.count() - 1, task)

            self.UI.logger.info(f"TaskWindow - 成功加载 {len(self.UrgentImportant)+len(self.UrgentNotImportant)+len(self.NotUrgentImportant)+len(self.NotUrgentNotImportant)} 个任务")
        except Exception as e:
            FloatMessage.FloatMessage(f"加载任务失败：{e}", bg_color='#ff2020', text_color='#000000')
            self.UI.logger.error(f"TaskWindow - loadLocalTask 异常：{e}")

    def saveToCSV(self, showMsg=False):
        """将所有任务的数据保存到 CSV 文件（分号分隔）"""
        csvPath = MAIN_PATH / 'Data' / 'TaskWindow' / 'Task.csv'
        allTasks = (self.UrgentImportant + self.UrgentNotImportant +
                    self.NotUrgentImportant + self.NotUrgentNotImportant)

        data = []
        for task in allTasks:
            data.append({
                'Content': task.content,
                'CreateTime': str(task.createTime),
                'EndTime': str(task.endTime),
                'FinishTime': str(task.finishTime) if task.finishTime else '',
                'LoopMode': task.loopMode,
                'SonTask': task.sonTask,
                'Urgent': str(task.urgent),
                'Important': str(task.important)
            })

        try:
            with open(csvPath, 'w', encoding='utf-8-sig', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=['Content', 'CreateTime', 'EndTime',
                                                        'FinishTime', 'LoopMode', 'SonTask',
                                                        'Urgent', 'Important'], delimiter=';')
                writer.writeheader()
                writer.writerows(data)
            if showMsg:
                FloatMessage.FloatMessage("任务已保存", bg_color='#33cc33', text_color='#000000')
            self.UI.logger.info("TaskWindow - 保存 CSV 成功")
        except Exception as e:
            FloatMessage.FloatMessage(f"保存失败：{e}", bg_color='#ff2020', text_color='#000000')
            self.UI.logger.error(f"TaskWindow - saveToCSV 异常：{e}")

    def addTask(self):
        """弹出添加任务对话框"""
        dialog = AddTaskDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.getData()
            # 创建任务控件
            task = TaskWidget(
                content=data['content'],
                createTime=data['createTime'],
                endTime=data['endTime'],
                finishTime=None,
                loopMode=data['loopMode'],
                sonTask='',
                urgent=data['urgent'],
                important=data['important'],
                parentWindow=self
            )

            # 确定所属象限并添加
            if data['urgent'] and data['important']:
                targetList = self.UrgentImportant
                layout = self.Quad1Layout
            elif data['urgent'] and not data['important']:
                targetList = self.UrgentNotImportant
                layout = self.Quad2Layout
            elif not data['urgent'] and data['important']:
                targetList = self.NotUrgentImportant
                layout = self.Quad3Layout
            else:
                targetList = self.NotUrgentNotImportant
                layout = self.Quad4Layout

            targetList.append(task)
            layout.insertWidget(layout.count() - 1, task)

            # 自动保存
            self.saveToCSV(showMsg=False)
            FloatMessage.FloatMessage("任务已添加", bg_color='#33cc33', text_color='#000000')
            self.UI.logger.info(f"TaskWindow - 新增任务：{data['content']}")

    def removeTask(self, task):
        """从所有列表和布局中移除任务控件（由 TaskWidget 删除时调用）"""
        # 从列表中移除
        for lst in (self.UrgentImportant, self.UrgentNotImportant,
                    self.NotUrgentImportant, self.NotUrgentNotImportant):
            if task in lst:
                lst.remove(task)
                break

        # 从布局中移除
        task.setParent(None)
        task.deleteLater()

        # 自动保存
        self.saveToCSV(showMsg=False)
        self.UI.logger.info(f"TaskWindow - 删除任务：{task.content}")


class TaskWidget(QWidget):
    """单个任务卡片，包含内容、时间、操作按钮"""

    def __init__(self, content, createTime, endTime, finishTime,
                 loopMode, sonTask, urgent, important, parentWindow):
        super().__init__()
        self.content = content
        self.createTime = createTime
        self.endTime = endTime
        self.finishTime = finishTime
        self.loopMode = loopMode
        self.sonTask = sonTask
        self.urgent = urgent
        self.important = important
        self.parentWindow = parentWindow  # TaskWindow 实例

        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setObjectName("TaskWidget")
        self.initUI()

    def initUI(self):
        """构建任务卡片的 UI"""
        layout = QVBoxLayout(self)
        layout.setObjectName("TaskWidgetLayout")

        # 信息栏
        infoBar = QHBoxLayout()

        # 左侧：任务内容和时间
        leftPanel = QVBoxLayout()
        self.ContentLabel = QLabel(self.content)
        self.ContentLabel.setObjectName("ContentLabel")
        self.ContentLabel.setAlignment(Qt.AlignmentFlag.AlignLeft)
        leftPanel.addWidget(self.ContentLabel)

        createStr = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.createTime))
        self.CreateLabel = QLabel(f"创建：{createStr}")
        self.CreateLabel.setObjectName("CreateTimeLabel")
        leftPanel.addWidget(self.CreateLabel)

        endStr = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.endTime))
        self.EndLabel = QLabel(f"截止：{endStr}")
        self.EndLabel.setObjectName("EndTimeLabel")
        leftPanel.addWidget(self.EndLabel)

        if self.finishTime:
            finishStr = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.finishTime))
            self.FinishLabel = QLabel(f"完成：{finishStr}")
        else:
            self.FinishLabel = QLabel("未完成")
        self.FinishLabel.setObjectName("FinishTimeLabel")
        leftPanel.addWidget(self.FinishLabel)

        # 右侧：操作按钮
        rightPanel = QVBoxLayout()
        self.ConfigBtn = QPushButton("更改")
        self.ConfigBtn.setObjectName("ConfigButton")
        self.ConfigBtn.clicked.connect(self.configTask)
        rightPanel.addWidget(self.ConfigBtn)

        self.CompleteBtn = QPushButton("完成")
        self.CompleteBtn.setObjectName("CompleteButton")
        self.CompleteBtn.clicked.connect(self.completeTask)
        rightPanel.addWidget(self.CompleteBtn)

        self.DeleteBtn = QPushButton("删除")
        self.DeleteBtn.setObjectName("DeleteButton")
        self.DeleteBtn.clicked.connect(self.deleteTask)
        rightPanel.addWidget(self.DeleteBtn)

        infoBar.addLayout(leftPanel)
        infoBar.addStretch()
        infoBar.addLayout(rightPanel)
        layout.addLayout(infoBar)

        # 子任务占位（暂未实现）
        self.SonTaskBar = QVBoxLayout()
        layout.addLayout(self.SonTaskBar)

    def configTask(self):
        """弹出修改任务对话框"""
        dialog = EditTaskDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.getData()
            oldUrgent = self.urgent
            oldImportant = self.important
            # 更新属性
            self.content = data['content']
            self.createTime = data['createTime']
            self.endTime = data['endTime']
            self.loopMode = data['loopMode']
            newUrgent = data['urgent']
            newImportant = data['important']

            # 判断是否需要移动象限
            if newUrgent != oldUrgent or newImportant != oldImportant:
                # 1. 从原列表中移除
                for lst in (self.parentWindow.UrgentImportant, self.parentWindow.UrgentNotImportant,
                            self.parentWindow.NotUrgentImportant, self.parentWindow.NotUrgentNotImportant):
                    if self in lst:
                        lst.remove(self)
                        break
                # 2. 从原布局中取出（但不删除）
                self.setParent(None)
                # 3. 更新属性
                self.urgent = newUrgent
                self.important = newImportant
                # 4. 添加到新列表和布局
                if newUrgent and newImportant:
                    targetList = self.parentWindow.UrgentImportant
                    layout = self.parentWindow.Quad1Layout
                elif newUrgent and not newImportant:
                    targetList = self.parentWindow.UrgentNotImportant
                    layout = self.parentWindow.Quad2Layout
                elif not newUrgent and newImportant:
                    targetList = self.parentWindow.NotUrgentImportant
                    layout = self.parentWindow.Quad3Layout
                else:
                    targetList = self.parentWindow.NotUrgentNotImportant
                    layout = self.parentWindow.Quad4Layout
                targetList.append(self)
                layout.insertWidget(layout.count() - 1, self)
            else:
                # 仅更新显示内容
                self.ContentLabel.setText(self.content)
                self.CreateLabel.setText(f"创建：{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(self.createTime))}")
                self.EndLabel.setText(f"截止：{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(self.endTime))}")

            # 保存
            self.parentWindow.saveToCSV(showMsg=False)
            FloatMessage.FloatMessage("任务已更新", bg_color='#33cc33', text_color='#000000')
            self.parentWindow.UI.logger.info(f"TaskWindow - 更新任务：{self.content}")

    def completeTask(self):
        """标记任务为完成"""
        if self.finishTime is not None:
            reply = QMessageBox.question(
                self,
                "确认",
                "任务已完成，是否撤销完成状态？",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.Yes:
                self.finishTime = None
                self.FinishLabel.setText("未完成")
        else:
            self.finishTime = int(time.time())
            finishStr = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.finishTime))
            self.FinishLabel.setText(f"完成：{finishStr}")

        self.parentWindow.saveToCSV(showMsg=False)
        self.parentWindow.UI.logger.info(f"TaskWindow - 完成任务：{self.content}")

    def deleteTask(self):
        """删除任务"""
        reply = QMessageBox.question(
            self,
            "确认删除",
            f"确定要删除任务“{self.content}”吗？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.parentWindow.removeTask(self)


class AddTaskDialog(QDialog):
    """新增任务对话框（使用象限下拉框）"""

    # 象限映射：显示文本 -> (urgent, important)
    QUAD_MAP = {
        "重要且紧急": (True, True),
        "重要不紧急": (False, True),
        "不重要但紧急": (True, False),
        "不重要不紧急": (False, False)
    }

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("新增任务")
        self.setObjectName("AddTaskDialog")
        self.resize(400, 300)
        self.initUI()

    def initUI(self):
        layout = QFormLayout(self)

        # 任务内容
        self.ContentEdit = QLineEdit()
        layout.addRow("内容：", self.ContentEdit)

        # 截止时间（默认一小时后）
        self.EndTimeEdit = QDateTimeEdit()
        self.EndTimeEdit.setDateTime(QDateTime.currentDateTime().addSecs(3600))
        self.EndTimeEdit.setCalendarPopup(True)
        layout.addRow("截止时间：", self.EndTimeEdit)

        # 循环模式
        self.LoopCombo = QComboBox()
        self.LoopCombo.addItems(["once", "daily", "weekly", "monthly"])
        layout.addRow("循环模式：", self.LoopCombo)

        # 象限选择（替代原来的紧急/重要）
        self.QuadCombo = QComboBox()
        self.QuadCombo.addItems(list(self.QUAD_MAP.keys()))
        self.QuadCombo.setCurrentText("重要且紧急")  # 默认
        layout.addRow("所属象限：", self.QuadCombo)

        # 按钮
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)

    def getData(self):
        """返回用户输入的数据字典，包含 (urgent, important) 布尔值"""
        quadText = self.QuadCombo.currentText()
        urgent, important = self.QUAD_MAP[quadText]
        return {
            'content': self.ContentEdit.text(),
            'createTime': int(time.time()),  # 当前时间为创建时间
            'endTime': int(self.EndTimeEdit.dateTime().toSecsSinceEpoch()),
            'loopMode': self.LoopCombo.currentText(),
            'urgent': urgent,
            'important': important
        }


class EditTaskDialog(QDialog):
    """编辑任务对话框，预填现有数据，使用象限下拉框"""

    QUAD_MAP = AddTaskDialog.QUAD_MAP  # 复用映射
    # 反向映射： (urgent, important) -> 显示文本
    REVERSE_MAP = {v: k for k, v in QUAD_MAP.items()}

    def __init__(self, task_widget, parent=None):
        super().__init__(parent)
        self.task = task_widget
        self.setWindowTitle("编辑任务")
        self.setObjectName("EditTaskDialog")
        self.resize(400, 300)
        self.initUI()

    def initUI(self):
        layout = QFormLayout(self)

        self.ContentEdit = QLineEdit(self.task.content)
        layout.addRow("内容：", self.ContentEdit)

        dt = QDateTime.fromSecsSinceEpoch(self.task.endTime)
        self.EndTimeEdit = QDateTimeEdit(dt)
        self.EndTimeEdit.setCalendarPopup(True)
        layout.addRow("截止时间：", self.EndTimeEdit)

        self.LoopCombo = QComboBox()
        self.LoopCombo.addItems(["once", "daily", "weekly", "monthly"])
        self.LoopCombo.setCurrentText(self.task.loopMode)
        layout.addRow("循环模式：", self.LoopCombo)

        # 象限选择，根据当前 urgent/important 设置默认项
        self.QuadCombo = QComboBox()
        self.QuadCombo.addItems(list(self.QUAD_MAP.keys()))
        currentQuad = self.REVERSE_MAP.get((self.task.urgent, self.task.important), "重要且紧急")
        self.QuadCombo.setCurrentText(currentQuad)
        layout.addRow("所属象限：", self.QuadCombo)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)

    def getData(self):
        quadText = self.QuadCombo.currentText()
        urgent, important = self.QUAD_MAP[quadText]
        return {
            'content': self.ContentEdit.text(),
            'createTime': self.task.createTime,  # 创建时间不变
            'endTime': int(self.EndTimeEdit.dateTime().toSecsSinceEpoch()),
            'loopMode': self.LoopCombo.currentText(),
            'urgent': urgent,
            'important': important
        }
