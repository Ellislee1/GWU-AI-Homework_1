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

        # All Filling states, this ignores filling the infinite pitcher
        for i in range(len(self.pitchers)):
            if self.volumes[i] == self.pitchers[i]:
                continue

            copy = np.copy(self.volumes)
            copy[i] = self.pitchers[i]
            new_states.append(np.append(copy, self.steps + 1))

        # Add Emptying States, Empty all pitchers to 0 (if pitcher have some volume)
        for i in range(len(self.volumes)):
            if self.volumes[i] == 0:
                continue
            copy = np.copy(self.volumes)
            copy[i] = 0
            new_states.append(np.append(copy, self.steps + 1))

        # Add Transfer States
        for i in range(-1, len(self.volumes) - 1):
            if self.volumes[i] == 0:
                continue
            for j in range(-1, len(self.volumes) - 1):
                if i == j:
                    continue
                
                # Dump all into infinate state "-1"
                if j == -1:
                    copy = np.copy(self.volumes)
                    copy[j] += copy[i]
                    copy[i] = 0
                    new_states.append(np.append(copy, self.steps + 1))
                else:
                    copy = np.copy(self.volumes)
                    dest_diff = self.pitchers[j] - copy[j]
                    worst = min(dest_diff, copy[i])
                    copy[j] += worst
                    copy[i] -= worst

                    new_states.append(np.append(copy, self.steps + 1))

        return new_states

    def load_env_state(self, volumes, steps):
        self.volumes = volumes
        self.steps = steps

    def get_state(self):
        state = self.volumes.copy()
        state = np.append(state, self.steps)
        return state
