import os
from uiElements import MessagePopup
from agent import AgentFactory
from agentsToolBoxWidget import AgentsToolBoxWidget
from PySide6.QtWidgets import (QToolBox, QSizePolicy)
from PySide6.QtGui import (QIcon, QPixmap, QColor)
from PySide6.QtCore import (Signal)


class AgentsToolBox(QToolBox):

    trainAgentSignal = Signal(str, int)
    playAgentSignal = Signal(str, int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.factory = AgentFactory()
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding,
                                 QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(7)
        self.setSizePolicy(sizePolicy)

        self.files = []

    def add_agent(self, filepath):
        if filepath in self.files:
            print(f"[WARNING] file '{filepath}' already loaded, " +
                  "nothing was done.")
            return
        print(f"[LOADING] agent file: '{filepath}'")
        agentInfo = None
        try:
            agentInfo = self.factory.info_from_file(filepath)
        except Exception as e:
            print(f"[ERROR] file '{filepath}':\n{e}")
            print(f"[WARNING]: file '{filepath}' hasn't been added.")
            return
        pixmap = QPixmap(100, 100)
        pixmap.fill(QColor(*agentInfo['color']))
        widget = AgentsToolBoxWidget(filepath, agentInfo, self)
        self.addItem(widget, QIcon(pixmap), agentInfo['name'])
        self.files.append(filepath)

    def delete_agent(self, filepath):
        widget = self.currentWidget()
        try:
            os.remove(filepath)
        except Exception as e:
            msgPopup = MessagePopup(
                f"Couldn't delete '{filepath}':\n{e}", "red", self
            )
            msgPopup.finished.connect(msgPopup.deleteLater)
            msgPopup.open()
            return
        self.removeItem(self.currentIndex())
        self.files.remove(filepath)
        widget.deleteLater()

    def copy_agent(self, srcFile, destFile):
        try:
            agent = self.factory.agent_from_file(srcFile)
            agent.save_to_file(destFile)
        except Exception as e:
            msgPopup = MessagePopup(
                f"Couldn't copy the agent:\n{e}", "red", self
            )
            msgPopup.finished.connect(msgPopup.deleteLater)
            msgPopup.open()
            return
        self.add_agent(destFile)
