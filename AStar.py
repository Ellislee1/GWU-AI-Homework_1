import numpy as np
from Environment import Environment as Env

class Node:
    def __init__(self, state, parent, g=0, h=0):
        self.state = state
        self.parent = parent
        self.g = g
        self.h = h
        self.f = g+h

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
        return self.open
    
    def list_closed(self):
        return self.closed
    
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

        self.closed.append(q)
        return len(self.open) <= 0

    def run(self):
        while not self.empty:
            print("Here")
            self.empty = self.step()

