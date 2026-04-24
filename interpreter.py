import time
from enums import Status as St
from PySide6.QtCore import (QThread, Signal)


class Interpreter(QThread):
    def __init__(self, environment, agent, sessions, parent=None):
        super().__init__(parent)
        self.env = environment
        self.agent = agent
        self.sessions = sessions
        self.paused = True
        self.print = True
        self.singleStep = False
        self.canceled = False
        self.delay = 0

    def set_delay(self, delay):
        self.delay = delay

    def set_paused(self, paused):
        self.paused = paused

    def set_print(self, _print):
        self.print = _print

    def single_step(self):
        self.singleStep = True

    def cancel(self):
        self.canceled = True


class Trainer(Interpreter):

    trainingFinished = Signal()
    trainingCanceled = Signal(int)

    def __init__(self, environment, agent, sessions):
        super().__init__(environment, agent, sessions)

    # Q-learning algorithm
    def run(self):
        agent = self.agent
        progress = 0
        for e in range(self.sessions):
            if self.canceled:
                break

            self.env.new_game()

            if self.delay > 0:
                time.sleep(self.delay)

            if self.print:
                if e > 0:
                    print("\n########################################\n")
                print(f"Episode {e + 1}/{self.sessions}\n")

            episode = []
            while self.env.status != St.DEAD and not self.canceled:
                while self.paused and not self.singleStep:
                    continue
                self.singleStep = False
                state = self.env.get_state()
                action = agent.choose_action(state)
                self.env.move_snake(action)
                reward = self.env.get_reward(agent.rewards)
                episode.append({'state': state,
                                'action': action,
                                'reward': reward})
                if self.print:
                    print(f"\n{state}")
                    print(f"\n{str(action)}")
                if self.delay > 0:
                    time.sleep(self.delay)

            if self.canceled:
                break

            if self.print:
                print("\nEpisode finished")
                print(f"final length: {len(self.env.snake)}")
                print(f"time alive: {len(episode)}")
                print(f"total rewards: {sum(s['reward'] for s in episode)}")
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

            self.agent.sessions += 1
            progress += 1

            if self.delay > 0 and e < self.sessions - 1:
                time.sleep(self.delay * 2)

        if self.print:
            print("\n########################################\n")
            print("Training finished.")

        agent.save_to_file(agent.name)
        if self.canceled:
            self.trainingCanceled.emit(progress)
        else:
            self.trainingFinished.emit()


class Player(Interpreter):

    playSessionFinished = Signal(list, list, list)

    def __init__(self, environment, agent, sessions, parent=None):
        super().__init__(environment, agent, sessions, parent)

    def run(self):
        rewards = []
        lengths = []
        times = []
        agent = self.agent

        for e in range(self.sessions):
            if self.canceled:
                break

            self.env.new_game()

            if self.print:
                if e > 0:
                    print("\n########################################\n")
                print(f"Game {e + 1}/{self.sessions}\n")

            if self.delay > 0:
                time.sleep(self.delay)

            total_reward = 0
            time_alive = 0
            while self.env.status != St.DEAD and not self.canceled:
                while self.paused and not self.singleStep:
                    continue
                self.singleStep = False
                state = self.env.get_state()
                action = agent.choose_action(state, training=False)
                self.env.move_snake(action)
                total_reward += self.env.get_reward(agent.rewards)
                time_alive += 1
                if self.print:
                    print(f"\n{state}")
                    print(f"\n{str(action)}")
                self.env.move_snake(action)
                if self.delay > 0:
                    time.sleep(self.delay)
            if self.canceled:
                break
            rewards.append(total_reward)
            lengths.append(len(self.env.snake))
            times.append(time_alive)

            if self.print:
                print("\nGame finished")
                print(f"final length: {len(self.env.snake)}")
                print(f"time alive: {time_alive}")
                print(f"total rewards: {total_reward}")

        if self.print:
            print("\n########################################\n")
            print("Play session finished.")
        self.playSessionFinished.emit(rewards, lengths, times)
        return {"rewards": rewards, "lengths": lengths, "times": times}
