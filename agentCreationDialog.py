from PySide6.QtWidgets import (QDialog, QVBoxLayout, QDialogButtonBox,
                               QLabel, QLineEdit, QSpinBox, QWidget,
                               QHBoxLayout, QDoubleSpinBox, QSizePolicy,
                               QFrame, QSpacerItem, QPushButton)
from PySide6.QtGui import (QPixmap, QColor, QFont, QIcon)
from PySide6.QtCore import (Signal, Qt, QSize)
from agent import (Agent, AgentFactory)
import resources_rc


class ColorDisplay(QLabel):
    def __init__(self, width, height, parent=None):
        super().__init__(parent=parent)
        self.color = (0, 0, 0)
        self.w = width
        self.h = height
        self.setFixedWidth(width)
        self.setFixedHeight(height)
        pixmap = QPixmap(width, height)
        pixmap.fill(QColor(*self.color))
        self.setPixmap(pixmap)

    def set_size(self, width, height):
        self.w = width
        self.h = height
        self.setFixedWidth(width)
        self.setFixedHeight(height)
        self.set_color(self.color)

    def set_color(self, color):
        self.color = color
        pixmap = QPixmap(self.w, self.h)
        pixmap.fill(QColor(*color))
        self.setPixmap(pixmap)


class SubtitleLine(QWidget):
    def __init__(self, text, parent=None):
        super().__init__(parent=parent)
        mainLayout = QHBoxLayout()
        mainLayout.setSpacing(3)
        mainLayout.setContentsMargins(0, 0, 0, 0)
        font = QFont()
        font.setPointSize(9)
        label = QLabel(text)
        label.setFont(font)
        label.setStyleSheet("color: rgb(125, 125, 125)")
        line = QFrame(frameShape=QFrame.HLine, lineWidth=1)
        line.setStyleSheet("color: rgb(125, 125, 125)")
        line.setSizePolicy(QSizePolicy(QSizePolicy.Expanding,
                                       QSizePolicy.Ignored))
        mainLayout.addWidget(label)
        mainLayout.addWidget(line)
        self.setLayout(mainLayout)


