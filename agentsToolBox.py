from PySide6.QtWidgets import (QToolBox, QSizePolicy)
from PySide6.QtGui import (QIcon, QPixmap, QColor)
from PySide6.QtCore import (Signal)
from agent import Agent
from agentsToolBoxWidget import AgentsToolBoxWidget


class AgentsToolBox(QToolBox):

    trainAgentSignal = Signal(Agent, int)

    def __init__(self, parent=None):
        super().__init__(parent)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding,
                                 QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(7)
        self.setSizePolicy(sizePolicy)

    def addAgent(self, agent):
        pixmap = QPixmap(20, 20)
        pixmap.fill(QColor(*agent.color))
        widget = AgentsToolBoxWidget(agent, toolBox=self)
        self.addItem(widget, QIcon(pixmap), agent.name)
