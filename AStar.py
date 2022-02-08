import numpy as np
import heapq
import numba as nb
import math

import util
from Environment import Environment as Env


@nb.njit(nogil=True)
def get_h(state, goal: int, pitchers) -> int:
    if goal > np.max(pitchers):
        target = goal - state[-1]
    else:
        target = np.min(goal-state)
    estimate = 0

    # goal pitcher is overflowed: (ideal case) just pour out exact excess into another cup
    if target <= 0:
        return 1

    # find the pitcher closest to the target value
    closest, closest_index = util.find_closest(pitchers, target)
    # get the multiple of that pitcher that gets closest to the target amount
    multiple: int = util.closest_multiple(closest, target)

    # add 2 steps for each multiple (1 to fill, 1 to transfer)
    estimate += multiple * 2
    # subtract a step if cup to use is already fully filled
    if state[closest_index] == pitchers[closest_index]:
        estimate -= 1

    # add 1 step for each filled pitcher (prioritize transferring to goal state)
    # min_diff = min(goal - state[:closest_index:-1])
    # estimate -= min_diff
    for i, amount in enumerate(state[:-1]):
        # check for exact solution
        if target - amount ==0:
            return 1

        # penalize for unnecessarily filling other pitchers
        if i != closest_index and amount > 0 and state[closest_index] == pitchers[closest_index]:
            # avoid double counting ideal (closest) pitcher
            estimate += 1


    return estimate+math.floor(np.min(goal-state)/10)
    





class Node:
    def __init__(self, state, parent, h=0):
        self.state = np.copy(state)
        self.parent = parent
        self.g = state[-1]
        self.h = h
        self.f = self.g + self.h

    def __str__(self) -> str:
        return f"{self.state}, f: {self.f}"

    def __eq__(self, __o: object) -> bool:

        if isinstance(__o, Node):
            return (__o.state[:-1] == self.state[:-1]).all()
        
        return False
    
    def __lt__(self, __o: object) -> bool:
        if isinstance(__o, Node):
            return __o.f > self.f    
    
    def __gt__(self, __o: object) -> bool:
        if isinstance(__o, Node):
            return __o.f < self.f
    
    def __hash__(self):
        _str = str(int(np.sum(self.state[:-1])))
        for i in range(len(self.state[:-1])):
            _str += f'_{str(int(self.state[i]))}'
        
        return hash(_str)

class AStar:
    def __init__(self, env: Env):
        # suppress printing in scientific notation (easier to read for testing)
        np.set_printoptions(suppress=True)
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

    def print_path(self):
        path = []

        n = self.success

        while n is not None:
            path.insert(0, n.state[:-1])
            n = n.parent

        print(path)

    def get_steps(self) -> int:
        if self.success is None:
            return -1
        return self.success.g

    def list_open(self):
        for node in self.open:
            print(node)

    def list_closed(self):
        for node in self.closed:
            print(node)

    def step(self, naive=False) -> bool:
        if len(self.open) <= 0:
            return True

        # get min-cost state from min-heap
        q = heapq.heappop(self.open)
        try:
            del self.open_dict[hash(q)]
        except:
            pass

        if hash(q) in self.closed and self.closed[hash(q)].g > q.g:
            self.closed[hash(q)] = q
        elif q not in self.closed:
            self.closed[hash(q)] = q
        
        if self.lower is not None and self.lower <= q.f:
            self.iterations += 1
            return len(self.open) <= 0
            
        # Generate Q's successors
        successors = self.env.propagate(q.state[:-1], q.state[-1])
        # Add to open
        for state in successors:
            to_add = Node(state, q, get_h(state[:-1], self.goal, self.env.pitchers))
            if self.check_finished(state):
                val = self.clear_up(to_add)
                if naive:
                    self.success = val
                    return True
                if self.lower is None or val.g < self.lower:
                    self.success = val
                    self.lower = val.g

            to_add = Node(state, q, get_h(state[:-1], self.goal, self.env.pitchers))
            skip = False

            # Duplicate state detection:
            # check if the current state is in the queue to be explored with a lesser score
            if hash(to_add) in self.open_dict and self.open_dict[hash(to_add)].f <= to_add.f:
                if not(to_add.state[:-1] == self.open_dict[hash(to_add)].state[:-1]).all():
                    print(to_add.state[:-1], self.open_dict[hash(to_add)].state[:-1])
                continue
            # Check if the current state has already been visited before (with a smaller score)
            if hash(to_add) in self.closed and self.closed[hash(to_add)].f <= to_add.f:
                if not(to_add.state[:-1] == self.closed[hash(to_add)].state[:-1]).all():
                    print(to_add.state[:-1], self.closed[hash(to_add)].state[:-1])
                continue
            
            if self.lower is None or to_add.f < self.lower:
                heapq.heappush(self.open, to_add)
                self.open_dict[hash(to_add)] = to_add
            else:
                self.closed[hash(to_add)] = to_add

        # self.close_stale()
        if self.iterations % 500 == 0:
            open_delta, closed_delta = len(self.open) - self.previous[0], len(self.closed) - self.previous[1]
            self.previous[0], self.previous[1] =  len(self.open),  len(self.closed)
            print(f"Iteration {self.iterations}: Closed branches =  {len(self.closed)} [{int(closed_delta)}]| Open branches =  {len(self.open)} [{int(open_delta)}]\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r", end="")
        self.iterations += 1
        return len(self.open) <= 0

    def check_finished(self, state) -> bool:
        # see if the infinite cup has teh desired quantity
        return state[-2] == self.env.goal

    def run(self, naive=False):
        if util.is_valid_problem(self.env.pitchers, self.goal):
            while not self.empty:
                self.empty = self.step(naive)
            print(f"\t\t\t\t\t\t\t\nIteration {self.iterations}: Closed branches =  {len(self.closed)}| "
                  f"Open branches =  {len(self.open)}\t\t\t\t\t\t\t\t\t")

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
