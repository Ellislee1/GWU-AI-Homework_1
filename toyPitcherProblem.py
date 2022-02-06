import util
from AStar import AStar as A
from Environment import Environment as Env
from FileParser import Parser

path = "Files/test2.txt"

p = Parser()

pitchers, goal = p.parse(path)
assert util.is_valid_problem(pitchers, goal)

env = Env(pitchers, goal)

a = A(env)

print("Naive")
a.run(naive=True)
print("Done")
a.print_path()
print(a.get_steps())

print("None Naive")
a.run(naive=False)
print("Done")
a.print_path()
print(a.get_steps())