class AgentCreationDialog(QDialog):

    agentCreated = Signal(Agent)
    factory = AgentFactory()

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setWindowTitle("Agent creation")
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet("""
        QWidget {background-color: rgb(40, 48, 56)}
        QDialog {border: 2px ridge grey}""")

        mainLayout = QVBoxLayout()
        mainLayout.setSpacing(15)
        mainLayout.setContentsMargins(15, 15, 15, 15)

        personalityLayout = QHBoxLayout()
        personalityLayout.setSpacing(3)
        personalityLayout.setContentsMargins(15, 0, 15, 0)

        self.randomButton = QPushButton()
        self.randomButton.setIcon(QIcon(":/assets/dice_icon.png"))
        self.randomButton.setIconSize(QSize(22, 22))
        self.randomButton.setToolTip("Random personality")

        self.nameLineEdit = QLineEdit()
        self.nameLineEdit.setMaxLength(15)

        self.RSpinbox = QSpinBox()
        self.RSpinbox.setRange(0, 255)
        self.GSpinbox = QSpinBox()
        self.GSpinbox.setRange(0, 255)
        self.BSpinbox = QSpinBox()
        self.BSpinbox.setRange(0, 255)
        self.colorDisplay = ColorDisplay(20, 20)

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
        personalityLayout.addWidget(self.colorDisplay,
                                    alignment=Qt.AlignVCenter)

        personalityWidget = QWidget()
        personalityWidget.setLayout(personalityLayout)

        paramsLayout = QHBoxLayout()
        paramsLayout.setSpacing(3)
        paramsLayout.setContentsMargins(15, 0, 15, 0)

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

        paramsWidget = QWidget()
        paramsWidget.setLayout(paramsLayout)

        rewardsLayout = QHBoxLayout()
        rewardsLayout.setSpacing(3)
        rewardsLayout.setContentsMargins(15, 0, 15, 0)

        self.aliveSpinBox = QDoubleSpinBox()
        self.aliveSpinBox.setRange(-100, 100)
        self.aliveSpinBox.setSingleStep(0.1)
        self.aliveSpinBox.setAccelerated(True)
        self.aliveSpinBox.setValue(0)
        self.deadSpinBox = QDoubleSpinBox()
        self.deadSpinBox.setRange(-100, -0.1)
        self.deadSpinBox.setSingleStep(0.1)
        self.deadSpinBox.setAccelerated(True)
        self.deadSpinBox.setValue(-5)
        self.greenSpinBox = QDoubleSpinBox()
        self.greenSpinBox.setRange(0, 100)
        self.greenSpinBox.setSingleStep(0.1)
        self.greenSpinBox.setAccelerated(True)
        self.greenSpinBox.setValue(1)
        self.redSpinBox = QDoubleSpinBox()
        self.redSpinBox.setRange(-100, 0)
        self.redSpinBox.setSingleStep(0.1)
        self.redSpinBox.setAccelerated(True)
        self.redSpinBox.setValue(-1)

        rewardsLayout.addWidget(QLabel("alive:"))
        rewardsLayout.addWidget(self.aliveSpinBox)
        rewardsLayout.addSpacing(20)
        rewardsLayout.addWidget(QLabel("dead:"))
        rewardsLayout.addWidget(self.deadSpinBox)
        rewardsLayout.addSpacing(20)
        rewardsLayout.addWidget(QLabel("green:"))
        rewardsLayout.addWidget(self.greenSpinBox)
        rewardsLayout.addSpacing(20)
        rewardsLayout.addWidget(QLabel("red:"))
        rewardsLayout.addWidget(self.redSpinBox)

        rewardsWidget = QWidget()
        rewardsWidget.setLayout(rewardsLayout)

        targetLayout = QHBoxLayout()
        targetLayout.setSpacing(3)
        targetLayout.setContentsMargins(15, 0, 15, 0)

        targetLenLabel = QLabel("target length:")
        targetLenLabel.setToolTip("""Sets the snake's length after which the
penalty isn't applied anymore.""")
        self.targetLenSpinbox = QSpinBox()
        self.targetLenSpinbox.setRange(1, 100)
        self.targetLenSpinbox.setValue(10)
        penaltyLabel = QLabel("penalty:")
        penaltyLabel.setToolTip(
            """This penalty is applied to all scores except for green
while the snake is under the target length.""")
        self.penaltySpinbox = QSpinBox()
        self.penaltySpinbox.setRange(-100, 0)
        self.penaltySpinbox.setValue(-1)

        targetLayout.addWidget(targetLenLabel)
        targetLayout.addWidget(self.targetLenSpinbox)
        targetLayout.addSpacing(20)
        targetLayout.addWidget(penaltyLabel)
        targetLayout.addWidget(self.penaltySpinbox)
        targetLayout.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Expanding,
                                               QSizePolicy.Ignored))

        targetWidget = QWidget()
        targetWidget.setLayout(targetLayout)

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok |
                                     QDialogButtonBox.Cancel)

        mainLayout.addWidget(SubtitleLine("Personality"))
        mainLayout.addWidget(personalityWidget)
        mainLayout.addSpacing(15)
        mainLayout.addWidget(SubtitleLine("Learning parameters"))
        mainLayout.addWidget(paramsWidget)
        mainLayout.addSpacing(15)
        mainLayout.addWidget(SubtitleLine("Reward structure"))
        mainLayout.addWidget(rewardsWidget)
        mainLayout.addWidget(targetWidget)
        mainLayout.addSpacing(15)
        mainLayout.addWidget(buttonBox, alignment=Qt.AlignCenter)
        self.setLayout(mainLayout)

        self.RSpinbox.valueChanged.connect(self.change_color)
        self.GSpinbox.valueChanged.connect(self.change_color)
        self.BSpinbox.valueChanged.connect(self.change_color)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        self.finished.connect(self.deleteLater)

    def change_color(self):
        self.colorDisplay.set_color((
            self.RSpinbox.value(),
            self.GSpinbox.value(),
            self.BSpinbox.value()
        ))

    # def accept(self):
    #     agent = self.factory.new()
    #     super().accept()