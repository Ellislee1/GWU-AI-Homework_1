import numpy as np

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


class AStar:
    def __init__(self, env: Env):
        self.env = env
        self.open = []
        self.closed = []

        self.open.append(Node(self.env.get_state(), None))
        self.empty = False
        self.success = None
        self.lower = None
        self.total_explored = 99
        self.goal = self.env.goal
        self.iterations = 0

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

        if target < 0:
            estimate = 1
            return estimate

        closest, closest_index = util.find_closest(self.env.pitchers, target)
        multiple: int = util.closest_multiple(closest, target)

        # add 2 steps for each multiple (1 to fill, 1 to transfer)
        estimate += multiple*2

        # now subtract steps for pitchers that are already filled
        if state[closest_index] > 0:
            estimate -= 1

        # add 1 step for each filled pitcher (prioritize transferring to goal state)
        for i, amount in enumerate(state[:-2]):
            if amount > 0:
                estimate += 1

            # if 1 of the pitchers matches the remaining amount, use that
            if target - self.env.pitchers[i] == 0:
                estimate = 1
                return estimate

        return estimate

    def step(self, naive=True) -> bool:
        if not self.runnable:
            return True

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

        # print(f'low index: {low_index}, low_f: {low_f}')
        q = self.open.pop(low_index)
        # print("q: ", q)
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
            for i in range(len(self.open)):
                if self.open[i] == to_add and self.open[i].f < to_add.f:
                    skip = True
                    break
            if skip:
                continue

            for i in range(len(self.closed)):
                if self.closed[i] == to_add and self.closed[i].g < to_add.f:
                    skip = True
                    break
            if skip:
                continue
            self.open.append(to_add)
            self.closed.append(q)
        self.close_stale()
        if self.iterations % 25 == 0:
            print(f"Iteration:{self.iterations}: Closed branches =  {len(self.closed)} | Open branches =  {len(self.open)}")
        self.iterations += 1
        return len(self.open) <= 0

    def close_stale(self):
        if self.lower == None:
            return

        new_open = []

        
        for node in self.open:
            if node.f < self.lower:
                new_open.append(node)
            else:
                self.closed.append(node)

        self.open = new_open.copy()
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
        self.closed.append(node)
        success_index = np.where(node.state[:-1] == self.env.goal)[0]

        # print(node.state[:-1][-1], self.env.goal)
        if not node.state[:-1][-1] == self.env.goal:
            new_state = np.copy(node.state)
            if not node.state[:-1][-1] == 0:
                new_state[-2] = 0
                new_state[-1] += 1
                node = Node(new_state, node)
                self.closed.append(node)

            new_state[-2] = self.env.goal
            new_state[-1] += 1
            new_state[success_index] = 0
            node = Node(new_state, node)
            self.closed.append(node)

        return node
