import time
from enums import Status as St
from PySide6.QtCore import (QObject, Signal)


class Trainer(QObject):

    trainingFinished = Signal()
    playSessionFinished = Signal(list, list, list)

    def __init__(self, environment, parent=None):
        super().__init__(parent)
        self.env = environment
        self.paused = True
        self.print = True
        self.singleStep = False
        self.canceled = False
        self.delay = 0.1

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

    def qLearning(self, agent, episodes):
        for e in range(episodes):
            if self.canceled:
                break

            self.env.new_game()

            if self.delay > 0:
                time.sleep(self.delay)

            if self.print:
                if e > 0:
                    print("\n########################################\n")
                print(f"Episode {e + 1}/{episodes}\n")

            # hold while paused
            while self.paused and not self.singleStep and not self.canceled:
                continue
            self.singleStep = False
            if self.canceled:
                break

            episode = []
            while self.env.status != St.DEAD and not self.canceled:
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

            if self.delay > 0 and e < episodes - 1:
                time.sleep(self.delay * 2)

        if not self.canceled:
            agent.save_to_file(agent.name)
            self.trainingFinished.emit()

    def playAgent(self, agent, episodes):
        rewards = []
        lengths = []
        times = []

        for e in range(episodes):
            if self.canceled:
                break

            self.env.new_game()

            if self.print:
                if e > 0:
                    print("\n########################################\n")
                print(f"Game {e + 1}/{episodes}\n")

            while self.paused and not self.singleStep and not self.canceled:
                continue
            self.singleStep = False
            if self.canceled:
                break

            total_reward = 0
            time_alive = 0
            if self.delay > 0:
                time.sleep(self.delay)

            while self.env.status != St.DEAD and not self.canceled:
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

        if not self.canceled:
            self.playSessionFinished.emit(rewards, lengths, times)
