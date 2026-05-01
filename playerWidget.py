from PySide6.QtWidgets import (QWidget, QSizePolicy, QGridLayout,
                               QHBoxLayout, QPushButton, QComboBox,
                               QLabel)
from PySide6.QtGui import QIcon
from PySide6.QtCore import (QSize, Qt, Signal, Slot)
import resources_rc  # noqa


class PlayerWidget(QWidget):

    pausedChanged = Signal(bool)
    delayChanged = Signal(float)

    def __init__(self):
        super().__init__()
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding,
                                 QSizePolicy.Policy.Preferred)
        self.setSizePolicy(sizePolicy)

        self.playerLayout = QGridLayout(self)
        self.playerLayout.setSpacing(0)
        self.playerLayout.setContentsMargins(8, 0, 8, 6)

        self.cancelButton = QPushButton()
        self.cancelButton.setIconSize(QSize(22, 22))
        self.cancelButton.setIcon(QIcon(":/assets/cancel_icon.png"))
        self.cancelButton.setFlat(True)
        self.cancelButton.setToolTip(
            '<span style="color:white;">Cancel</span>'
        )
        self.playerLayout.addWidget(self.cancelButton, 0, 0,
                                    alignment=Qt.AlignLeft)

        self.pauseIcon = QIcon(":/assets/pause_icon.png")
        self.playIcon = QIcon(":/assets/play_icon.png")
        self.paused = True
        self.playPauseButton = QPushButton()
        self.playPauseButton.setIconSize(QSize(25, 25))
        self.playPauseButton.setIcon(self.playIcon)
        self.playPauseButton.setFlat(True)
        self.playPauseButton.clicked.connect(self.toggle_paused)
        self.playerLayout.addWidget(self.playPauseButton, 0, 1,
                                    alignment=Qt.AlignRight)

        self.nextFrameButton = QPushButton()
        self.nextFrameButton.setIconSize(QSize(25, 25))
        self.nextFrameButton.setIcon(QIcon(":/assets/next_frame_icon.png"))
        self.nextFrameButton.setFlat(True)
        self.nextFrameButton.setEnabled(False)
        self.nextFrameButton.setToolTip(
            '<span style="color:white;">Next frame</span>'
        )
        self.playerLayout.addWidget(self.nextFrameButton, 0, 2,
                                    alignment=Qt.AlignLeft)

        self.fpsWidget = QWidget()
        self.fpsLayout = QHBoxLayout()
        self.fpsLayout.setSpacing(1)
        self.fpsLayout.setContentsMargins(0, 0, 0, 0)
        self.fpsWidget.setLayout(self.fpsLayout)
        self.fpsLAbel = QLabel("fps:")
        self.fpsLayout.addWidget(self.fpsLAbel)

        self.fpsComboBox = QComboBox()
        self.fpsComboBox.addItem("1", userData=1.0)
        self.fpsComboBox.addItem("2", userData=0.5)
        self.fpsComboBox.addItem("5", userData=0.2)
        self.fpsComboBox.addItem("10", userData=0.1)
        self.fpsComboBox.addItem("20", userData=0.05)
        self.fpsComboBox.addItem("50", userData=0.02)
        self.fpsComboBox.currentIndexChanged.connect(self.fps_changed)
        self.fpsLayout.addWidget(self.fpsComboBox)

        self.playerLayout.addWidget(self.fpsWidget, 0, 3,
                                    alignment=Qt.AlignRight)

        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet("background-color: rgb(18, 22, 25);")

    @Slot(int)
    def fps_changed(self, index):
        self.delayChanged.emit(self.fpsComboBox.itemData(index))

    def toggle_paused(self):
        self.set_paused(not self.paused)

    def set_paused(self, paused):
        self.paused = paused
        if self.paused:
            self.playPauseButton.setIcon(self.playIcon)
            self.nextFrameButton.setEnabled(True)
        else:
            self.playPauseButton.setIcon(self.pauseIcon)
            self.nextFrameButton.setEnabled(False)
        self.pausedChanged.emit(self.paused)
