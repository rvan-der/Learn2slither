import time
from statistics import median
from enums import Status as St
from agent import AgentFactory
from environment import Environment
from PySide6.QtCore import (QObject, QRunnable, Signal, Slot)


class InterpreterSignals(QObject):
    progressMade = Signal(int)
    timerUpdate = Signal(int)
    trainingFinished = Signal(int, float, int, int)
    playSessionFinished = Signal(int, list, list, list)


class Interpreter(QRunnable):
    def __init__(self, filepath, sessions, train=True, outfile=None):
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
        self.emitFrequency = 100
        self.sendProgressNow = False

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
        if not self.displayOn and not printOn:
            self.emitFrequency = 100
        else:
            self.emitFrequency = 1
            self.sendProgressNow = True

    @Slot(bool)
    def set_display_on(self, displayOn):
        self.displayOn = displayOn
        self.env.set_display_on(displayOn)
        if not self.printOn and not displayOn:
            self.emitFrequency = 100
        else:
            self.sendProgressNow = True
            self.emitFrequency = 1

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
                self.sigs.timerUpdate.emit(0)
                time.sleep(self.delay)

            if self.printOn:
                print("\n########################################\n")
                if e == 0:
                    print("Starting training sessions.\n")
                print(f"Episode {e + 1}/{self.sessions}\n")

            episode = []
            timer = 0
            while not self.canceled:
                while self.paused and not self.singleStep \
                        and not self.canceled:
                    continue
                if self.canceled:
                    break
                self.singleStep = False
                state = self.env.get_state()
                action = None
                reward = 0
                if state.status != St.DEAD:
                    action = agent.choose_action(state)
                    self.env.move_snake(action)
                    reward = self.env.get_reward(agent.rewardStruct)
                episode.append({'state': state,
                                'action': action,
                                'reward': reward})
                timer += 1
                if self.printOn:
                    print(f"\n{state}")
                    print(f"{str(action)}")
                if self.displayOn:
                    self.sigs.timerUpdate.emit(timer)
                    time.sleep(self.delay)
                if state.status == St.DEAD:
                    break

            if self.canceled:
                break

            totalRewards = sum(step['reward'] for step in episode)
            length = len(self.env.snake)
            timeAlive = len(episode) - 1
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
            for k, step in enumerate(episode[:-1]):
                q_old = agent.qtable.get_qvalue(step['state'], step['action'])
                g = agent.gamma
                td_target = 0
                i = 0
                while i <= agent.td_n and k + i < len(episode) - 1:
                    td_target += g**i * episode[k + i]['reward']
                    i += 1
                s_ki = episode[k + i]['state']
                td_target += g**i * max(agent.qtable.get_qvalues(s_ki))
                td_error = td_target - q_old
                q_new = q_old + agent.alpha * td_error
                agent.qtable.set_qvalue(step['state'], step['action'], q_new)

            agent.increment_sessions()
            progress += 1
            if progress % self.emitFrequency == 0 or self.sendProgressNow:
                self.sigs.progressMade.emit(agent.sessions)
            self.sendProgressNow = False

        self.sigs.progressMade.emit(agent.sessions)

        if self.printOn:
            print("\n########################################\n")
        print("\nTraining finished !\n")
        if progress > 0:
            print(f"""   Sessions: {progress}
Max rewards: {maxRewards}
 Max length: {maxLength}
   Max time: {maxTime}""")
        else:
            print("0 sessions completed. No results to show.")

        if self.displayOn:
            self.sigs.progressMade.emit(agent.sessions)
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
                self.sigs.timerUpdate.emit(0)
                time.sleep(self.delay)

            totalReward = 0
            timeAlive = 0
            while self.env.status != St.DEAD and not self.canceled \
                    and timeAlive < 5000:
                while self.paused and not self.singleStep \
                        and not self.canceled:
                    continue
                if self.canceled:
                    break
                self.singleStep = False
                state = self.env.get_state()
                action = agent.choose_action(state, training=False)
                self.env.move_snake(action)
                totalReward += self.env.get_reward(agent.rewardStruct)
                timeAlive += 1
                if self.printOn:
                    self.sigs.timerUpdate.emit(timeAlive)
                    print(f"\n{state}")
                    print(f"{str(action)}")
                if self.displayOn:
                    time.sleep(self.delay)
            if self.canceled:
                break
            rewards.append(totalReward)
            lengths.append(len(self.env.snake))
            times.append(timeAlive)
            progress += 1

            if self.printOn:
                print("\nGame finished")
                print(f"final length: {len(self.env.snake)}")
                print(f"time alive: {timeAlive}")
                print(f"total rewards: {totalReward}")

        if self.printOn:
            print("\n########################################\n")
        print("\nPlay session finished !\n")
        if progress > 0:
            print(Interpreter.play_stats_message(
                progress, rewards, lengths, times, 5000
            ))
        else:
            print("0 games finished. No results to show.")

        if not self.aborted:
            self.sigs.playSessionFinished.emit(
                progress, rewards, lengths, times
            )

    @staticmethod
    def play_stats_message(progress, rewards, lengths, times, timeout):
        st = Interpreter.play_stats(progress, rewards, lengths, times, timeout)
        sepLine = "--------|" + "-----------|" * 4
        msg = f"games: {progress}\n" + " " * 8
        msg += f"""|    min    |  median   |   mean    |    max    |
{sepLine}
rewards | {st['minimum']['reward']:<10}| {st['median']['reward']:<10}| \
{st['mean']['reward']:<10}| {st['maximum']['reward']:<10}|
{sepLine}
lengths | {st['minimum']['length']:<10}| {st['median']['length']:<10}| \
{st['mean']['length']:<10}| {st['maximum']['length']:<10}|
{sepLine}
times   | {st['minimum']['time']:<10}| {st['median']['time']:<10}| \
{st['mean']['time']:<10}| {st['maximum']['time']:<10}|

length < 10 : {st["tooSmall"]}
timeouts: {st["nbTimeouts"]}"""
        return msg

    @staticmethod
    def play_stats(progress, rewards, lengths, times, timeout):
        stats = {}
        stats['total'] = {}
        stats['minimum'] = {}
        stats['maximum'] = {}
        stats['mean'] = {}
        stats['median'] = {}
        stats['total']['reward'] = round(sum(rewards), 2)
        stats['total']['length'] = sum(lengths)
        stats['total']['time'] = sum(times)
        stats['minimum']['reward'] = round(min(rewards), 2)
        stats['minimum']['length'] = min(lengths)
        stats['minimum']['time'] = min(times)
        stats['maximum']['reward'] = round(max(rewards), 2)
        stats['maximum']['length'] = max(lengths)
        stats['maximum']['time'] = max(times)
        stats['median']['reward'] = round(median(rewards), 2)
        stats['median']['length'] = round(median(lengths), 2)
        stats['median']['time'] = round(median(times), 2)
        stats['mean']['reward'] = round(stats['total']['reward'] / progress, 2)
        stats['mean']['length'] = round(stats['total']['length'] / progress, 2)
        stats['mean']['time'] = round(stats['total']['time'] / progress, 2)
        stats['tooSmall'] = len([sLen for sLen in lengths if sLen < 10])
        stats['nbTimeouts'] = len([t for t in times if t == timeout])
        return stats
