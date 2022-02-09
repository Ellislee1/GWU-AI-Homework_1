import numpy as np

"""
    Emvironment class acts as an interface to simulate taking all
    action available from a given initial state.
        - pitchers:     The maximum volume in all pitchers
        - goal:         The goal to reach
        - steps:        The number of steps to reach the current state
        - volumes:      The vurrent volumes in the pitchers in the current
                        state
"""
class Environment:
    def __init__(self, pitchers, goal):
        self.pitchers = pitchers
        self.goal = goal
        self.steps = 0

        self.volumes = np.zeros(len(pitchers) + 1)

    def propagate(self, volumes=None, steps=None):
        """'propagate' simulates all possible valid next steps from the
            current state"""
        
        # Load the state
        if volumes is not None and steps is not None:
            self.load_env_state(volumes, steps)
        
        new_states = []

        new_states = self.get_fill_max(new_states)
        new_states = self.get_empty(new_states)
        new_states = self.get_transfer(new_states)

        return new_states
    
    def get_fill_max(self, states):
        """All Filling states, this ignores filling the infinite pitcher"""
        for i in range(len(self.pitchers)):
            if self.volumes[i] == self.pitchers[i]:
                continue

            copy = np.copy(self.volumes)
            copy[i] = self.pitchers[i]
            states.append(np.append(copy, self.steps + 1))
        
        return states

    def get_empty(self, states):
        """Add Emptying States, Empty all pitchers to 0 
        (if pitcher have some volume)"""
        for i in range(len(self.volumes)):
            if self.volumes[i] == 0:
                continue
            copy = np.copy(self.volumes)
            copy[i] = 0
            states.append(np.append(copy, self.steps + 1))
        
        return states

    def get_transfer(self, states):
        """Add Transfer States by looping through all possible source
        states and destination states and making valid transfers"""
        for i in range(-1, len(self.volumes) - 1):
            if self.volumes[i] == 0:
                continue
            for j in range(-1, len(self.volumes) - 1):
                if i == j:
                    continue
                
                # Dump all into infinate state "-1"
                copy = np.copy(self.volumes)
                if j == -1:
                    transfer = copy[i]
                else:
                    dest_diff = self.pitchers[j] - copy[j]
                    transfer = min(dest_diff, copy[i])

                copy[j] += transfer
                copy[i] -= transfer 
                states.append(np.append(copy, self.steps + 1))
        return states

    def load_env_state(self, volumes, steps):
        self.volumes = volumes
        self.steps = steps

    def get_state(self):
        state = self.volumes.copy()
        state = np.append(state, self.steps)
        return state
