import time
from enums import Status as St
from agent import AgentFactory
from environment import Environment
from PySide6.QtCore import (QObject, QRunnable, Signal, Slot)


class InterpreterSignals(QObject):
    progressMade = Signal()
    trainingFinished = Signal(int, float, int, int)
    playSessionFinished = Signal(int, list, list, list)


class Interpreter(QRunnable):
    def __init__(self, filepath, sessions, train, outfile=None):
        super().__init__()
        self.sigs = InterpreterSignals()
        self.env = Environment(displayOn=False)
        self.factory = AgentFactory()
        self.displayOn = False
        self.paused = False
        self.printOn = False
        self.singleStep = False
        self.canceled = False
        self.delay = 0
        self.train = train
        self.sessions = sessions
        self.filepath = filepath
        self.outfile = outfile
        self.aborted = False

    def set_filepath(self, filepath):
        self.filepath = filepath

    def set_sessions(self, sessions):
        self.sessions = sessions

    @Slot(float)
    def set_delay(self, delay):
        self.delay = delay

    @Slot(bool)
    def set_paused(self, paused):
        self.paused = paused

    @Slot(bool)
    def set_print_on(self, printOn):
        self.printOn = printOn

    @Slot(bool)
    def set_display_on(self, displayOn):
        self.displayOn = displayOn
        self.env.displayOn = displayOn

    @Slot()
    def single_step(self):
        self.singleStep = True

    @Slot()
    def cancel(self):
        self.canceled = True

    @Slot()
    def abort(self):
        self.aborted = True
        self.canceled = True

    @Slot()
    def run(self):
        if self.train:
            self.q_learning()
        else:
            self.play()

    def q_learning(self):
        agent = self.factory.agent_from_file(self.filepath)
        maxLength = 0
        maxTime = 0
        maxRewards = float('-inf')
        progress = 0

        for e in range(self.sessions):
            if self.canceled:
                break

            self.env.new_game()

            if self.displayOn:
                time.sleep(self.delay)

            if self.printOn:
                print("\n########################################\n")
                if e == 0:
                    print("Starting training sessions.\n")
                print(f"Episode {e + 1}/{self.sessions}\n")

            episode = []
            while self.env.status != St.DEAD and not self.canceled:
                while self.paused and not self.singleStep \
                        and not self.canceled:
                    continue
                if self.canceled:
                    break
                self.singleStep = False
                state = self.env.get_state()
                action = agent.choose_action(state)
                self.env.move_snake(action)
                reward = self.env.get_reward(agent.rewardStruct)
                episode.append({'state': state,
                                'action': action,
                                'reward': reward})
                if self.printOn:
                    print(f"\n{state}")
                    print(f"{str(action)}")
                if self.displayOn:
                    time.sleep(self.delay)

            if self.canceled:
                break

            totalRewards = sum(step['reward'] for step in episode)
            length = len(self.env.snake)
            timeAlive = len(episode)
            if totalRewards > maxRewards:
                maxRewards = totalRewards
            if length > maxLength:
                maxLength = length
            if timeAlive > maxTime:
                maxTime = timeAlive

            if self.printOn:
                print("\nEpisode finished")
                print(f"final length: {length}")
                print(f"time alive: {timeAlive}")
                print(f"total rewards: {totalRewards}")
                print("\nUpdating Q-values...")

            # update Q-values
            for k, step in enumerate(episode):
                s = step['state']
                a = step['action']
                r = step['reward']
                q_old = agent.qtable.get_qvalue(s, a)
                td_target = r
                i = 1
                while i < agent.td_n + 1 and k + i < len(episode):
                    td_target += (agent.gamma ** i) * episode[k + i]['reward']
                    i += 1
                if k + i < len(episode):
                    s_ki = episode[k + i]['state']
                    q_max = max(agent.qtable.get_state_values(s_ki))
                    td_target += (agent.gamma ** i) * q_max
                td_error = td_target - q_old
                q_new = q_old + agent.alpha * td_error
                agent.qtable.set_qvalue(s, a, q_new)

            agent.increment_sessions()
            progress += 1
            self.sigs.progressMade.emit()

        if self.printOn:
            print("\n########################################\n")
            print("Training finished.")

        agent.save_to_file(
            self.filepath if self.outfile is None else self.outfile
        )
        if not self.aborted:
            if maxRewards == float('-inf'):
                maxRewards = 0
            self.sigs.trainingFinished.emit(
                progress, maxRewards, maxLength, maxTime
            )

    def play(self):
        agent = self.factory.agent_from_file(self.filepath)
        rewards = []
        lengths = []
        times = []
        progress = 0

        for e in range(self.sessions):
            if self.canceled:
                break

            self.env.new_game()

            if self.printOn:
                print("\n########################################\n")
                if e == 0:
                    print("Starting play session.\n")
                print(f"Game {e + 1}/{self.sessions}\n")

            if self.displayOn:
                time.sleep(self.delay)

            total_reward = 0
            time_alive = 0
            while self.env.status != St.DEAD and not self.canceled:
                while self.paused and not self.singleStep \
                        and not self.canceled:
                    continue
                if self.canceled:
                    break
                self.singleStep = False
                state = self.env.get_state()
                action = agent.choose_action(state, training=False)
                self.env.move_snake(action)
                total_reward += self.env.get_reward(agent.rewardStruct)
                time_alive += 1
                if self.printOn:
                    print(f"\n{state}")
                    print(f"{str(action)}")
                if self.displayOn:
                    time.sleep(self.delay)
            if self.canceled:
                break
            rewards.append(total_reward)
            lengths.append(len(self.env.snake))
            times.append(time_alive)
            progress += 1

            if self.printOn:
                print("\nGame finished")
                print(f"final length: {len(self.env.snake)}")
                print(f"time alive: {time_alive}")
                print(f"total rewards: {total_reward}")

        if self.printOn:
            print("\n########################################\n")
            print("Play session finished.")

        if not self.aborted:
            self.sigs.playSessionFinished.emit(
                progress, rewards, lengths, times
            )
