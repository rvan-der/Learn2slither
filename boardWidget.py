from enums import Tile as Tl
from uiElements import ColorDisplay
from PySide6.QtWidgets import (QWidget, QGridLayout, QSpacerItem, QSizePolicy,
                               QHBoxLayout, QLabel)
from PySide6.QtGui import (QColor, QFont)
from PySide6.QtCore import (Qt, Slot)


class BoardWidget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.colors = {
            Tl.WALL: QColor(45, 45, 45),
            Tl.EMPTY: QColor(60, 60, 60),
            Tl.RED: QColor(255, 0, 0),
            Tl.GREEN: QColor(0, 255, 0),
            Tl.HEAD: QColor(0, 0, 178),
            Tl.BODY: QColor(0, 0, 255),
            'idle': QColor(50, 50, 50)
        }

        self.setSizePolicy(QSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        )
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet("background-color: rgb(18, 22, 25)")

        self.timerLabel = QLabel("T :")
        self.timerLabel.setFont(QFont("Sans Serif", 12, 600))
        self.timerValueLabel = QLabel("0")
        self.timerValueLabel.setFont(QFont("Sans Serif", 12, 600))
        self.timerLayout = QHBoxLayout()
        self.timerLayout.setContentsMargins(10, 0, 0, 0)
        self.timerLayout.addWidget(self.timerLabel)
        self.timerLayout.addWidget(self.timerValueLabel)
        self.timerLayout.addSpacerItem(QSpacerItem(
            0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum
        ))
        self.timerWidget = QWidget()
        self.timerWidget.setLayout(self.timerLayout)

        self.lengthLabel = QLabel("L :")
        self.lengthLabel.setFont(QFont("Sans Serif", 12, 600))
        self.lengthValueLabel = QLabel("0")
        self.lengthValueLabel.setFont(QFont("Sans Serif", 12, 600))
        self.lengthLayout = QHBoxLayout()
        self.lengthLayout.setContentsMargins(10, 0, 0, 0)
        self.lengthLayout.addWidget(self.lengthLabel)
        self.lengthLayout.addWidget(self.lengthValueLabel)
        self.lengthLayout.addSpacerItem(QSpacerItem(
            0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum
        ))
        self.lengthWidget = QWidget()
        self.lengthWidget.setLayout(self.lengthLayout)

        self.mainLayout = QGridLayout(self)
        self.mainLayout.setContentsMargins(10, 10, 10, 10)
        self.mainLayout.setSpacing(1)
        self.setLayout(self.mainLayout)

        self.mainLayout.addItem(
            QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum),
            0, 0
        )
        self.mainLayout.addItem(
            QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum),
            13, 13
        )
        self.mainLayout.addItem(
            QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding),
            13, 0
        )
        self.mainLayout.addItem(
            QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding),
            0, 13
        )

        self.mainLayout.addWidget(self.timerWidget, 1, 13)
        self.mainLayout.addWidget(self.lengthWidget, 2, 13)

        self.cells = []
        for y in range(1, 13):
            for x in range(1, 13):
                cell = ColorDisplay(22, 22, self.colors['idle'])
                self.cells.append(cell)
                self.mainLayout.addWidget(cell, y, x)

    @Slot(int, int, Tl)
    def update_cell(self, x, y, tile):
        i = 12 * y + x
        self.cells[i].set_color(self.colors[tile])

    @Slot(int)
    def set_timer(self, time):
        self.timerValueLabel.setText(str(time))

    @Slot(int)
    def set_length(self, length):
        self.lengthValueLabel.setText(str(length))

    @Slot()
    def clear_display(self):
        self.timerValueLabel.setText("0")
        self.lengthValueLabel.setText("0")
        for cell in self.cells:
            cell.set_color(self.colors['idle'])

    @Slot(list)
    def set_agent_color(self, color):
        self.colors[Tl.HEAD] = QColor(*[c * 0.7 for c in color])
        self.colors[Tl.BODY] = QColor(*color)
