import sys
from interpreter import Interpreter
from agent import AgentFactory
from rewards import RewardStructure
from learn2SlitherGUI import Learn2SlitherGUI
from PySide6.QtWidgets import QApplication

factory = AgentFactory()

usage = """help:
learn2Slither [command] <args> <options>
commands:
    gui
    info [agent_file]
    train [agent_file] [sessions] <options>
        -o [output_file]
        -v
    play [agent_file] [sessions] <options>
        -v
    new <options>
        -o [output_file]
        -n [name]
        -c [R] [G] [B]
        -td [td_degree]
        -a [alpha]
        -g [gamma]
        -k [kappa]
        -e [epsilon]
        -r [alive] [dead] [green] [red]
"""
commands = ["gui", "train", "play", "new"]


def gui():
    if len(sys.argv) > 2:
        print(f'Too many arguments.\n{usage}')
        return
    app = QApplication()
    learn2Slither = Learn2SlitherGUI()
    learn2Slither.show()
    app.exec()


def info():
    if len(sys.argv) < 3:
        print(f'Missing arguments.\n{usage}')
        return
    if len(sys.argv) > 3:
        print(f'Too many arguments.\n{usage}')
        return
    info = None
    try:
        info = factory.info_from_file(sys.argv[2])
    except Exception as e:
        print(e)
        return
    for key in info.keys():
        print(f'{key}: {info[key]}')


def train():
    if len(sys.argv) < 4:
        print(f'Missing arguments.\n{usage}')
        return
    filepath = sys.argv[2]
    try:
        factory.data_from_file(filepath)
    except Exception as e:
        print(e, usage, sep="\n")
        return
    sessions = sys.argv[3]
    try:
        sessions = int(sessions)
    except Exception:
        print("Expected int for number of sessions.")
        return
    if sessions < 1:
        print("Number of sessions must be at least 1.")
        return
    outfile = filepath
    verbose = False
    options = ["-o", "-v"]
    i = 4
    while i < len(sys.argv):
        if sys.argv[i] not in options:
            print(f"Invalid option '{sys.argv[i]}'.\n{usage}")
            return
        match sys.argv[i]:
            case "-o":
                i += 1
                if i >= len(sys.argv) or sys.argv[i].startswith("-"):
                    print(f'Missing argument for option -o.\n{usage}')
                    return
                outfile = sys.argv[i]
                options.remove("-o")
            case "-v":
                verbose = True
                options.remove("-v")
        i += 1
    try:
        agent = factory.agent_from_file(filepath)
        agent.save_to_file(outfile)
    except Exception as e:
        print(f'Invalid output file.\n{e}')
        return
    interpreter = Interpreter(filepath, sessions, outfile=outfile)
    interpreter.set_print_on(verbose)
    interpreter.q_learning()


def play():
    if len(sys.argv) < 4:
        print(f'Missing arguments.\n{usage}')
        return
    filepath = sys.argv[2]
    try:
        factory.data_from_file(filepath)
    except Exception as e:
        print(e)
        print(usage)
        return
    sessions = sys.argv[3]
    try:
        sessions = int(sessions)
    except Exception:
        print("Expected int for number of sessions.")
        return
    if sessions < 1:
        print("Number of sessions must be at least 1.")
        return
    verbose = False
    if len(sys.argv) > 5:
        print("Too many arguments.")
    if len(sys.argv) == 5:
        if sys.argv[4] != "-v":
            print(f"Invalid option '{sys.argv[4]}'")
            return
        verbose = True
    interpreter = Interpreter(filepath, sessions)
    interpreter.set_print_on(verbose)
    interpreter.play()


def new():
    argv = sys.argv
    argc = len(sys.argv)
    options = ["-o", "-n", "-c", "-td", "-a", "-g", "-k", "-e", "-r"]
    name = factory.random_name()
    outfile = factory.default_filepath(name, folder=".")
    r, g, b = factory.random_color()
    td_n = 2
    alpha = 0.1
    gamma = 0.9
    kappa = 0.02
    epsilon = 0.001
    rewards = RewardStructure()

    i = 2
    while i < argc:
        if argv[i] not in options:
            print(f"Invalid option '{argv[i]}'.\n{usage}")
            return
        match argv[i]:
            case "-o":
                if i + 1 >= argc or argv[i + 1].startswith("-"):
                    print(f"Missing argument for option '{argv[i]}'.\n{usage}")
                    return
                outfile = argv[i + 1]
                options.remove("-o")
                i += 1
            case "-n":
                if i + 1 >= argc or argv[i + 1].startswith("-"):
                    print(f"Missing argument for option '{argv[i]}'.\n{usage}")
                    return
                name = argv[i + 1]
                if "-o" in options:
                    outfile = factory.default_filepath(name, folder=".")
                options.remove("-n")
                i += 1
            case "-c":
                if i + 3 >= argc:
                    print(f"Missing argument for option '{argv[i]}'.\n{usage}")
                    return
                try:
                    r = int(argv[i + 1])
                    g = int(argv[i + 2])
                    b = int(argv[i + 3])
                except Exception as e:
                    print(e, usage, sep="\n")
                    return
                options.remove("-c")
                i += 3
            case "-td":
                if i + 1 >= argc or argv[i + 1].startswith("-"):
                    print(f"Missing argument for option '{argv[i]}'.\n{usage}")
                    return
                try:
                    td_n = int(argv[i + 1])
                except Exception as e:
                    print(e, usage, sep="\n")
                    return
                options.remove("-td")
                i += 1
            case "-a" | "-g" | "-k" | "-e":
                if i + 1 >= argc or argv[i + 1].startswith("-"):
                    print(f"Missing argument for option '{argv[i]}'.\n{usage}")
                    return
                try:
                    if argv[i] == "-a":
                        alpha = float(argv[i + 1])
                    if argv[i] == "-g":
                        gamma = float(argv[i + 1])
                    if argv[i] == "-k":
                        kappa = float(argv[i + 1])
                    if argv[i] == "-e":
                        epsilon = float(argv[i + 1])
                except Exception as e:
                    print(e, usage, sep="\n")
                    return
                options.remove(argv[i])
                i += 1
            case "-r":
                if i + 4 >= argc:
                    print(f"Missing argument for option '{argv[i]}'.\n{usage}")
                    return
                try:
                    alive = float(argv[i + 1])
                    dead = float(argv[i + 2])
                    green = float(argv[i + 3])
                    red = float(argv[i + 4])
                    rewards.set_rewards(alive, dead, green, red)
                except Exception as e:
                    print(e, usage, sep="\n")
                    return
                i += 4
        i += 1

    try:
        factory.new(filepath=outfile, name=name, color=[r, g, b], alpha=alpha,
                    gamma=gamma, kappa=kappa, epsilon=epsilon, td_n=td_n,
                    rewards=rewards)
    except Exception as e:
        print(e)
        return
    print(f'Agent "{name}" successfully created at "{outfile}".')


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f'Expected command.\n{usage}')
        exit()
    match sys.argv[1]:
        case "gui":
            gui()
        case "info":
            info()
        case "train":
            train()
        case "play":
            play()
        case "new":
            new()
        case _:
            print(f'Unknown command.\n{usage}')
