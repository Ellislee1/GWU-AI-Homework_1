import numpy as np
import heapq

import util
from Environment import Environment as Env


class Node:
    def __init__(self, state, parent, h=0):
        self.state = np.copy(state)
        self.parent = parent
        self.g = state[-1]
        self.h = h
        self.f = self.g + self.h

    def __str__(self) -> str:
        return f"{self.state}, {self.f}"

    def __eq__(self, __o: object) -> bool:

        if isinstance(__o, Node):
            return (__o.state[:-1] == self.state[:-1]).all()
        
        return False
    
    def __lt__(self, __o: object) -> bool:
        if isinstance(__o, Node):
             return __o.f < self.f        
        return False
    
    def __hash__(self):
        _str = ""
        for i in range(len(self.state[:-1])):
            _str += str(int(self.state[i]))
        return int(_str)

class AStar:
    def __init__(self, env: Env):
        self.env = env
        self.open = []
        self.open_dict = {}
        self.closed = {}

        n = Node(self.env.get_state(), None)
        heapq.heappush(self.open, n)
        self.open_dict[hash(n)] = n
        self.empty = False
        self.success = None
        self.lower = None
        self.goal = self.env.goal
        self.iterations = 0

        self.previous = np.zeros(2)

        self.initilise()
    
    def initilise(self):
        pitchers = self.env.pitchers
        gcd = np.gcd.reduce(pitchers)
        
        if gcd <= self.goal and self.goal % gcd == 0:
            self.runnable = True
        else:
            self.runnable = False

    def print_path(self):
        path = []

        n = self.success

        while n is not None:
            path.insert(0, n.state[:-1])
            n = n.parent

        print(path)

    def get_steps(self) -> int:
        if self.success is None:
            return None
        return self.success.g

    def list_open(self):
        for node in self.open:
            print(node)

    def list_closed(self):
        for node in self.closed:
            print(node)

    def get_h(self, state) -> int:
        target = self.env.goal - state[-1]
        estimate = 0

        # goal pitcher is overflowed: (ideal case) just pour out exact excess into another cup
        if target < 0:
            return 1

        closest, closest_index = util.find_closest(self.env.pitchers, target)
        multiple: int = util.closest_multiple(closest, target)

        # add 2 steps for each multiple (1 to fill, 1 to transfer)
        estimate += multiple*2

        # now subtract steps for pitchers that are already filled
        # subtract a step if cup to use is already filled
        if state[closest_index] > 0:
            estimate -= 1

        # add 1 step for each filled pitcher (prioritize transferring to goal state)
        for i, amount in enumerate(state[:-2]):
            if i != closest_index and amount > 0:
                estimate += 1

            # check for exact solution
            if target - self.env.pitchers[i] == 0:
                return 1

        return estimate

    def step(self, naive=True) -> bool:
        if not self.runnable:
            return True

        if len(self.open) <= 0:
            return True

        q = heapq.heappop(self.open)
        try:
            del self.open_dict[hash(q)]
        except:
            pass

        if hash(q) in self.closed and self.closed[hash(q)].g > q.f:
            self.closed[hash(q)] = q
        elif not q in self.closed:
            self.closed[hash(q)] = q
            
        # Generate Q's successors
        successors = self.env.propagate(q.state[:-1], q.state[-1])
        # Add to open
        for state in successors:
            if self.check_finished(state):
                n = Node(state, q, self.get_h(state))

                val = self.clear_up(n)

                if naive:
                    self.success = val
                    return True
                if self.lower is None or val.g < self.lower:
                    self.success = val
                    self.lower = val.g

            to_add = Node(state, q, self.get_h(state[:-1]))
            skip = False

            if hash(to_add) in self.open_dict and self.open_dict[hash(to_add)].g < q.f:
                continue

            if hash(to_add) in self.closed and self.closed[hash(to_add)].g < q.f:
            # if self.closed[i] == to_add and self.closed[i].g < to_add.f:
                continue
            
            if self.lower is None or to_add.f < self.lower:
                heapq.heappush(self.open, to_add)
                self.open_dict[hash(to_add)] = to_add
            else:
                self.closed[hash(to_add)] = to_add

        # self.close_stale()
        if self.iterations % 1000 == 0:
            open_delta, closed_delta = len(self.open) - self.previous[0], len(self.closed) - self.previous[1]
            self.previous[0], self.previous[1] =  len(self.open),  len(self.closed)
            print(f"Iteration:{self.iterations}: Closed branches =  {len(self.closed)} [{closed_delta}]| Open branches =  {len(self.open)} [{open_delta}]")
        self.iterations += 1
        return len(self.open) <= 0

    def close_stale(self):
        if self.lower == None:
            return

        new_open = []
        new_open_dict = {}

        for node in self.open:
            if node.f < self.lower and not hash(node) in self.closed:
                heapq.heappush(new_open, node)
                new_open_dict[hash(node)] = node
            else:
                if hash(node) in self.closed and self.closed[hash(node)].g > node.f:
                    self.closed[hash(node)] = node
                elif not node in self.closed:
                    self.closed[hash(node)] = node
                # self.closed.add(node)

        self.open = new_open.copy()
        self.open_dict = new_open_dict
        # print(len(self.open), len(self.closed), self.lower)

    def check_finished(self, state) -> bool:
        for elem in state[:-1]:
            if elem == self.env.goal:
                return True
        return False

    def run(self, naive=True):
        while not self.empty:
            self.empty = self.step(naive)

    def clear_up(self, poss):
        node = poss
        self.closed[hash(node)] = node
        success_index = np.where(node.state[:-1] == self.env.goal)[0]

        # print(node.state[:-1][-1], self.env.goal)
        if not node.state[:-1][-1] == self.env.goal:
            new_state = np.copy(node.state)
            if not node.state[:-1][-1] == 0:
                new_state[-2] = 0
                new_state[-1] += 1
                node = Node(new_state, node)
                self.closed[hash(node)] = node

            new_state[-2] = self.env.goal
            new_state[-1] += 1
            new_state[success_index] = 0
            node = Node(new_state, node)
            self.closed[hash(node)] = node

        return node
