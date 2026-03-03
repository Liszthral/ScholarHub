"""
    CopyRight: Liszthral
    Email: 2239288228@qq.com
    Project: ScholarHub - UI - AlarmWindow
    Version: Alpha 1.3.0
    UpdateTime: 2026-0303-2030
"""

import csv
import os
from datetime import datetime
from main import MAIN_PATH
from Utils import FloatMessage

from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtCore import Qt, QTimer, QTime, QUrl
from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QGridLayout, QScrollArea, QFrame, QDialog, QFormLayout,
    QLineEdit, QComboBox, QTimeEdit, QDialogButtonBox,
    QMessageBox, QCheckBox, QListWidget, QAbstractItemView
)


class AlarmWindow(QWidget):
    """闹钟管理主窗口：3×3网格展示闹钟卡片，支持开关、多模式、铃声选择"""

    name = 'AlarmWindow'
    index = 16

    def __init__(self, UI=None):
        super().__init__()
        self.UI = UI
        self.setObjectName("AlarmWindow")

        self.current_row = 0
        self.current_col = 0
        self.alarms = []          # 存储所有 AlarmWidget 实例

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.initUI()
        self.loadLocalAlarm()
        self.startTimerCheck()

    def initUI(self):
        """初始化界面：顶部工具栏 + 闹钟网格区域"""
        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)
        self.audio_output.setVolume(0.5)  # 设置音量 50%

        topBar = QHBoxLayout()
        topBar.addWidget(self.UI.turnWidgetButton('HomeWindow'))

        self.AddButton = QPushButton("新增闹钟")
        self.AddButton.setObjectName("AddAlarmButton")
        self.AddButton.clicked.connect(self.createAlarm)
        topBar.addWidget(self.AddButton)

        self.SaveButton = QPushButton("保存")
        self.SaveButton.setObjectName("SaveAlarmButton")
        self.SaveButton.clicked.connect(lambda: self.saveToCSV(showMsg=True))
        topBar.addWidget(self.SaveButton)

        topBar.addStretch()
        self.layout.addLayout(topBar)

        # 闹钟网格滚动区域
        self.AlarmArea = QWidget()
        self.AlarmArea.setObjectName("AlarmArea")
        self.AlarmScroll = QScrollArea()
        self.AlarmScroll.setWidgetResizable(True)
        self.AlarmScroll.setFrameShape(QFrame.Shape.NoFrame)
        self.AlarmScroll.setWidget(self.AlarmArea)

        self.AlarmGrid = QGridLayout(self.AlarmArea)
        self.AlarmGrid.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.AlarmGrid.setHorizontalSpacing(10)
        self.AlarmGrid.setVerticalSpacing(10)

        self.layout.addWidget(self.AlarmScroll)

    def addAlarmWidget(self, ring_time='08:00', loop_mode='once', week_days='',
                       remark='', ring_music='default', enabled=True):
        """
        创建闹钟卡片并添加到网格
        :param ring_time: 字符串 "HH:MM"
        :param loop_mode: "once"/"daily"/"weekly"
        :param week_days: 仅 weekly 有效，逗号分隔的数字（1=周一,7=周日）
        :param remark: 备注
        :param ring_music: 铃声文件名
        :param enabled: 开关状态
        """
        widget = AlarmWidget(
            ring_time=ring_time,
            loop_mode=loop_mode,
            week_days=week_days,
            remark=remark,
            ring_music=ring_music,
            enabled=enabled,
            parent_window=self
        )
        self.alarms.append(widget)

        self.AlarmGrid.addWidget(widget, self.current_row, self.current_col)
        self.current_col += 1
        if self.current_col >= 3:
            self.current_col = 0
            self.current_row += 1

        self.UI.logger.info(f"AlarmWindow - 添加闹钟：{ring_time} {remark}")
        return widget

    def removeAlarmWidget(self, widget):
        """从网格和列表中移除指定闹钟控件"""
        if widget in self.alarms:
            self.alarms.remove(widget)
            widget.setParent(None)
            widget.deleteLater()
            self.refreshGrid()
            self.UI.logger.info(f"AlarmWindow - 移除闹钟：{widget.ring_time}")
            self.saveToCSV(showMsg=False)

    def refreshGrid(self):
        """重新排列所有闹钟（3列）"""
        for i in reversed(range(self.AlarmGrid.count())):
            item = self.AlarmGrid.itemAt(i)
            if item and item.widget():
                item.widget().setParent(None)

        self.current_row = 0
        self.current_col = 0

        for widget in self.alarms:
            self.AlarmGrid.addWidget(widget, self.current_row, self.current_col)
            self.current_col += 1
            if self.current_col >= 3:
                self.current_col = 0
                self.current_row += 1

    def loadLocalAlarm(self):
        """从 CSV 加载闹钟数据（新格式：无 RetainMode）"""
        csv_path = MAIN_PATH / "Data" / "AlarmWindow" / "Alarm.csv"
        if not csv_path.exists():
            csv_path.parent.mkdir(parents=True, exist_ok=True)
            with open(csv_path, 'w', encoding='utf-8-sig', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=[
                    'RingTime', 'LoopMode', 'WeekDays', 'Remark',
                    'RingMusic', 'Enabled'
                ], delimiter=';')
                writer.writeheader()
            self.UI.logger.info(f"AlarmWindow - 创建空文件 {csv_path}")
            return

        try:
            with open(csv_path, 'r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f, delimiter=';')
                for row in reader:
                    enabled = row.get('Enabled', 'True').lower() in ('true', '1', 'yes')
                    self.addAlarmWidget(
                        ring_time=row.get('RingTime', '08:00'),
                        loop_mode=row.get('LoopMode', 'once'),
                        week_days=row.get('WeekDays', ''),
                        remark=row.get('Remark', ''),
                        ring_music=row.get('RingMusic', 'default'),
                        enabled=enabled
                    )
            self.UI.logger.info(f"AlarmWindow - 成功加载 {len(self.alarms)} 个闹钟")
        except Exception as e:
            FloatMessage.FloatMessage(f"加载闹钟失败：{e}", bg_color='#ff2020', text_color='#000000')
            self.UI.logger.error(f"AlarmWindow - loadLocalAlarm 异常：{e}")

    def saveToCSV(self, showMsg=False):
        """将所有闹钟数据保存到 CSV（新格式）"""
        csv_path = MAIN_PATH / "Data" / "AlarmWindow" / "Alarm.csv"
        data = []
        for w in self.alarms:
            data.append({
                'RingTime': w.ring_time,
                'LoopMode': w.loop_mode,
                'WeekDays': w.week_days,
                'Remark': w.remark,
                'RingMusic': w.ring_music,
                'Enabled': str(w.enabled)
            })

        try:
            with open(csv_path, 'w', encoding='utf-8-sig', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=[
                    'RingTime', 'LoopMode', 'WeekDays', 'Remark',
                    'RingMusic', 'Enabled'
                ], delimiter=';')
                writer.writeheader()
                writer.writerows(data)
            if showMsg:
                FloatMessage.FloatMessage("闹钟已保存", bg_color='#33cc33', text_color='#000000')
            self.UI.logger.info("AlarmWindow - 保存 CSV 成功")
        except Exception as e:
            FloatMessage.FloatMessage(f"保存失败：{e}", bg_color='#ff2020', text_color='#000000')
            self.UI.logger.error(f"AlarmWindow - saveToCSV 异常：{e}")

    def createAlarm(self):
        """弹出新增闹钟对话框"""
        dialog = AddAlarmDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.getData()
            self.addAlarmWidget(
                ring_time=data['ring_time'],
                loop_mode=data['loop_mode'],
                week_days=data['week_days'],
                remark=data['remark'],
                ring_music=data['ring_music'],
                enabled=data['enabled']
            )
            self.saveToCSV(showMsg=False)
            FloatMessage.FloatMessage("闹钟已添加", bg_color='#33cc33', text_color='#000000')
            self.UI.logger.info(f"AlarmWindow - 新增闹钟：{data['ring_time']} {data['remark']}")

    def startTimerCheck(self):
        """启动每分钟检查定时器"""
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.checkAlarms)
        self.timer.start(60000)
        self.checkAlarms()  # 立即执行一次

    def checkAlarms(self):
        """检查当前时间是否匹配任何已启用的闹钟"""
        now = datetime.now()
        current_time = now.strftime("%H:%M")
        current_weekday = now.isoweekday()  # 周一=1, 周日=7

        for widget in self.alarms[:]:  # 遍历副本
            if not widget.enabled:
                continue

            if widget.ring_time != current_time:
                continue

            should_ring = False
            if widget.loop_mode == 'once':
                should_ring = True
            elif widget.loop_mode == 'daily':
                should_ring = True
            elif widget.loop_mode == 'weekly':
                if widget.week_days:
                    days = [int(x.strip()) for x in widget.week_days.split(',') if x.strip()]
                    if current_weekday in days:
                        should_ring = True

            if should_ring:
                self.triggerAlarm(widget)

    def triggerAlarm(self, widget):
        """触发闹钟：播放铃声并弹窗提示，根据模式决定是否删除"""
        # 构建铃声文件路径
        if widget.ring_music and widget.ring_music != 'default':
            music_path = MAIN_PATH / "MediaFile" / "Audio" / widget.ring_music
            if music_path.exists():
                self.player.setSource(QUrl.fromLocalFile(str(music_path)))
                self.player.play()
                print("播放器状态：", self.player.mediaStatus())
            else:
                self.UI.logger.warning(f"AlarmWindow - 铃声文件不存在：{music_path}")
        else:
            self.UI.logger.info("AlarmWindow - 使用默认铃声（无音频播放）")

        # 弹窗告示
        QMessageBox.information(
            self,
            "闹钟提醒",
            f"时间：{widget.ring_time}\n备注：{widget.remark}\n铃声：{widget.ring_music}"
        )

        # 停止播放
        self.player.stop()
        self.UI.logger.info(f"AlarmWindow - 闹钟触发：{widget.ring_time} {widget.remark}")

        # 仅 once 模式触发后删除闹钟
        if widget.loop_mode == 'once':
            self.removeAlarmWidget(widget)


