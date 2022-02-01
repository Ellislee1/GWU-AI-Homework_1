from readline import get_history_item
from this import d
import numpy as np
from math import inf

class Environment:
    def __init__(self, pitchers, goal):
        self.pitchers = pitchers
        self.goal = goal
        self.steps = 0

        self.volumes = np.zeros(len(pitchers)+1)

        self.actions = {}

        self.actions["Fill"] = np.full(len(pitchers), np.inf)
        self.actions["Empty"] = np.full(len(pitchers)+1, np.inf)
        self.actions["Transfer"] = np.full((len(pitchers)+1,len(pitchers)+1), np.inf)

        self.get_h()
    
    def fill (self, source, dest):
        if source == -2:
            if dest != -1:
                self.volumes[dest] = self.pitchers[dest]
                self.steps += 1
        else:
            if dest == -1 and self.volumes[source] > 0:
                self.volumes[-1] += self.volumes[source]
                self.volumes[source] = 0
                self.steps += 1
            
            elif dest == -2 and self.volumes[source] > 0:
                print("Here")
                self.volumes[source] = 0
                self.steps += 1
            else:
            
                dest_diff = self.pitchers[dest] - self.volumes[dest]
                source_val = self.volumes[source]
                

                if source_val > 0 and dest_diff > 0:
                    print(source_val, dest_diff)
                    worst = min(source_val,dest_diff, )
                    to_move = dest_diff - (dest_diff-worst)
                    self.volumes[dest] += to_move
                    self.volumes[source] -= to_move

                    self.steps += 1
        self.get_h()

    def get_state(self):
        state = self.volumes.copy()
        state = np.append(state, 0)
        return state

    def get_h(self):
        cur_dist = self.get_distance()

        # Get the distances for filling a pitcher
        for i in range(len(self.actions["Fill"])):
            if self.volumes[i] == self.pitchers[i]:
                self.actions["Fill"][i] = inf
                continue
            
            copy = self.volumes.copy()
            copy[i] = self.pitchers[i]
            self.actions["Fill"][i] = self.get_experimental_dist(copy)
        
        # Get the distance for emptying a pitcher
        for i in range(-1,len(self.pitchers)):
            if self.volumes[i] == 0:
                self.actions["Empty"][i] = inf
                continue

            # Add distance code
            copy = self.volumes.copy()
            copy[i] = 0
            self.actions["Empty"][i] = self.get_experimental_dist(copy)

        # Get the distance for transfering liquid
        for i in range(-1,len(self.pitchers)):
            # Cannot transfer if there is nothing in pitcher[i], so continue
            if self.volumes[i] == 0:
                for j in range(-1,len(self.pitchers)):
                    self.actions["Transfer"][i,j] = inf
                continue

            for j in range(-1,len(self.pitchers)):
                # Can not transfer volume to itsself
                if i == j:
                    continue
                
                # Cannot transfer to an already full container
                if j >= 0 and self.volumes[j] == self.pitchers[j]:
                    self.actions["Transfer"][i,j] = inf
                    continue

                if j == -1:
                    # Add distance code
                    copy = self.volumes.copy()
                    copy[j] += self.volumes[i]
                    copy[i] = 0
                    self.actions["Transfer"][i,j] = self.get_experimental_dist(copy)
                    continue

                # Add distance code
                copy = self.volumes.copy()
                diff = self.pitchers[j] - copy[j]
                move = min(diff, copy[i])
                copy[i] -= move
                copy[j] += move
                self.actions["Transfer"][i,j] = self.get_experimental_dist(copy)

    def get_distance(self):
        return np.abs(self.goal - np.sum(self.volumes))
    
    # Used for getting the example costs (distances) NOT IMPLIMENTED
    def get_experimental_dist(self, state):
        return np.inf
    
    def __str__(self) -> str:
        headers = ""

        for i in self.pitchers:
            headers += f'{i}\t'
        
        headers += "Inf"

        volumes = ""

        for i in self.volumes:
            volumes += f'{i}\t'

        return f'\n---------------------------------\n------ Current Environment ------\n---------------------------------'\
        f'\n{headers}\n{volumes}\n\nDistance: {self.get_distance()}\n{self.actions}\n\n\t\t Total Steps: {self.steps}'