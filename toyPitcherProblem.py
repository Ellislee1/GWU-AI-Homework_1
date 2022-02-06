import util
from AStar import AStar as A
from Environment import Environment as Env
from FileParser import Parser


def compute_problem(path: str) -> int:
    p = Parser()
    pitchers, goal = p.parse(path)
    if not util.is_valid_problem(pitchers, goal):
        return -1

    env = Env(pitchers, goal)
    # print(env)

    # test2(env)
    a = A(env)

    a.run(naive=False)
    print("Done")
    a.print_path()
    print(a.get_steps())
    return a.get_steps()


if __name__ == "__main__":
    file_path = "Files/test2.txt"
    steps = compute_problem(file_path)
    print('Number of steps: ', steps)