class AlarmWidget(QWidget):
    """闹钟卡片，包含时间、备注、模式、开关、操作按钮"""

    def __init__(self, ring_time, loop_mode, week_days, remark,
                 ring_music, enabled, parent_window):
        super().__init__()
        self.ring_time = ring_time
        self.loop_mode = loop_mode
        self.week_days = week_days
        self.remark = remark
        self.ring_music = ring_music
        self.enabled = enabled
        self.parent_window = parent_window

        self.setObjectName("AlarmWidget")
        self.setMaximumHeight(140)
        self.setMaximumWidth(240)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        self.initUI()
        self.updateModeDisplay()

    def initUI(self):
        layout = QVBoxLayout(self)

        # 顶部：开关 + 时间
        top_bar = QHBoxLayout()
        self.SwitchCheck = QCheckBox()
        self.SwitchCheck.setObjectName("AlarmSwitch")
        self.SwitchCheck.setChecked(self.enabled)
        self.SwitchCheck.toggled.connect(self.onSwitchToggled)
        top_bar.addWidget(self.SwitchCheck)

        self.TimeLabel = QLabel(self.ring_time)
        self.TimeLabel.setObjectName("RingTimeLabel")
        self.TimeLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        top_bar.addWidget(self.TimeLabel)
        top_bar.addStretch()
        layout.addLayout(top_bar)

        # 备注
        self.RemarkLabel = QLabel(self.remark if self.remark else "无备注")
        self.RemarkLabel.setObjectName("RemarkLabel")
        self.RemarkLabel.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.RemarkLabel)

        # 模式显示
        self.ModeLabel = QLabel()
        self.ModeLabel.setObjectName("ModeLabel")
        self.ModeLabel.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.ModeLabel)

        # 操作按钮行
        btn_bar = QHBoxLayout()
        self.ConfigBtn = QPushButton("更改")
        self.ConfigBtn.setObjectName("ConfigButton")
        self.ConfigBtn.clicked.connect(self.configAlarm)
        btn_bar.addWidget(self.ConfigBtn)

        self.CompleteBtn = QPushButton("完成")
        self.CompleteBtn.setObjectName("CompleteButton")
        self.CompleteBtn.clicked.connect(self.completeAlarm)
        btn_bar.addWidget(self.CompleteBtn)

        self.DeleteBtn = QPushButton("删除")
        self.DeleteBtn.setObjectName("DeleteButton")
        self.DeleteBtn.clicked.connect(self.deleteAlarm)
        btn_bar.addWidget(self.DeleteBtn)
        layout.addLayout(btn_bar)

    def updateModeDisplay(self):
        """根据当前模式更新显示文本"""
        if self.loop_mode == 'once':
            mode_text = "仅一次"
        elif self.loop_mode == 'daily':
            mode_text = "每天"
        elif self.loop_mode == 'weekly':
            if self.week_days:
                day_map = {1: '一', 2: '二', 3: '三', 4: '四', 5: '五', 6: '六', 7: '日'}
                days = [day_map.get(int(d), '?') for d in self.week_days.split(',') if d]
                mode_text = "每周" + ''.join(days)
            else:
                mode_text = "每周(未设置)"
        else:
            mode_text = self.loop_mode

        music_name = os.path.basename(self.ring_music) if self.ring_music != 'default' else '默认'
        mode_text += f" | {music_name}"
        self.ModeLabel.setText(mode_text)

    def onSwitchToggled(self, checked):
        """开关状态改变时更新 enabled 并自动保存"""
        self.enabled = checked
        self.parent_window.saveToCSV(showMsg=False)
        self.parent_window.UI.logger.info(f"AlarmWidget - 开关 {'开启' if checked else '关闭'}：{self.ring_time}")

    def configAlarm(self):
        """打开编辑对话框"""
        dialog = EditAlarmDialog(self, self.parent_window)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.getData()
            self.ring_time = data['ring_time']
            self.loop_mode = data['loop_mode']
            self.week_days = data['week_days']
            self.remark = data['remark']
            self.ring_music = data['ring_music']
            # 开关状态保持原样
            self.TimeLabel.setText(self.ring_time)
            self.RemarkLabel.setText(self.remark if self.remark else "无备注")
            self.updateModeDisplay()
            self.parent_window.saveToCSV(showMsg=False)
            FloatMessage.FloatMessage("闹钟已更新", bg_color='#33cc33', text_color='#000000')
            self.parent_window.UI.logger.info(f"AlarmWidget - 更新闹钟：{self.ring_time}")

    def completeAlarm(self):
        """手动触发闹钟"""
        self.parent_window.triggerAlarm(self)

    def deleteAlarm(self):
        """删除闹钟"""
        reply = QMessageBox.question(
            self,
            "确认删除",
            f"确定要删除闹钟“{self.ring_time} - {self.remark}”吗？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.parent_window.removeAlarmWidget(self)


class AddAlarmDialog(QDialog):
    """新增闹钟对话框（无保留模式）"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("新增闹钟")
        self.setObjectName("AddAlarmDialog")
        self.resize(400, 350)
        self.initUI()

    def initUI(self):
        layout = QFormLayout(self)

        # 响铃时间：默认当前时间+1小时，去掉秒
        default_time = QTime.currentTime().addSecs(3600)
        default_time = QTime(default_time.hour(), default_time.minute())
        self.TimeEdit = QTimeEdit()
        self.TimeEdit.setDisplayFormat("HH:mm")
        self.TimeEdit.setTime(default_time)
        layout.addRow("响铃时间：", self.TimeEdit)

        # 循环模式
        self.LoopCombo = QComboBox()
        self.LoopCombo.addItems(["once", "daily", "weekly"])
        self.LoopCombo.currentTextChanged.connect(self.onLoopModeChanged)
        layout.addRow("重复模式：", self.LoopCombo)

        # 星期选择（仅 weekly 可见）
        self.WeekList = QListWidget()
        self.WeekList.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
        days = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
        for d in days:
            self.WeekList.addItem(d)
        self.WeekList.setMaximumHeight(100)
        self.WeekLabel = QLabel("选择星期：")
        self.WeekLabel.setVisible(False)
        self.WeekList.setVisible(False)
        layout.addRow(self.WeekLabel, self.WeekList)

        # 备注
        self.RemarkEdit = QLineEdit()
        layout.addRow("备注：", self.RemarkEdit)

        # 铃声选择
        self.MusicCombo = QComboBox()
        self.loadMusicFiles()
        layout.addRow("铃声：", self.MusicCombo)

        # 开关状态
        self.EnableCheck = QCheckBox("开启闹钟")
        self.EnableCheck.setChecked(True)
        layout.addRow(self.EnableCheck)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)

        self.onLoopModeChanged("once")

    def loadMusicFiles(self):
        audio_dir = MAIN_PATH / "MediaFile" / "Audio"
        self.MusicCombo.clear()
        self.MusicCombo.addItem("default")
        if audio_dir.exists():
            for file in audio_dir.glob("*.mp3"):
                self.MusicCombo.addItem(file.name)
        else:
            self.parent().UI.logger.warning("AddAlarmDialog - Audio directory not found")

    def onLoopModeChanged(self, mode):
        visible = (mode == "weekly")
        self.WeekLabel.setVisible(visible)
        self.WeekList.setVisible(visible)
        self.resize(400, 400 if visible else 350)

    def getData(self):
        week_days = ""
        if self.LoopCombo.currentText() == "weekly":
            selected_indexes = [item.row() for item in self.WeekList.selectedIndexes()]
            days_num = [i+1 for i in selected_indexes]
            week_days = ",".join(str(d) for d in days_num)

        return {
            'ring_time': self.TimeEdit.time().toString("HH:mm"),
            'loop_mode': self.LoopCombo.currentText(),
            'week_days': week_days,
            'remark': self.RemarkEdit.text().strip(),
            'ring_music': self.MusicCombo.currentText(),
            'enabled': self.EnableCheck.isChecked()
        }


class EditAlarmDialog(QDialog):
    """编辑闹钟对话框（无保留模式）"""

    def __init__(self, alarm_widget, parent=None):
        super().__init__(parent)
        self.widget = alarm_widget
        self.setWindowTitle("编辑闹钟")
        self.setObjectName("EditAlarmDialog")
        self.resize(400, 400)
        self.initUI()

    def initUI(self):
        layout = QFormLayout(self)

        time_parts = self.widget.ring_time.split(':')
        qtime = QTime(int(time_parts[0]), int(time_parts[1])) if len(time_parts) == 2 else QTime.currentTime()
        self.TimeEdit = QTimeEdit()
        self.TimeEdit.setDisplayFormat("HH:mm")
        self.TimeEdit.setTime(qtime)
        layout.addRow("响铃时间：", self.TimeEdit)

        self.LoopCombo = QComboBox()
        self.LoopCombo.addItems(["once", "daily", "weekly"])
        self.LoopCombo.setCurrentText(self.widget.loop_mode)
        self.LoopCombo.currentTextChanged.connect(self.onLoopModeChanged)
        layout.addRow("重复模式：", self.LoopCombo)

        self.WeekList = QListWidget()
        self.WeekList.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
        days = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
        for d in days:
            self.WeekList.addItem(d)
        self.WeekList.setMaximumHeight(100)
        self.WeekLabel = QLabel("选择星期：")
        self.WeekLabel.setVisible(self.widget.loop_mode == "weekly")
        self.WeekList.setVisible(self.widget.loop_mode == "weekly")

        if self.widget.week_days:
            selected = [int(x.strip()) for x in self.widget.week_days.split(',') if x.strip()]
            for i in range(7):
                if (i+1) in selected:
                    self.WeekList.item(i).setSelected(True)

        layout.addRow(self.WeekLabel, self.WeekList)

        self.RemarkEdit = QLineEdit(self.widget.remark)
        layout.addRow("备注：", self.RemarkEdit)

        self.MusicCombo = QComboBox()
        self.loadMusicFiles()
        index = self.MusicCombo.findText(self.widget.ring_music)
        if index >= 0:
            self.MusicCombo.setCurrentIndex(index)
        layout.addRow("铃声：", self.MusicCombo)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)

    def loadMusicFiles(self):
        audio_dir = MAIN_PATH / "MediaFile" / "Audio"
        self.MusicCombo.clear()
        self.MusicCombo.addItem("default")
        if audio_dir.exists():
            for file in audio_dir.glob("*.mp3"):
                self.MusicCombo.addItem(file.name)

    def onLoopModeChanged(self, mode):
        visible = (mode == "weekly")
        self.WeekLabel.setVisible(visible)
        self.WeekList.setVisible(visible)
        self.adjustSize()

    def getData(self):
        week_days = ""
        if self.LoopCombo.currentText() == "weekly":
            selected_indexes = [item.row() for item in self.WeekList.selectedIndexes()]
            days_num = [i+1 for i in selected_indexes]
            week_days = ",".join(str(d) for d in days_num)

        return {
            'ring_time': self.TimeEdit.time().toString("HH:mm"),
            'loop_mode': self.LoopCombo.currentText(),
            'week_days': week_days,
            'remark': self.RemarkEdit.text().strip(),
            'ring_music': self.MusicCombo.currentText(),
            'enabled': self.widget.enabled  # 开关状态不在此修改
        }
