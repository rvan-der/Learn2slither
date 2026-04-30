from PySide6.QtWidgets import (QLabel, QWidget, QHBoxLayout,
                               QSizePolicy, QFrame, QDialogButtonBox,
                               QDialog, QGridLayout)
from PySide6.QtGui import (QPainter, QBrush, QFont)
from PySide6.QtCore import Qt


class ColorDisplay(QWidget):
    def __init__(self, width, height, color, parent=None):
        super().__init__(parent)
        self.setFixedWidth(width)
        self.setFixedHeight(height)
        self.br = QBrush(Qt.SolidPattern)
        self.br.setColor(color)
        self.painter = QPainter()

    def set_color(self, color):
        self.br.setColor(color)
        self.update()

    def paintEvent(self, event):
        self.painter.begin(self)
        self.painter.fillRect(event.rect(), self.br)
        self.painter.end()


class SubtitleLine(QWidget):
    def __init__(self, text, pointSize=9, parent=None):
        super().__init__(parent=parent)
        mainLayout = QHBoxLayout()
        mainLayout.setSpacing(4)
        mainLayout.setContentsMargins(0, 0, 0, 0)

        leftLine = QFrame(frameShape=QFrame.HLine, lineWidth=1)
        leftLine.setStyleSheet("color: rgb(125, 125, 125)")
        leftLine.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,
                               QSizePolicy.Ignored))
        leftLine.setFixedWidth(16)

        label = QLabel(text)
        label.setStyleSheet("color: rgb(125, 125, 125)")
        font = QFont()
        font.setPointSize(pointSize)
        label.setFont(font)

        rightLine = QFrame(frameShape=QFrame.HLine, lineWidth=1)
        rightLine.setStyleSheet("color: rgb(125, 125, 125)")
        rightLine.setSizePolicy(QSizePolicy(QSizePolicy.Expanding,
                                QSizePolicy.Ignored))

        mainLayout.addWidget(leftLine)
        mainLayout.addWidget(label)
        mainLayout.addWidget(rightLine)
        self.setLayout(mainLayout)


class MessagePopup(QDialog):
    def __init__(self, text, color=None, parent=None):
        super().__init__(parent=parent, f=Qt.Popup)
        print("hello popup")
        self.setAttribute(Qt.WA_StyledBackground, True)
        style = """QDialog{background-color: rgb(40, 48, 56);
border: 2px ridge grey}"""
        if color is not None:
            style += "\nQLabel {color: " + color + "}"
        self.setStyleSheet(style)

        layout = QGridLayout()

        label = QLabel(text)
        font = QFont("Courier New")
        font.setStyleHint(QFont.TypeWriter)
        font.setFixedPitch(True)
        label.setFont(font)
        layout.addWidget(label, 0, 0, alignment=Qt.AlignCenter)

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        self.finished.connect(self.deleteLater)
        layout.addWidget(buttonBox, 1, 0, alignment=Qt.AlignCenter)
        self.setLayout(layout)
