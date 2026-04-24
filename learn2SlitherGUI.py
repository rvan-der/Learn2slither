import sys

from l2sMainWindow import Ui_l2sMainWindow
from boardWidget import BoardWidget
from stdoutTextEdit import StdoutTextEdit
from agentsToolBox import AgentsToolBox
from playerWidget import PlayerWidget
from environment import Environment
from agent import AgentFactory
from rewards import RewardStructure
from interpreter import Trainer
from PySide6.QtWidgets import (QApplication, QMainWindow, QDialog,
                               QGridLayout, QLabel, QDialogButtonBox)
from PySide6.QtCore import (Qt, Signal)


class MessagePopup(QDialog):
    def __init__(self, text, parent=None):
        super().__init__(parent=parent, f=Qt.Popup)
        layout = QGridLayout()

        label = QLabel(text)
        layout.addWidget(label, 0, 0, alignment=Qt.AlignCenter)

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok)
        buttonBox.accepted.connect(self.accept)
        layout.addWidget(buttonBox, 1, 0, alignment=Qt.AlignCenter)
        self.setLayout(layout)


class Learn2SlitherGUI(QMainWindow, Ui_l2sMainWindow):

    fpsChanged = Signal(float)

    def __init__(self, environment, app, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.environment = environment
        self.trainer = None

        self.boardWidget = BoardWidget(environment)
        self.boardFrameLayout.insertWidget(0, self.boardWidget)

        self.playerWidget = PlayerWidget()
        self.playerWidget.fpsComboBox.currentIndexChanged.connect(
            self.fps_changed
        )
        self.playerWidget.setEnabled(False)
        self.boardFrameLayout.insertWidget(1, self.playerWidget)

        self.stdoutTextEdit = StdoutTextEdit()
        self.stdOutFrameLayout.insertWidget(0, self.stdoutTextEdit)

        self.agentsToolBox = AgentsToolBox()
        self.agentsToolBox.trainAgentSignal.connect(self.train_agent)
        self.agentsToolBox.currentChanged.connect(self.set_agent_colors)

        self.factory = AgentFactory()
        for _ in range(5):
            self.agentsToolBox.addAgent(self.factory.new(2, RewardStructure()))
        self.agentsScrollArea.setWidget(self.agentsToolBox)

        self.environment.cellUpdate.connect(self.boardWidget.update_cell)
        self.environment.init_empty_board()

    def set_agent_colors(self, index):
        agent = self.agentsToolBox.widget(index).agent
        body_color = agent.color
        head_color = [c * 0.7 for c in body_color]
        self.boardWidget.set_snake_colors(head_color, body_color)
        self.environment.init_empty_board()

    def train_agent(self, agent, sessions):
        self.agentsToolBox.setEnabled(False)
        self.playerWidget.setEnabled(True)
        self.trainer = Trainer(self.environment, agent, sessions)
        self.trainer.trainingFinished.connect(self.training_finished)
        self.trainer.trainingCanceled.connect(self.training_canceled)
        self.playerWidget.pausedChanged.connect(self.trainer.set_paused)
        self.playerWidget.nextFrameButton.clicked.connect(
            self.trainer.single_step
        )
        delay = self.playerWidget.fpsComboBox.currentData()
        self.trainer.set_delay(delay)
        self.fpsChanged.connect(self.trainer.set_delay)
        self.trainer.start()

    def fps_changed(self, index):
        delay = self.playerWidget.fpsComboBox.itemData(index)
        self.fpsChanged.emit(delay)

    def training_finished(self):
        self.agentsToolBox.setEnabled(True)
        self.playerWidget.set_paused(True)
        self.playerWidget.setEnabled(False)
        dialog = MessagePopup("Training finished !", parent=self)
        dialog.open()

    def training_canceled(self, progress):
        self.agentsToolBox.setEnabled(True)
        self.playerWidget.set_paused(True)
        self.playerWidget.setEnabled(False)
        dialog = MessagePopup(
            f""" Training was interrupted. The last uncomplete episode\n
            hasn't been taken into account but the progress from {progress}\n
            completed episodes has been saved.""",
            parent=self
        )
        dialog.open()

    def quit_thread(self):
        self.trainer.cancel()
        self.trainerThread.quit()
        self.trainerThread.wait()


if __name__ == "__main__":
    environment = Environment(10, 10)
    app = QApplication(sys.argv)
    window = Learn2SlitherGUI(environment, app)
    window.show()
    app.exec()
