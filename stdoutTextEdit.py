import sys
from PySide6.QtWidgets import (QPlainTextEdit, QFrame, QSizePolicy)
from PySide6.QtCore import (QObject, Signal)
from PySide6.QtGui import (QFont, QTextCursor)


class StdoutRedirect(QObject):

    instance = None

    stdoutWritten = Signal(str)

    def __new__(cls):
        if cls.instance is None:
            cls.instance = super(StdoutRedirect, cls).__new__(cls)
        return cls.instance

    def write(self, text):
        self.stdoutWritten.emit(text)
        print(text, end='', file=sys.__stdout__)

    def flush(self):
        pass


class StdoutTextEdit(QPlainTextEdit):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setReadOnly(True)
        font = QFont("Courier New")
        font.setStyleHint(QFont.TypeWriter)
        font.setFixedPitch(True)
        self.setFont(font)
        self.setStyleSheet("""background-color: rgb(15, 16, 17);
                           color: rgb(200, 200, 200);""")
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setFrameShadow(QFrame.Shadow.Plain)
        self.setLineWidth(0)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding,
                                 QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(2)
        self.setSizePolicy(sizePolicy)

        self.stdoutRedirect = StdoutRedirect()
        self.stdoutRedirect.stdoutWritten.connect(self.append_text)
        sys.stdout = self.stdoutRedirect

    def append_text(self, text):
        scrollBar = self.verticalScrollBar()
        atEnd = False
        if scrollBar.value() == scrollBar.maximum():
            atEnd = True
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        cursor.insertText(text)
        if atEnd:
            scrollBar.setValue(scrollBar.maximum())
