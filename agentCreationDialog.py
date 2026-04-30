from PySide6.QtWidgets import (QDialog, QVBoxLayout, QDialogButtonBox,
                               QLabel, QLineEdit, QSpinBox, QWidget,
                               QHBoxLayout, QDoubleSpinBox, QSizePolicy,
                               QGridLayout, QPushButton, QCheckBox,
                               QSpacerItem, QFileDialog)
from PySide6.QtGui import (QIcon, QValidator, QColor)
from PySide6.QtCore import (Signal, Qt, QSize)
from uiElements import (MessagePopup, ColorDisplay, SubtitleLine)
from agent import (Agent, AgentFactory)
from rewards import RewardStructure
import resources_rc  # noqa


class NameValidator(QValidator):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

    def validate(self, input, pos):
        if input == "":
            return QValidator.State.Intermediate
        if not input.isalnum():
            return QValidator.State.Invalid
        return QValidator.State.Acceptable


class AgentCreationDialog(QDialog):

    agentCreated = Signal(str)
    factory = AgentFactory()

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setWindowTitle("Agent creation")
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet("""
QWidget {background-color: rgb(40, 48, 56)}
QSpinBox, QLineEdit, QDoubleSpinBox {background-color: rgb(60, 72, 90)}
QDialog {border: 2px ridge grey}""")

        self.randomButton = QPushButton()
        self.randomButton.setIcon(QIcon(":/assets/dice_icon.png"))
        self.randomButton.setIconSize(QSize(22, 22))
        self.randomButton.setToolTip("Random personality")

        self.nameLineEdit = QLineEdit()
        self.nameLineEdit.setMaxLength(20)
        self.nameLineEdit.setValidator(NameValidator())
        self.nameLineEdit.setText(AgentFactory.random_name())

        color = AgentFactory.random_color()
        self.RSpinbox = QSpinBox()
        self.RSpinbox.setRange(0, 255)
        self.RSpinbox.setValue(color[0])
        self.GSpinbox = QSpinBox()
        self.GSpinbox.setRange(0, 255)
        self.GSpinbox.setValue(color[1])
        self.BSpinbox = QSpinBox()
        self.BSpinbox.setRange(0, 255)
        self.BSpinbox.setValue(color[2])
        self.colorDisplay = ColorDisplay(20, 20, QColor(*color))

        personalityLayout = QHBoxLayout()
        personalityLayout.setSpacing(5)
        personalityLayout.setContentsMargins(20, 0, 20, 0)
        personalityLayout.addWidget(self.randomButton)
        personalityLayout.addSpacing(20)
        personalityLayout.addWidget(QLabel("name:"))
        personalityLayout.addWidget(self.nameLineEdit)
        personalityLayout.addSpacing(20)
        personalityLayout.addWidget(QLabel("color(RGB):"))
        personalityLayout.addWidget(self.RSpinbox)
        personalityLayout.addWidget(self.GSpinbox)
        personalityLayout.addWidget(self.BSpinbox)
        personalityLayout.addSpacing(8)
        personalityLayout.addWidget(
            self.colorDisplay,
            alignment=Qt.AlignVCenter
        )

        personalityWidget = QWidget()
        personalityWidget.setLayout(personalityLayout)

        self.paramsResetButton = QPushButton()
        self.paramsResetButton.setIcon(QIcon(":/assets/reset_icon.png"))
        self.paramsResetButton.setIconSize(QSize(20, 20))
        self.paramsResetButton.setToolTip("Reset learning parameters")

        tdnLabel = QLabel("td_N:")
        tdnLabel.setToolTip("Temporal difference degree")
        self.tdnSpinBox = QSpinBox()
        self.tdnSpinBox.setRange(1, 100)
        self.tdnSpinBox.setValue(1)

        alphaLabel = QLabel("alpha:")
        alphaLabel.setToolTip("Learning rate")
        self.alphaSpinBox = QDoubleSpinBox()
        self.alphaSpinBox.setRange(0, 1)
        self.alphaSpinBox.setSingleStep(0.01)
        self.alphaSpinBox.setValue(0.2)

        epsilonLabel = QLabel("epsilon:")
        epsilonLabel.setToolTip("Exploration rate")
        self.epsilonSpinBox = QDoubleSpinBox()
        self.epsilonSpinBox.setRange(0, 1)
        self.epsilonSpinBox.setSingleStep(0.01)
        self.epsilonSpinBox.setValue(0.5)

        gammaLabel = QLabel("gamma:")
        gammaLabel.setToolTip("Discount factor")
        self.gammaSpinBox = QDoubleSpinBox()
        self.gammaSpinBox.setRange(0, 1)
        self.gammaSpinBox.setSingleStep(0.01)
        self.gammaSpinBox.setValue(0.9)

        paramsLayout = QHBoxLayout()
        paramsLayout.setSpacing(5)
        paramsLayout.setContentsMargins(20, 0, 20, 0)
        paramsLayout.addWidget(self.paramsResetButton)
        paramsLayout.addSpacing(20)
        paramsLayout.addSpacerItem(QSpacerItem(
            20, 0, QSizePolicy.MinimumExpanding, QSizePolicy.Minimum
        ))
        paramsLayout.addWidget(tdnLabel)
        paramsLayout.addWidget(self.tdnSpinBox)
        paramsLayout.addSpacing(20)
        paramsLayout.addWidget(alphaLabel)
        paramsLayout.addWidget(self.alphaSpinBox)
        paramsLayout.addSpacing(20)
        paramsLayout.addWidget(epsilonLabel)
        paramsLayout.addWidget(self.epsilonSpinBox)
        paramsLayout.addSpacing(20)
        paramsLayout.addWidget(gammaLabel)
        paramsLayout.addWidget(self.gammaSpinBox)
        paramsLayout.addSpacerItem(QSpacerItem(
            0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum
        ))

        paramsWidget = QWidget()
        paramsWidget.setLayout(paramsLayout)

        self.rewardsResetButton = QPushButton()
        self.rewardsResetButton.setIcon(QIcon(":/assets/reset_icon.png"))
        self.rewardsResetButton.setIconSize(QSize(20, 20))
        self.rewardsResetButton.setToolTip("Reset reward structure")

        self.aliveSpinBox = QDoubleSpinBox()
        self.aliveSpinBox.setRange(-100, 100)
        self.aliveSpinBox.setSingleStep(0.1)
        self.aliveSpinBox.setAccelerated(True)
        self.aliveSpinBox.setValue(0)
        aliveLayout = QHBoxLayout()
        aliveLayout.setSpacing(5)
        aliveLayout.addWidget(QLabel("alive:"))
        aliveLayout.addWidget(self.aliveSpinBox)
        aliveWidget = QWidget()
        aliveWidget.setLayout(aliveLayout)

        self.deadSpinBox = QDoubleSpinBox()
        self.deadSpinBox.setRange(-100, -0.1)
        self.deadSpinBox.setSingleStep(0.1)
        self.deadSpinBox.setAccelerated(True)
        self.deadSpinBox.setValue(-5)
        deadLayout = QHBoxLayout()
        deadLayout.setSpacing(5)
        deadLayout.addWidget(QLabel("dead:"))
        deadLayout.addWidget(self.deadSpinBox)
        deadWidget = QWidget()
        deadWidget.setLayout(deadLayout)

        self.greenSpinBox = QDoubleSpinBox()
        self.greenSpinBox.setRange(0, 100)
        self.greenSpinBox.setSingleStep(0.1)
        self.greenSpinBox.setAccelerated(True)
        self.greenSpinBox.setValue(2)
        greenLayout = QHBoxLayout()
        greenLayout.setSpacing(5)
        greenLayout.addWidget(QLabel("green:"))
        greenLayout.addWidget(self.greenSpinBox)
        greenWidget = QWidget()
        greenWidget.setLayout(greenLayout)

        self.redSpinBox = QDoubleSpinBox()
        self.redSpinBox.setRange(-100, 0)
        self.redSpinBox.setSingleStep(0.1)
        self.redSpinBox.setAccelerated(True)
        self.redSpinBox.setValue(-2)
        redLayout = QHBoxLayout()
        redLayout.setSpacing(5)
        redLayout.addWidget(QLabel("red:"))
        redLayout.addWidget(self.redSpinBox)
        redWidget = QWidget()
        redWidget.setLayout(redLayout)

        targetLenLabel = QLabel("target length:")
        targetLenLabel.setToolTip(
            """The snake's length after which the
penalty isn't applied anymore.""")
        self.targetLenSpinBox = QSpinBox()
        self.targetLenSpinBox.setRange(1, 100)
        self.targetLenSpinBox.setValue(10)
        targetLenLayout = QHBoxLayout()
        targetLenLayout.setSpacing(5)
        targetLenLayout.addWidget(targetLenLabel)
        targetLenLayout.addWidget(self.targetLenSpinBox)
        targetLenWidget = QWidget()
        targetLenWidget.setLayout(targetLenLayout)

        penaltyLabel = QLabel("      penalty:")
        penaltyLabel.setToolTip(
            """This penalty is applied to all scores except for green
while the snake is under the target length.""")
        self.penaltySpinBox = QSpinBox()
        self.penaltySpinBox.setRange(-100, 0)
        self.penaltySpinBox.setValue(-1)
        penaltyLayout = QHBoxLayout()
        penaltyLayout.setSpacing(5)
        penaltyLayout.addWidget(penaltyLabel)
        penaltyLayout.addWidget(self.penaltySpinBox)
        penaltyWidget = QWidget()
        penaltyWidget.setLayout(penaltyLayout)

        rewardsLayout = QGridLayout()
        rewardsLayout.setContentsMargins(20, 0, 20, 0)
        rewardsLayout.addWidget(
            self.rewardsResetButton, 0, 0, alignment=Qt.AlignLeft
        )
        rewardsLayout.addItem(
            QSpacerItem(
                20, 0, QSizePolicy.MinimumExpanding, QSizePolicy.Minimum
            ),
            0, 1
        )
        rewardsLayout.addWidget(aliveWidget, 0, 2, alignment=Qt.AlignRight)
        rewardsLayout.addWidget(greenWidget, 0, 3, alignment=Qt.AlignRight)
        rewardsLayout.addWidget(targetLenWidget, 0, 4, alignment=Qt.AlignRight)
        rewardsLayout.addWidget(deadWidget, 1, 2, alignment=Qt.AlignRight)
        rewardsLayout.addWidget(redWidget, 1, 3, alignment=Qt.AlignRight)
        rewardsLayout.addWidget(penaltyWidget, 1, 4, alignment=Qt.AlignRight)
        rewardsLayout.addItem(
            QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum),
            0, 5
        )

        rewardsWidget = QWidget()
        rewardsWidget.setLayout(rewardsLayout)

        fileLayout = QHBoxLayout()
        fileLayout.setSpacing(5)
        fileLayout.setContentsMargins(20, 0, 20, 0)

        self.fileLineEdit = QLineEdit(
            AgentFactory.default_filepath(self.nameLineEdit.text())
        )
        self.fileLineEdit.setSizePolicy(
            QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        )
        self.fileLineEdit.setReadOnly(True)

        self.defaultCheckBox = QCheckBox()
        self.defaultCheckBox.setChecked(True)
        self.defaultCheckBox.setText("default")

        fileLayout.addWidget(QLabel("save to:"))
        fileLayout.addWidget(self.fileLineEdit)
        fileLayout.addSpacing(20)
        fileLayout.addWidget(self.defaultCheckBox)

        fileWidget = QWidget()
        fileWidget.setLayout(fileLayout)

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok |
                                     QDialogButtonBox.Cancel)

        mainLayout = QVBoxLayout()
        mainLayout.setSpacing(20)
        mainLayout.setContentsMargins(20, 20, 20, 20)
        mainLayout.addWidget(SubtitleLine("Personality"))
        mainLayout.addWidget(personalityWidget)
        mainLayout.addSpacing(20)
        mainLayout.addWidget(SubtitleLine("Learning parameters"))
        mainLayout.addWidget(paramsWidget)
        mainLayout.addSpacing(20)
        mainLayout.addWidget(SubtitleLine("Reward structure"))
        mainLayout.addWidget(rewardsWidget)
        mainLayout.addSpacing(20)
        mainLayout.addWidget(SubtitleLine("File"))
        mainLayout.addWidget(fileWidget)
        mainLayout.addSpacing(20)
        mainLayout.addWidget(buttonBox, alignment=Qt.AlignCenter)
        self.setLayout(mainLayout)

        self.nameLineEdit.textChanged.connect(self.name_changed)
        self.RSpinbox.valueChanged.connect(self.change_color)
        self.GSpinbox.valueChanged.connect(self.change_color)
        self.BSpinbox.valueChanged.connect(self.change_color)
        self.randomButton.clicked.connect(self.random_personality)
        self.defaultCheckBox.checkStateChanged.connect(self.default_changed)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        self.finished.connect(self.deleteLater)

    def name_changed(self, name):
        if self.defaultCheckBox.isChecked():
            self.fileLineEdit.setText(
                AgentFactory.default_filepath(name)
            )

    def change_color(self):
        self.colorDisplay.set_color(QColor(
            self.RSpinbox.value(),
            self.GSpinbox.value(),
            self.BSpinbox.value()
        ))

    def random_personality(self):
        color = AgentFactory.random_color()
        self.RSpinbox.setValue(color[0])
        self.GSpinbox.setValue(color[1])
        self.BSpinbox.setValue(color[2])
        self.change_color()
        self.nameLineEdit.setText(AgentFactory.random_name())

    def default_changed(self, checkState):
        if checkState == Qt.Checked:
            self.fileLineEdit.setText(
                AgentFactory.default_filepath(self.nameLineEdit.text())
            )
            self.fileLineEdit.setReadOnly(True)
        else:
            self.fileLineEdit.setReadOnly(False)

    def select_folder(self):
        dialog = QFileDialog(self)
        dialog.setDefaultSuffix("l2s")
        dialog.setNameFilter("*.l2s")
        dialog.open()

    def accept(self):
        name = self.nameLineEdit.text()
        if self.nameLineEdit.validator().validate(name, 0) !=\
                QValidator.State.Acceptable:
            MessagePopup(
                "Name can't be empty or contain \
non alphanumeric characters.",
                color="red",
                parent=self
            ).open()
            return
        if name == "":
            name = self.factory.random_name()
        color = (
            self.RSpinbox.value(),
            self.GSpinbox.value(),
            self.BSpinbox.value()
        )
        td_n = self.tdnSpinBox.value()
        epsilon = self.epsilonSpinBox.value()
        alpha = self.alphaSpinBox.value()
        gamma = self.gammaSpinBox.value()
        rewards = RewardStructure()
        rewards.set_rewards(
            self.aliveSpinBox.value(),
            self.deadSpinBox.value(),
            self.greenSpinBox.value(),
            self.redSpinBox.value()
        )
        rewards.set_target_len(self.targetLenSpinBox.value())
        rewards.set_penalty(self.penaltySpinBox.value())
        filepath = self.fileLineEdit.text()

        agent = None
        try:
            agent = self.factory.new(td_n, epsilon, alpha, gamma, rewards,
                                     name, color, filepath)
        except Exception as e:
            MessagePopup(
                f"Couldn't create the agent:\n{e}",
                color="red", parent=self
            ).open()

        if agent is not None:
            self.agentCreated.emit(filepath)
            super().accept()
