import sys
import os
from statistics import median
from interpreter import Interpreter
from l2sMainWindow import Ui_l2sMainWindow
from boardWidget import BoardWidget
from stdoutTextEdit import StdoutTextEdit
from agentsToolBox import AgentsToolBox
from playerWidget import PlayerWidget
from uiElements import MessagePopup
from agentCreationDialog import AgentCreationDialog
from PySide6.QtWidgets import (QApplication, QMainWindow, QMenu)
from PySide6.QtCore import (Signal, Slot, QEvent, QThreadPool)
from PySide6.QtGui import QAction


class MyMenu(QMenu):

    def __init__(self, parent=None):
        super().__init__(parent)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.MouseButtonRelease \
                and isinstance(obj, QMenu) \
                and obj.activeAction().isCheckable():
            obj.activeAction().trigger()
            return True
        return super().eventFilter(obj, event)


class Learn2SlitherGUI(QMainWindow, Ui_l2sMainWindow):

    printOnChanged = Signal(bool)
    displayOnChanged = Signal(bool)
    abortSignal = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.aborted = False
        self.displayOn = True
        self.printOn = True
        self.threadpool = QThreadPool()
        # self.interpreter = None

        self.displayOnAction = QAction("Board display")
        self.displayOnAction.setCheckable(True)
        self.displayOnAction.setChecked(True)

        self.printOnAction = QAction("Print to stdout")
        self.printOnAction.setCheckable(True)
        self.printOnAction.setChecked(True)

        settingsMenu = QMenu("Settings")
        settingsMenu.addAction(self.displayOnAction)
        settingsMenu.addAction(self.printOnAction)
        self.menubar.addMenu(settingsMenu)

        self.boardWidget = BoardWidget()
        self.boardFrameLayout.insertWidget(0, self.boardWidget)

        self.playerWidget = PlayerWidget()
        self.playerWidget.setEnabled(False)
        self.boardFrameLayout.insertWidget(1, self.playerWidget)

        self.stdoutTextEdit = StdoutTextEdit()
        self.stdOutFrameLayout.insertWidget(0, self.stdoutTextEdit)

        self.agentsToolBox = AgentsToolBox()
        self.agentsScrollArea.setWidget(self.agentsToolBox)

        self.agentsToolBox.trainAgentSignal.connect(self.train_agent)
        self.agentsToolBox.playAgentSignal.connect(self.play_agent)
        self.createAgentButton.clicked.connect(self.create_agent)
        self.displayOnAction.toggled.connect(self.change_display_on)
        self.printOnAction.toggled.connect(self.change_print_on)
        QApplication.instance().aboutToQuit.connect(self.abort)

        self.populate()
        print("\nWelcome !")

    @Slot(bool)
    def change_display_on(self, displayOn):
        self.displayOn = displayOn
        if displayOn is False:
            self.boardWidget.clear_display()
        self.boardFrame.setEnabled(displayOn)
        if displayOn is True and self.interpreter is not None \
                and self.interpreter.isRunning():
            self.playerWidget.setEnabled(True)
        self.displayOnChanged.emit(displayOn)

    @Slot(bool)
    def change_print_on(self, printOn):
        self.printOn = printOn
        self.printOnChanged.emit(printOn)

    def import_folder(self, folder):
        folder_path = os.path.expanduser(folder)
        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            for item in os.listdir(folder_path):
                filepath = f"{folder_path}/{item}"
                if os.path.isfile(filepath) and filepath.endswith(".l2s"):
                    self.agentsToolBox.addAgent(filepath)

    def populate(self):
        self.import_folder(
            "/sgoinfre/goinfre/Perso/rvan-der/Learn2Slither/agents"
        )
        self.import_folder("~/.local/Learn2Slither/agents")

    @Slot()
    def create_agent(self):
        dialog = AgentCreationDialog(self)
        dialog.agentCreated.connect(self.agentsToolBox.addAgent)
        dialog.open()

    @Slot(str, int)
    def train_agent(self, filepath, sessions):
        self.launch_session(filepath, sessions, train=True)

    @Slot(str, int)
    def play_agent(self, filepath, sessions):
        self.launch_session(filepath, sessions, train=False)

    @Slot(int, float, int, int)
    def training_finished(self, progress, maxRwds, maxLen, maxTime):
        title = "Training finished !\n\n"
        msg = "0 sessions completed. No results to show."
        if progress > 0:
            msg = f"""Games: {progress}
   Max rewards: {maxRwds}
    Max length: {maxLen}
      Max time: {maxTime}"""
        self.close_session(title + msg)

    @Slot(int, list, list, list)
    def play_session_finished(self, progress, rewards, lengths, times):
        title = "Play session finished !\n\n"
        msg = "0 games finished. No results to show."
        if progress > 0:
            msg = self.play_stats_message(progress, rewards, lengths, times)
        self.close_session(title + msg)

    def launch_session(self, filepath, sessions, train):
        self.agentsToolBox.setEnabled(False)
        self.playerWidget.set_paused(True)
        self.playerWidget.setEnabled(True)

        worker = Interpreter(filepath, sessions, train=train)
        worker.set_delay(self.playerWidget.fpsComboBox.currentData())
        worker.set_paused(True)
        worker.set_print_on(self.printOn)
        worker.set_display_on(self.displayOn)

        worker.setAutoDelete(True)
        self.threadpool.start(worker)

        worker.env.cellUpdate.connect(self.boardWidget.update_cell)
        worker.sigs.playSessionFinished.connect(self.play_session_finished)
        worker.sigs.trainingFinished.connect(self.training_finished)
        worker.sigs.progressMade.connect(
            self.agentsToolBox.currentWidget().increment_sessions
        )

        self.displayOnChanged.connect(worker.set_display_on)
        self.printOnChanged.connect(worker.set_print_on)
        self.playerWidget.pausedChanged.connect(worker.set_paused)
        self.playerWidget.nextFrameButton.clicked.connect(worker.single_step)
        self.playerWidget.cancelButton.clicked.connect(worker.cancel)
        self.playerWidget.delayChanged.connect(worker.set_delay)
        self.abortSignal.connect(worker.abort)

    def close_session(self, msg):
        self.agentsToolBox.setEnabled(True)
        self.playerWidget.setEnabled(False)

        msgPopup = MessagePopup(msg, parent=self)
        msgPopup.finished.connect(self.boardWidget.clear_display)
        msgPopup.finished.connect(msgPopup.deleteLater)
        msgPopup.open()

    def play_stats_message(self, progress, rewards, lengths, times):
        st = self.play_stats(progress, rewards, lengths, times)
        sepLine = "--------|" + "----------|" * 5 + "\n"
        msg = f"games: {st['games']}\n" + " " * 8
        msg += "|  total   |   min    |   max    |   mean   |  median  |\n"
        msg += sepLine + f"rewards |{st['total']['reward']:>9} |" + \
        f"{st['minimum']['reward']:>9} |{st['maximum']['reward']:>9} |" + \
        f"{st['mean']['reward']:>9} |{st['median']['reward']:>9} |\n" + \
        sepLine + f"lengths |{st['total']['length']:>9} |" + \
        f"{st['minimum']['length']:>9} |{st['maximum']['length']:>9} |" + \
        f"{st['mean']['length']:>9} |{st['median']['length']:>9} |\n" + \
        sepLine + f"times   |{st['total']['time']:>9} |" + \
        f"{st['minimum']['time']:>9} |{st['maximum']['time']:>9} |" + \
        f"{st['mean']['time']:>9} |{st['median']['time']:>9} |"
        return msg

    def play_stats(self, progress, rewards, lengths, times):
        stats = {}
        stats['games'] = progress
        stats['total'] = {}
        stats['minimum'] = {}
        stats['maximum'] = {}
        stats['mean'] = {}
        stats['median'] = {}
        stats['total']['reward'] = sum(rewards)
        stats['total']['length'] = sum(lengths)
        stats['total']['time'] = sum(times)
        stats['minimum']['reward'] = min(rewards)
        stats['minimum']['length'] = min(lengths)
        stats['minimum']['time'] = min(times)
        stats['maximum']['reward'] = max(rewards)
        stats['maximum']['length'] = max(lengths)
        stats['maximum']['time'] = max(times)
        stats['median']['reward'] = median(rewards)
        stats['median']['length'] = median(lengths)
        stats['median']['time'] = median(times)
        stats['mean']['reward'] = stats['total']['reward'] / progress
        stats['mean']['length'] = stats['total']['length'] / progress
        stats['mean']['time'] = stats['total']['time'] / progress
        return stats

    @Slot()
    def abort(self):
        self.abortSignal.emit()
        self.threadpool.waitForDone()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    learn2Slither = Learn2SlitherGUI()
    learn2Slither.show()
    app.exec()
