import argparse
import util
from AStar import AStar as A
from Environment import Environment as Env
from FileParser import Parser


default_path = "Files/test2.txt"
default_naive = True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Pitcher files')
    parser.add_argument('--file' , dest='file', type=str, help='Path to the input file')
    parser.add_argument('--naive' , dest='naive', type=str, help='Should the algorithm run naively')

    p = Parser()
    args = parser.parse_args()

    file = args.file if not args.file is None else default_path
    
    pitchers, goal = p.parse(file)
    assert util.is_valid_problem(pitchers, goal)

    env = Env(pitchers, goal)

    a = A(env)

    if args.naive == "True":
        a.run(naive=True)
    elif args.naive == "False":
        a.run(naive=False)
    else:
        a.run(naive=default_naive)
    
    print(f'Path found takes: {a.get_steps()} steps')
    a.print_path()
