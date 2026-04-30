from enums import Tile as Tl
from uiElements import ColorDisplay
from PySide6.QtWidgets import (QWidget, QGridLayout, QSpacerItem, QSizePolicy)
from PySide6.QtGui import QColor
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

    @Slot()
    def clear_display(self):
        for cell in self.cells:
            cell.set_color(self.colors['idle'])

    def set_agent_color(self, color):
        self.colors[Tl.HEAD] = QColor(*[c * 0.7 for c in color])
        self.colors[Tl.BODY] = QColor(*color)
