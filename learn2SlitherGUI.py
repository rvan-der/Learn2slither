import sys
import statistics

from l2sMainWindow import Ui_l2sMainWindow
from boardWidget import BoardWidget
from stdoutTextEdit import StdoutTextEdit
from agentsToolBox import AgentsToolBox
from playerWidget import PlayerWidget
from environment import Environment
from agent import AgentFactory
from rewards import RewardStructure
from interpreter import (Trainer, Player)
from PySide6.QtWidgets import (QApplication, QMainWindow, QDialog,
                               QGridLayout, QLabel, QDialogButtonBox)
from PySide6.QtCore import (Qt, Signal, Slot)


class MessagePopup(QDialog):
    def __init__(self, text, parent=None):
        super().__init__(parent=parent, f=Qt.Popup)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet("QDialog{background-color: rgb(40, 48, 56)}")

        layout = QGridLayout()

        label = QLabel(text)
        layout.addWidget(label, 0, 0, alignment=Qt.AlignCenter)

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        self.finished.connect(self.deleteLater)
        layout.addWidget(buttonBox, 1, 0, alignment=Qt.AlignCenter)
        self.setLayout(layout)


class Learn2SlitherGUI(QMainWindow, Ui_l2sMainWindow):

    fpsChanged = Signal(float)

    def __init__(self, environment, app, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.environment = environment
        self.interpreter = None

        app.aboutToQuit.connect(self.abort)

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
        self.agentsToolBox.playAgentSignal.connect(self.play_agent)
        self.agentsToolBox.currentChanged.connect(self.set_agent_colors)

        self.factory = AgentFactory()
        for _ in range(20):
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

    def play_agent(self, agent, sessions):
        self.agentsToolBox.setEnabled(False)
        self.playerWidget.setEnabled(True)
        self.interpreter = Player(self.environment, agent, sessions)
        self.interpreter.set_paused(True)
        self.interpreter.playSessionFinished.connect(
            self.play_session_finished
        )
        self.playerWidget.pausedChanged.connect(self.interpreter.set_paused)
        self.playerWidget.nextFrameButton.clicked.connect(
            self.interpreter.single_step
        )
        self.playerWidget.cancelButton.clicked.connect(
            self.interpreter.cancel
        )
        delay = self.playerWidget.fpsComboBox.currentData()
        self.interpreter.set_delay(delay)
        self.fpsChanged.connect(self.interpreter.set_delay)
        self.interpreter.start()

    @Slot(list, list, list)
    def play_session_finished(self, rewards, lengths, times):
        self.agentsToolBox.setEnabled(True)
        self.playerWidget.set_paused(True)
        self.playerWidget.setEnabled(False)
        message = "0 play sessions finished. No results to show."
        if (len(rewards) > 0):
            message = f"""
Play sessions finished !\n
rewards:\n
   - total: {sum(rewards)}\n
   - mean:{sum(rewards) / len(rewards)}\n
   - median: {statistics.median(rewards)}\n
lengths:\n
   - total: {sum(lengths)}\n
   - mean:{sum(lengths) / len(lengths)}\n
   - median: {statistics.median(lengths)}\n
times alive:\n
   - total: {sum(times)}\n
   - mean:{sum(times) / len(times)}\n
   - median: {statistics.median(times)}
"""
        dialog = MessagePopup(message, parent=self)
        dialog.finished.connect(self.environment.init_empty_board)
        dialog.open()
        self.quit_interpreter_thread()

    def train_agent(self, agent, sessions):
        self.agentsToolBox.setEnabled(False)
        self.playerWidget.setEnabled(True)
        self.interpreter = Trainer(self.environment, agent, sessions)
        self.interpreter.set_paused(True)
        self.interpreter.trainingFinished.connect(self.training_finished)
        self.interpreter.trainingCanceled.connect(self.training_canceled)
        self.playerWidget.pausedChanged.connect(self.interpreter.set_paused)
        self.playerWidget.nextFrameButton.clicked.connect(
            self.interpreter.single_step
        )
        self.playerWidget.cancelButton.clicked.connect(
            self.interpreter.cancel
        )
        delay = self.playerWidget.fpsComboBox.currentData()
        self.interpreter.set_delay(delay)
        self.fpsChanged.connect(self.interpreter.set_delay)
        self.interpreter.start()

    def fps_changed(self, index):
        delay = self.playerWidget.fpsComboBox.itemData(index)
        self.fpsChanged.emit(delay)

    @Slot()
    def training_finished(self):
        self.agentsToolBox.setEnabled(True)
        self.playerWidget.set_paused(True)
        self.playerWidget.setEnabled(False)
        dialog = MessagePopup("Training finished !", parent=self)
        dialog.finished.connect(self.environment.init_empty_board)
        dialog.open()
        self.quit_interpreter_thread()

    @Slot(int)
    def training_canceled(self, progress):
        self.agentsToolBox.setEnabled(True)
        self.playerWidget.set_paused(True)
        self.playerWidget.setEnabled(False)
        dialog = MessagePopup(f"""
Training was interrupted. The last incomplete episode hasn't been\n
taken into account. The progress of {progress} completed episodes was saved.
""", parent=self)
        dialog.finished.connect(self.environment.init_empty_board)
        dialog.open()
        self.quit_interpreter_thread()

    def abort(self):
        print("ABORT!!")
        if self.interpreter is None:
            return
        if isinstance(self.interpreter, Trainer):
            self.interpreter.trainingCanceled.disconnect(
                self.training_canceled
            )
            self.interpreter.trainingFinished.disconnect(
                self.training_finished
            )
        else:
            self.interpreter.playSessionFinished.disconnect(
                self.play_session_finished
            )

        self.interpreter.cancel()
        self.quit_interpreter_thread()

    def quit_interpreter_thread(self):
        self.interpreter.quit()
        self.interpreter.wait()
        self.interpreter.deleteLater()
        self.interpreter = None


if __name__ == "__main__":
    environment = Environment(10, 10)
    app = QApplication(sys.argv)
    window = Learn2SlitherGUI(environment, app)
    window.show()
    app.exec()
