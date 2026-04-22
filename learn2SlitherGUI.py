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
from PySide6.QtWidgets import (QApplication, QMainWindow, QSizePolicy)


class Learn2SlitherGUI(QMainWindow, Ui_l2sMainWindow):
    def __init__(self, environment, app, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.environment = environment

        self.boardWidget = BoardWidget(environment)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding,
                                 QSizePolicy.Policy.Expanding)
        self.boardWidget.setSizePolicy(sizePolicy)
        self.boardFrameLayout.insertWidget(0, self.boardWidget)

        self.playerWidget = PlayerWidget()
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding,
                                 QSizePolicy.Policy.Minimum)
        self.playerWidget.setSizePolicy(sizePolicy)
        self.boardFrameLayout.insertWidget(1, self.playerWidget)
        self.playerWidget.setEnabled(False)

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
        self.playerWidget.pausedChanged.connect(self.trainer.set_paused)
        self.playerWidget.nextFrameButton.clicked.connect(self.trainer.single_step)
        self.trainer.trainingFinished.connect(self.training_finished)
        self.trainer.start()

    def training_finished(self):
        self.agentsToolBox.setEnabled(True)
        self.playerWidget.set_paused(True)
        self.playerWidget.setEnabled(False)

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
