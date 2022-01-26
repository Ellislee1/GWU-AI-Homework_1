from parser import parse
from Environment import Environment as Env

path = "Files/test1.txt"

pitchers,goal = parse(path)

env = Env(pitchers,goal)
print(env)

env.fill(-2,1)
print(env)

env.fill(1,-1)
print(env)

env.fill(-2,1)
print(env)

env.fill(1,-1)
print(env)

env.fill(-1,0)
print(env)

env.fill(-1,1)
print(env)

print(env.get_state())

