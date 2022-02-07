import argparse
import util
from AStar import AStar as A
from Environment import Environment as Env
from FileParser import Parser
import time


default_path = "Files/test3.txt"
default_naive = True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Pitcher files')
    parser.add_argument('--file' , dest='file', type=str, help='Path to the input file')
    parser.add_argument('--naive' , dest='naive', type=str, help='Should the algorithm run naively')
    parser.add_argument('--path' , dest='path', type=str, help='Should the algorithm run naively', default="False")

    p = Parser()
    args = parser.parse_args()

    file = args.file if args.file is not None else default_path

    pitchers, goal = p.parse(file)
    if util.is_valid_problem(pitchers, goal):
        env = Env(pitchers, goal)

        a = A(env)

        if args.naive.title() == "True":
            start = time.perf_counter()
            a.run(naive=True)
        elif args.naive.title() == "False":
            start = time.perf_counter()
            a.run(naive=False)
        else:
            start = time.perf_counter()
            a.run(naive=default_naive)
        end = time.perf_counter()
        if args.path.title() == "True":
            a.print_path()
        print(f'Path found takes: {a.get_steps()} steps (That took {(end-start):.3g} seconds)')
    else:
        print(f'Path found takes: -1 steps (No solution possible)')
