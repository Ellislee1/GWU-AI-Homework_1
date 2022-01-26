from this import d
import numpy as np

class Environment:
    def __init__(self, pitchers, goal):
        self.pitchers = pitchers
        self.goal = goal
        self.steps = 0

        self.volumes = np.zeros(len(pitchers)+1)
    
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
            
            else:
            
                dest_diff = self.pitchers[dest] - self.volumes[dest]
                source_val = self.volumes[source]
                

                if source_val > 0 and dest_diff > 0:
                    worst = min(source_val,dest_diff)

                    to_move = dest_diff - (dest_diff-worst)

                    self.volumes[dest] += to_move
                    self.volumes[source] -= to_move

                    self.steps += 1

    def get_state(self):
        return self.volumes

    def get_distance(self):
        return np.abs(self.goal - np.sum(self.volumes))
    
    def __str__(self) -> str:
        headers = ""

        for i in self.pitchers:
            headers += f'{i}\t'
        
        headers += "Inf"

        volumes = ""

        for i in self.volumes:
            volumes += f'{i}\t'

        return f'\n---------------------------------\n------ Current Environment ------\n---------------------------------'\
        f'\n{headers}\n{volumes}\n\nDistance: {self.get_distance()}\n\n\t\t Total Steps: {self.steps}'