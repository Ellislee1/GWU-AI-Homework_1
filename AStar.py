import heapq
import math

import numba as nb
import numpy as np

import util
from Environment import Environment as Env


def rh(state, distance: int, pitchers: np.array, est=0) -> int:
    """Gets the heuristic value (h) for a given state and goal."""

    # base: reached goal state
    if distance == 0:
        return est

    # get the largest amount of water in a cup that is <= the remaining distance
    closest, index = util.find_closest(pitchers, abs(distance))

    # go through the current water levels
    for i, pitcher in enumerate(pitchers):
        if pitcher == abs(distance):
            # If we still need to add water to gaol pitcher
            if distance > 0:
                # if 1 of the cups has the desired water, only 1 step away
                if state[i] == pitcher:
                    return est + 1
                else:
                    return est + 3
            else:
                # if we need to take water out from the goal pitcher:
                # if the perfect cup is empty, only 1 step away (transfer excess out)
                if state[i] == 0:
                    return est + 1
                else:
                    # otherwise, need an additional step to first empty cup and then transfer excess out
                    return est + 2

    # no pitcher small enough to fill difference; best case from here is transfer between 2 pitchers,
    # then transfer to goal
    if abs(distance) < np.min(pitchers):
        return est + 3

    # can still subtract the closest cup without reaching the goal, so recurse
    if distance > 0:
        return rh(state, distance-closest, pitchers, est+2)
    else:
        # target is overflowed, so transfer from goal out to closest match
        return rh(state, distance+closest, pitchers, est+2)


def get_h(state, goal: int, pitchers: np.array) -> int:
    # subtract the amount that's already in the goal pitcher
    distance = goal - state[-1]
    return rh(state, distance, pitchers)


class Node:
    """
        A node in the A* graph.
            - state:        The current state ([<volumes>,steps])
            - parent:       The parent node that created this node
            - g:            Total steps to this point
            - h:            Heuristic value
            - f:            Combination g+h
    """
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
            return (__o.g == self.g).all()
        
        return False
    
    def __lt__(self, __o: object) -> bool:
        if isinstance(__o, Node):
            return __o.f > self.f    
    
    def __gt__(self, __o: object) -> bool:
        if isinstance(__o, Node):
            return __o.f < self.f
    
    def __le__(self, __o: object) -> bool:
         if isinstance(__o, Node):
            return __o.g < self.g
    
    def __hash__(self):
        """Hash function for accessing state in dictionaries"""
        _str = str(int(np.sum(self.state[:-1])))
        for i in range(len(self.state[:-1])):
            _str += f'_{str(int(self.state[i]))}'
        
        return hash(_str)

"""
    A* Algorithm, using 'get_h()' lower bound.
    - env:          The environment to control the pitcher propagation
    - open:         Min-heap (f) on open states
    - open_dict:    An unorderd dictionary of the open hashes, 
                    used for quick access over the heap
    - closed:       An unorordered dictionary of all closed states
    - empty:        Flag for if the open dictionaty is empty 
                    (Used in single step operation only)
    - success:      The best successful terminal state
    - lower:        The g of the best current state (current lb)
    - goal:         The goal value
    - iterations:   A counter of iterations used for verbose output
"""
class AStar:
    def __init__(self, env: Env):
        # suppress printing in scientific notation (easier to read for testing)
        np.set_printoptions(suppress=True)
        self.env = env
        self.open = []
        self.open_dict = dict()
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

        # initial check to see if in the end state
        if self.check_finished(n.state):
            val = self.clear_up(n)
            if self.lower is None or val.n < self.lower:
                self.success = val
                self.lower = val.g

    def step(self, naive=False) -> bool:
        """
            Steps through throught the algorithm
        """

        # Ensure there is values in the open list
        if len(self.open) <= 0:
            return True

        # get min-cost state from min-heap
        q = heapq.heappop(self.open)

        # Handle phantom edge case, rarely called, does not affect code progression
        try:
            del self.open_dict[hash(q)]
        except:
            pass
        
        # Handle adding q to the closed list
        if (hash(q) in self.closed and self.closed[hash(q)].g > q.g) or q not in self.closed:
            self.closed[hash(q)] = q
        
        # Make sure that the current q.g is less than the lower value
        if self.lower is not None and self.lower <= q.g:
            self.end_iter()
            return len(self.open) <= 0
            
        # Generate Q's successors
        successors = np.array(self.env.propagate(q.state[:-1], q.state[-1]))

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
                    self.end_iter()
                    return len(self.open) <= 0

            # Duplicate state detection:
            # check if the current state is in the queue to be explored with a lesser score
            if hash(to_add) in self.open_dict and self.open_dict[hash(to_add)].g <= to_add.g:
                continue
            # Check if the current state has already been visited before (with a smaller score)
            if hash(to_add) in self.closed and self.closed[hash(to_add)].g <= to_add.g:
                continue
            
            if self.lower is None or to_add.f < self.lower:
                heapq.heappush(self.open, to_add)
                self.open_dict[hash(to_add)] = to_add
            else:
                self.closed[hash(to_add)] = to_add


        self.end_iter()
        return len(self.open) <= 0
    
    def end_iter(self):
        if self.iterations % 1000 == 0:
            open_delta, closed_delta = len(self.open) - self.previous[0], len(self.closed) - self.previous[1]
            self.previous[0], self.previous[1] =  len(self.open),  len(self.closed)
            print(f"Iteration {self.iterations}: Closed branches =  {len(self.closed)} [{int(closed_delta)}]| Open branches =  {len(self.open)} [{int(open_delta)}]\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r", end="")
        self.iterations += 1

    def print_path(self):
        path = []
        n = self.success
        while n is not None:
            path.insert(0, n.state[:-1])
            n = n.parent

        print(np.array(path))

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
