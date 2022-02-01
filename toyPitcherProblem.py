from parser import parse
from Environment import Environment as Env
from TestPrograms.testp1 import *
from AStar import AStar as A

path = "Files/test1.txt"

pitchers,goal = parse(path)

env = Env(pitchers,goal)
# print(env)

# test2(env)

a = A(env)


a.run()
print(a.success)