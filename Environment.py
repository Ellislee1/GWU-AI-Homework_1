import numpy as np


class Environment:
    def __init__(self, pitchers, goal):
        self.pitchers = pitchers
        self.goal = goal
        self.steps = 0

        self.volumes = np.zeros(len(pitchers) + 1)

        self.actions = {}

        self.actions["Fill"] = np.full(len(pitchers), np.inf)
        self.actions["Empty"] = np.full(len(pitchers) + 1, np.inf)
        self.actions["Transfer"] = np.full(
            (len(pitchers) + 1, len(pitchers) + 1), np.inf
        )

        # self.get_h()

    def propagate(self, volumes, steps):
        self.volumes = volumes
        self.steps = steps

        new_states = []

        # All Filling states
        for i in range(len(self.pitchers)):
            if self.volumes[i] == self.pitchers[i]:
                continue

            copy = np.copy(self.volumes)
            copy[i] = self.pitchers[i]
            new_states.append(np.append(copy, self.steps + 1))

        # Add Emptying States
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

    def get_state(self):
        state = self.volumes.copy()
        state = np.append(state, self.steps)
        return state
