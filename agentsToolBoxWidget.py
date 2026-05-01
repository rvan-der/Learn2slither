from uiElements import SubtitleLine
from enums import Status as St
from agent import AgentFactory
from PySide6.QtWidgets import (QWidget, QSizePolicy, QGridLayout,
                               QPushButton, QLabel, QSpinBox,
                               QSpacerItem, QHBoxLayout, QVBoxLayout,
                               QDialog)
from PySide6.QtCore import (Qt, Slot)


class ModelInfoPopup(QDialog):
    def __init__(self, agent, parent=None):
        super().__init__(parent=parent)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet("""QDialog{background-color: rgb(40, 48, 56);
border: 2px ridge grey}""")

        tdnLabel = QLabel("td_n:")
        tdnLabel.setToolTip("Temporal difference degree")
        alphaLabel = QLabel("alpha:")
        alphaLabel.setToolTip("Learning rate")
        epsilonLabel = QLabel("epsilon:")
        epsilonLabel.setToolTip("Exploration rate")
        gammaLabel = QLabel("gamma:")
        gammaLabel.setToolTip("Discount factor")

        targetLenLabel = QLabel("target length:")
        targetLenLabel.setToolTip(
            """The snake's length after which the
penalty isn't applied anymore.""")
        penaltyLabel = QLabel("penalty:")
        penaltyLabel.setToolTip(
            """This penalty is applied to all scores except for green
while the snake is under the target length.""")

        mainLayout = QGridLayout()
        mainLayout.setContentsMargins(20, 20, 20, 20)
        mainLayout.setSpacing(20)
        mainLayout.addWidget(
            SubtitleLine("Learning parameters"),
            0, 0, 1, 5,
            alignment=Qt.AlignBottom
        )
        mainLayout.addWidget(tdnLabel, 1, 0, alignment=Qt.AlignLeft)
        mainLayout.addWidget(
            QLabel(f"{agent.td_n}"),
            1, 1,
            alignment=Qt.AlignLeft
        )
        mainLayout.addWidget(alphaLabel, 1, 3, alignment=Qt.AlignLeft)
        mainLayout.addWidget(
            QLabel(f"{agent.alpha}"),
            1, 4,
            alignment=Qt.AlignLeft
        )
        mainLayout.addWidget(epsilonLabel, 2, 0, alignment=Qt.AlignLeft)
        mainLayout.addWidget(
            QLabel(f"{agent.epsilon}"),
            2, 1,
            alignment=Qt.AlignLeft
        )
        mainLayout.addWidget(gammaLabel, 2, 3, alignment=Qt.AlignLeft)
        mainLayout.addWidget(
            QLabel(f"{agent.gamma}"),
            2, 4,
            alignment=Qt.AlignLeft
        )
        mainLayout.addItem(QSpacerItem(
            0, 20,
            QSizePolicy.Preferred, QSizePolicy.Fixed
        ), 3, 0)
        mainLayout.addWidget(
            SubtitleLine("Reward structure"),
            4, 0, 1, 5,
            alignment=Qt.AlignBottom
        )
        mainLayout.addWidget(
            QLabel("alive:"), 5, 0, alignment=Qt.AlignLeft
        )
        mainLayout.addWidget(
            QLabel(f"{agent.rewards.rewards[St.ALIVE]}"),
            5, 1, alignment=Qt.AlignLeft
        )
        mainLayout.addWidget(
            QLabel("dead:"), 5, 3, alignment=Qt.AlignLeft
        )
        mainLayout.addWidget(
            QLabel(f"{agent.rewards.rewards[St.DEAD]}"),
            5, 4, alignment=Qt.AlignLeft
        )
        mainLayout.addWidget(
            QLabel("green:"), 6, 0, alignment=Qt.AlignLeft
        )
        mainLayout.addWidget(
            QLabel(f"{agent.rewards.rewards[St.GREEN]}"),
            6, 1, alignment=Qt.AlignLeft
        )
        mainLayout.addWidget(
            QLabel("red:"), 6, 3, alignment=Qt.AlignLeft
        )
        mainLayout.addWidget(
            QLabel(f"{agent.rewards.rewards[St.RED]}"),
            6, 4, alignment=Qt.AlignLeft
        )
        mainLayout.addWidget(targetLenLabel, 7, 0, alignment=Qt.AlignLeft)
        mainLayout.addWidget(
            QLabel(f"{agent.rewards.target_len}"),
            7, 1, alignment=Qt.AlignLeft
        )
        mainLayout.addWidget(penaltyLabel, 7, 3, alignment=Qt.AlignLeft)
        mainLayout.addWidget(
            QLabel(f"{agent.rewards.penalty}"),
            7, 4, alignment=Qt.AlignLeft
        )

        self.setLayout(mainLayout)


