from PySide6.QtWidgets import (QWidget, QSizePolicy, QGridLayout,
                               QPushButton, QLabel, QSpinBox,
                               QSpacerItem, QHBoxLayout)


class AgentsToolBoxWidget(QWidget):

    def __init__(self, agent, toolBox=None):
        super().__init__()
        self.agent = agent
        self.toolBox = toolBox

        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding,
                                 QSizePolicy.Policy.Preferred)
        self.setSizePolicy(sizePolicy)

        self.mainLayout = QGridLayout(self)
        self.mainLayout.setSpacing(6)
        self.mainLayout.setContentsMargins(6, 0, 6, 0)

        self.trainWidget = QWidget()
        self.trainLayout = QHBoxLayout()
        self.trainLayout.setSpacing(3)
        self.trainLayout.setContentsMargins(0, 0, 0, 0)

        self.trainButton = QPushButton("Train")
        self.trainButton.clicked.connect(self.trainAgent)

        self.episodesSpinBox = QSpinBox()
        self.episodesSpinBox.setRange(1, 100000)
        self.episodesSpinBox.setValue(1)
        self.episodesSpinBox.returnPressed.connect(
            self.trainAgent
        )

        episodesLabel = QLabel("episodes")

        trainHSpacer = QSpacerItem(0, 0, QSizePolicy.Expanding,
                                   QSizePolicy.Minimum)

        self.trainLayout.addWidget(self.trainButton)
        self.trainLayout.addWidget(self.episodesSpinBox)
        self.trainLayout.addWidget(episodesLabel)
        self.trainLayout.addItem(trainHSpacer)

        self.trainWidget.setLayout(self.trainLayout)

        self.playWidget = QWidget()
        self.playLayout = QHBoxLayout()
        self.playLayout.setSpacing(3)
        self.playLayout.setContentsMargins(0, 0, 0, 0)

        self.playButton = QPushButton("Play")
        self.playButton.clicked.connect(self.playAgent)

        self.gamesSpinBox = QSpinBox()
        self.gamesSpinBox.setRange(1, 100000)
        self.gamesSpinBox.setValue(1)
        self.gamesSpinBox.returnPressed.connect(
            self.playAgent
        )

        gamesLabel = QLabel("games")

        playHSpacer = QSpacerItem(0, 0, QSizePolicy.Expanding,
                                  QSizePolicy.Minimum)

        self.playLayout.addWidget(self.playButton)
        self.playLayout.addWidget(self.gamesSpinBox)
        self.playLayout.addWidget(gamesLabel)
        self.playLayout.addItem(playHSpacer)

        self.playWidget.setLayout(self.playLayout)

        mainVSpacer = QSpacerItem(0, 0, QSizePolicy.Minimum,
                                  QSizePolicy.Expanding)

        self.mainLayout.addWidget(self.trainWidget, 0, 0)
        self.mainLayout.addWidget(self.playWidget, 1, 0)
        self.mainLayout.addItem(mainVSpacer, 2, 0)

    def trainAgent(self):
        self.toolBox.trainAgentSignal.emit(
            self.agent, self.episodesSpinBox.value())

    def playAgent(self):
        self.toolBox.playAgentSignal.emit(
            self.agent, self.gamesSpinBox.value())
