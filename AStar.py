import numpy as np
from Environment import Environment as Env

class Node:
    def __init__(self, state, parent, h=0):
        self.state = state
        self.parent = parent
        self.g = state[-1]
        self.h = h
        self.f = self.g+self.h
        self.success = None

    def __str__(self) -> str:
        return f'{self.state}, {self.f}'


class AStar():
    def __init__(self, env: Env):
        self.env = env
        self.open = []
        self.closed = []

        self.open.append(Node(self.env.get_state(), None))
        self.empty = False
    
    def list_open(self):
        for node in self.open:
            print(node)
    
    def list_closed(self):
        for node in self.closed:
            print(node)
    
    def get_h(self, state):
        goal = self.env.goal
        total = np.sum(state)
        diffs = abs(state-goal)
        return min(diffs)+(0.2*total)
    
    def step(self):
        if len(self.open) <= 0:
            return True

        # Get lowest f
        low_index, low_f = 0, self.open[0].f

        if len(self.open) > 1:
            for i in range(1, len(self.open)):
                new_f = self.open[i].f
                if new_f < low_f:
                    low_f = new_f
                    low_index = i
        
        q = self.open.pop(low_index)
        # Generate Q's successors
        successors = self.env.proporgate(q.state[:-1],q.state[-1])
        print(successors)
        # Add to open
        for state in successors:
            if self.check_finished(state):
                self.success = state
                return True
            self.open.append(Node(state,q, self.get_h(state[:-1])))


        self.closed.append(q)
        return len(self.open) <= 0
    
    def check_finished(self, state) -> bool:
        for elem in state[:-1]:
            if elem == self.env.goal:
                return True
        return False


    def run(self):
        while not self.empty:
            self.empty = self.step()

