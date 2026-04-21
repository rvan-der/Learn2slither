from PySide6.QtWidgets import (QWidget, QGridLayout, QLabel,
                               QSpacerItem, QSizePolicy)
from PySide6.QtCore import Qt
from enums import Tile as Tl


class BoardWidget(QWidget):

    def __init__(self, environment, parent=None):
        super().__init__(parent)
        self.environment = environment
        self.colors = {
            Tl.WALL: [45, 45, 45],
            Tl.EMPTY: [60, 60, 60],
            Tl.RED: [255, 0, 0],
            Tl.GREEN: [0, 255, 0],
            Tl.HEAD: [0, 0, 178],
            Tl.BODY: [0, 0, 255]
        }
        self.cells = []

        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet("background-color: rgb(20, 24, 28)")

        self.layout = QGridLayout(self)
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.layout.setSpacing(1)
        self.setLayout(self.layout)

        hSpace = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
        hSpace2 = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.layout.addItem(hSpace, 0, 0)
        self.layout.addItem(hSpace2, environment.height + 3,
                            environment.width + 3)
        vSpace = QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)
        vSpace2 = QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.layout.addItem(vSpace, environment.height + 3, 0)
        self.layout.addItem(vSpace2, 0, environment.width + 3)

        for y in range(1, environment.height + 3):
            for x in range(1, environment.width + 3):
                cell = QLabel(self)
                cell.setMinimumSize(20, 20)
                self.cells.append(cell)
                self.layout.addWidget(cell, y, x)

    def update_cell(self, x, y, tile):
        color = self.colors[tile]
        self.cells[(self.environment.width + 2) * y + x].setStyleSheet(
            f"background-color: rgb({color[0]}, {color[1]}, {color[2]});"
            )

    def set_snake_colors(self, head_color, body_color):
        self.colors[Tl.HEAD] = head_color
        self.colors[Tl.BODY] = body_color
