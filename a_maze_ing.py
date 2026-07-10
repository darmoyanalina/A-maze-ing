import sys
import random
from typing import Any
from queue import Queue
from mazegen import Config, MazeGenerator
from mazegen.amazing_class import clear_terminal


def read_input() -> dict[str, Any] | None:
    configs: dict[str, Any] = {}
    try:
        file: str = sys.argv[1]
        with open(file, 'r') as config:
            for line in config:
                if not line.strip() or line.startswith('#'):
                    continue
                key, value = line.strip().split('=', 1)
                configs[key] = value
        configs['ENTRY'] = tuple(int(item.strip())
                                 for item in configs['ENTRY'].split(","))
        configs['EXIT'] = tuple(int(item.strip())
                                for item in configs['EXIT'].split(","))
        return configs
    except IndexError:
        print('USAGE: "python3 a_maze_ing.py <config>"')
        exit()


if __name__ == '__main__':
    try:
        conf: Config = Config.model_validate(read_input())
        if conf.SEED:
            random.seed(conf.SEED)
    except FileNotFoundError as e:
        print(f"[KO] - {e}")
        exit()
    except Exception:
        print("[KO] - Config file invalid")
        exit()

    try:
        our_maze = MazeGenerator(conf)
        our_maze.generate()
        our_maze.find_path()
        print("=== A-Maze-ing ===")
        print("1. Re-generate a new maze")
        print("2. Show / Hide the shortest path")
        print("3. Rotate the wall colors")
        print("4. Quit")
        showed: bool = True
        inp: str = input("Choice? (1-4): ")
        while "1" <= (inp) < "4":
            if inp == "1":
                our_maze = MazeGenerator(conf)
                if conf.SEED:
                    random.seed()
                our_maze.generate()
                print("=== A-Maze-ing ===")
                print("1. Re-generate a new maze")
                print("2. Show / Hide the shortest path")
                print("3. Rotate the wall colors")
                print("4. Quit")
                inp = input("Choice? (1-4): ")
                showed = False
            elif inp == "2":
                if showed:
                    our_maze.generate()
                    showed = False
                else:
                    our_maze.queue = Queue()
                    our_maze.find_path()
                    showed = True
                print("=== A-Maze-ing ===")
                print("1. Re-generate a new maze")
                print("2. Show / Hide the shortest path")
                print("3. Rotate the wall colors")
                print("4. Quit")
                inp = input("Choice? (1-4): ")
            elif inp == "3":
                clear_terminal()
                our_maze.visualize(conf.OUTPUT_FILE, random.randint(40, 47))
                print("=== A-Maze-ing ===")
                print("1. Re-generate a new maze")
                print("2. Show / Hide the shortest path")
                print("3. Rotate the wall colors")
                print("4. Quit")
                inp = input("Choice? (1-4): ")
            else:
                break
    except Exception as e:
        print(f'Error - {e}')
        exit()
