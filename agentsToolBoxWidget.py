from PySide6.QtWidgets import (QWidget, QSizePolicy, QGridLayout,
                               QPushButton, QLabel, QSpinBox)


class AgentsToolBoxWidget(QWidget):

    def __init__(self, agent, toolBox=None):
        super().__init__()
        self.agent = agent
        self.toolBox = toolBox
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding,
                                 QSizePolicy.Policy.Expanding)
        self.setSizePolicy(sizePolicy)
        self.layout = QGridLayout(self)
        self.layout.setSpacing(4)
        self.layout.setContentsMargins(6, 6, 6, 6)
        self.trainButton = QPushButton("Train")
        self.trainButton.clicked.connect(self.trainAgent)
        self.layout.addWidget(self.trainButton, 0, 0)
        self.episodesLabel = QLabel("episodes: ")
        self.episodesSpinBox = QSpinBox()
        self.episodesSpinBox.setRange(1, 100000)
        self.episodesSpinBox.setValue(100)
        self.layout.addWidget(self.episodesLabel, 0, 1)
        self.layout.addWidget(self.episodesSpinBox, 0, 2)

    def trainAgent(self):
        print(self.parent().__class__.__name__)
        self.toolBox.trainAgentSignal.emit(
            self.agent, self.episodesSpinBox.value())