class AgentsToolBoxWidget(QWidget):
    def __init__(self, filepath, agentInfo, toolBox):
        super().__init__()
        self.filepath = filepath
        self.toolBox = toolBox
        self.factory = AgentFactory()
        self.agentInfo = agentInfo

        self.setSizePolicy(QSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Preferred
        ))

        trainButton = QPushButton("Train")

        self.episodesSpinBox = QSpinBox()
        self.episodesSpinBox.setRange(1, 100000)
        self.episodesSpinBox.setValue(1)
        self.episodesSpinBox.setAccelerated(True)
        self.episodesSpinBox.returnPressed.connect(
            self.trainAgent
        )

        trainLayout = QHBoxLayout()
        trainLayout.setSpacing(3)
        trainLayout.setContentsMargins(0, 0, 0, 0)
        trainLayout.addWidget(trainButton)
        trainLayout.addWidget(self.episodesSpinBox)
        trainLayout.addWidget(QLabel("episodes"))
        trainLayout.addSpacerItem(QSpacerItem(
            0, 0,
            QSizePolicy.Expanding,
            QSizePolicy.Preferred
        ))

        trainWidget = QWidget()
        trainWidget.setLayout(trainLayout)

        self.playButton = QPushButton("Play")
        self.playButton.clicked.connect(self.playAgent)

        self.gamesSpinBox = QSpinBox()
        self.gamesSpinBox.setRange(1, 100000)
        self.gamesSpinBox.setValue(1)
        self.gamesSpinBox.setAccelerated(True)
        self.gamesSpinBox.returnPressed.connect(
            self.playAgent
        )

        self.playLayout = QHBoxLayout()
        self.playLayout.setSpacing(3)
        self.playLayout.setContentsMargins(0, 0, 0, 0)
        self.playLayout.addWidget(self.playButton)
        self.playLayout.addWidget(self.gamesSpinBox)
        self.playLayout.addWidget(QLabel("games"))
        self.playLayout.addSpacerItem(QSpacerItem(
            0, 0,
            QSizePolicy.Expanding,
            QSizePolicy.Preferred
        ))

        playWidget = QWidget()
        playWidget.setLayout(self.playLayout)

        self.sessionsLabel = QLabel(
            f"Training sessions: {self.agentInfo['sessions']}"
        )

        modelInfoButton = QPushButton("model")

        infoLayout = QHBoxLayout()
        infoLayout.setContentsMargins(0, 0, 0, 0)
        infoLayout.addWidget(self.sessionsLabel, alignment=Qt.AlignLeft)
        infoLayout.addWidget(modelInfoButton, alignment=Qt.AlignRight)
        infoWidget = QWidget()
        infoWidget.setLayout(infoLayout)

        mainLayout = QVBoxLayout(self)
        mainLayout.setSpacing(6)
        mainLayout.setContentsMargins(6, 0, 6, 0)
        mainLayout.addWidget(SubtitleLine("Actions"))
        mainLayout.addWidget(trainWidget)
        mainLayout.addWidget(playWidget)
        mainLayout.addSpacing(10)
        mainLayout.addWidget(SubtitleLine("Info"))
        mainLayout.addWidget(infoWidget)
        mainLayout.addSpacerItem(QSpacerItem(
            0, 0,
            QSizePolicy.Preferred,
            QSizePolicy.Expanding
        ))
        self.setLayout(mainLayout)

        trainButton.clicked.connect(self.trainAgent)
        modelInfoButton.clicked.connect(self.model_info)

    @Slot()
    def increment_sessions(self):
        self.agentInfo['sessions'] += 1
        self.sessionsLabel.setText(
            f"Training sessions: {self.agentInfo['sessions']}"
        )

    @Slot()
    def trainAgent(self):
        self.toolBox.trainAgentSignal.emit(
            self.filepath,
            self.episodesSpinBox.value()
        )

    @Slot()
    def playAgent(self):
        self.toolBox.playAgentSignal.emit(
            self.filepath,
            self.episodesSpinBox.value()
        )

    @Slot()
    def model_info(self):
        popup = ModelInfoPopup(self.agent, parent=self)
        popup.finished.connect(popup.deleteLater)
        popup.open()
