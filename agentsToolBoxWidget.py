from uiElements import (SubtitleLine, MessagePopup)
from enums import Status as St
from agent import AgentFactory
from PySide6.QtWidgets import (QWidget, QSizePolicy, QGridLayout,
                               QPushButton, QLabel, QSpinBox,
                               QSpacerItem, QHBoxLayout, QVBoxLayout,
                               QDialog, QLineEdit, QFileDialog,
                               QDialogButtonBox)
from PySide6.QtCore import (Qt, Slot, QSize)
from PySide6.QtGui import QIcon
import resources_rc  # noqa


class ModelInfoPopup(QDialog):
    def __init__(self, info, parent=None):
        super().__init__(parent=parent)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setWindowTitle("Model")
        self.setStyleSheet("""QWidget {background-color: rgb(40, 48, 56)}
QDialog {border: 2px ridge grey}""")

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
        mainLayout.addWidget(tdnLabel, 1, 0, alignment=Qt.AlignRight)
        mainLayout.addWidget(
            QLabel(f"{info['td_n']}"),
            1, 1,
            alignment=Qt.AlignLeft
        )
        mainLayout.addWidget(alphaLabel, 1, 3, alignment=Qt.AlignRight)
        mainLayout.addWidget(
            QLabel(f"{info['alpha']}"),
            1, 4,
            alignment=Qt.AlignLeft
        )
        mainLayout.addWidget(epsilonLabel, 2, 0, alignment=Qt.AlignRight)
        mainLayout.addWidget(
            QLabel(f"{info['epsilon']}"),
            2, 1,
            alignment=Qt.AlignLeft
        )
        mainLayout.addWidget(gammaLabel, 2, 3, alignment=Qt.AlignRight)
        mainLayout.addWidget(
            QLabel(f"{info['gamma']}"),
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
            QLabel("alive:"), 5, 0, alignment=Qt.AlignRight
        )
        mainLayout.addWidget(
            QLabel(f"{info['alive']}"),
            5, 1, alignment=Qt.AlignLeft
        )
        mainLayout.addWidget(
            QLabel("dead:"), 5, 3, alignment=Qt.AlignRight
        )
        mainLayout.addWidget(
            QLabel(f"{info['dead']}"),
            5, 4, alignment=Qt.AlignLeft
        )
        mainLayout.addWidget(
            QLabel("green:"), 6, 0, alignment=Qt.AlignRight
        )
        mainLayout.addWidget(
            QLabel(f"{info['green']}"),
            6, 1, alignment=Qt.AlignLeft
        )
        mainLayout.addWidget(
            QLabel("red:"), 6, 3, alignment=Qt.AlignRight
        )
        mainLayout.addWidget(
            QLabel(f"{info['red']}"),
            6, 4, alignment=Qt.AlignLeft
        )
        mainLayout.addWidget(targetLenLabel, 7, 0, alignment=Qt.AlignLeft)
        mainLayout.addWidget(
            QLabel(f"{info['target_len']}"),
            7, 1, alignment=Qt.AlignRight
        )
        mainLayout.addWidget(penaltyLabel, 7, 3, alignment=Qt.AlignLeft)
        mainLayout.addWidget(
            QLabel(f"{info['penalty']}"),
            7, 4, alignment=Qt.AlignRight
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
        self.episodesSpinBox.setRange(1, 1000000)
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
        self.gamesSpinBox.setRange(1, 1000000)
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

        fileLineEdit = QLineEdit()
        fileLineEdit.setText(self.filepath)
        fileLineEdit.setReadOnly(True)
        fileLineEdit.setStyleSheet(
            """QLineEdit {background-color: rgb(60, 72, 90);
border-radius: 4px}"""
        )

        copyButton = QPushButton()
        copyButton.setIcon(QIcon(":/assets/copy_icon.png"))
        copyButton.setIconSize(QSize(20, 20))
        copyButton.setToolTip("Copy snake")

        deleteButton = QPushButton()
        deleteButton.setIcon(QIcon(":/assets/delete_icon.png"))
        deleteButton.setIconSize(QSize(20, 20))
        deleteButton.setToolTip("/!\\ Delete snake /!\\")

        fileLayout = QHBoxLayout()
        fileLayout.addWidget(fileLineEdit)
        fileLayout.addWidget(copyButton)
        fileLayout.addWidget(deleteButton)

        fileWidget = QWidget()
        fileWidget.setLayout(fileLayout)

        mainLayout = QVBoxLayout(self)
        mainLayout.setSpacing(6)
        mainLayout.setContentsMargins(6, 0, 6, 0)
        mainLayout.addWidget(SubtitleLine("Actions"))
        mainLayout.addWidget(trainWidget)
        mainLayout.addWidget(playWidget)
        mainLayout.addSpacing(15)
        mainLayout.addWidget(SubtitleLine("Info"))
        mainLayout.addWidget(infoWidget)
        mainLayout.addSpacing(15)
        mainLayout.addWidget(SubtitleLine("File"))
        mainLayout.addWidget(fileWidget)
        mainLayout.addSpacerItem(QSpacerItem(
            0, 0,
            QSizePolicy.Preferred,
            QSizePolicy.Expanding
        ))
        self.setLayout(mainLayout)

        trainButton.clicked.connect(self.trainAgent)
        modelInfoButton.clicked.connect(self.model_info)
        copyButton.clicked.connect(self.select_file)
        deleteButton.clicked.connect(self.delete_agent)

    @Slot(int)
    def update_sessions(self, sessions):
        self.agentInfo['sessions'] = sessions
        self.sessionsLabel.setText(
            f"Training sessions: {sessions}"
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
            self.gamesSpinBox.value()
        )

    @Slot()
    def delete_agent(self):
        msgPopup = MessagePopup(
            f"""Are you sure you want to delete {self.agentInfo['name']} ?
file: {self.filepath}""",
            "red",
            self,
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            "/!\\ Attention /!\\"
        )
        msgPopup.accepted.connect(self.toolBox.deleteAgentSignal.emit)
        msgPopup.finished.connect(msgPopup.deleteLater)
        msgPopup.open()

    @Slot()
    def select_file(self):
        dialog = QFileDialog(self)
        dialog.setDefaultSuffix("l2s")
        dialog.setNameFilter("*.l2s")
        dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)
        dialog.fileSelected.connect(self.copy_file)
        dialog.open()

    def copy_file(self, destFile):
        self.toolBox.copyAgentSignal.emit(self.filepath, destFile)

    @Slot()
    def model_info(self):
        popup = ModelInfoPopup(self.agentInfo, parent=self)
        popup.finished.connect(popup.deleteLater)
        popup.open()
