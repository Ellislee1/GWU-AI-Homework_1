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

    def proporgate(self, volumes, steps):
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

    # def fill (self, source, dest):
    #     if source == -2:
    #         if dest != -1:
    #             self.volumes[dest] = self.pitchers[dest]
    #             self.steps += 1
    #     else:
    #         if dest == -1 and self.volumes[source] > 0:
    #             self.volumes[-1] += self.volumes[source]
    #             self.volumes[source] = 0
    #             self.steps += 1

    #         elif dest == -2 and self.volumes[source] > 0:
    #             print("Here")
    #             self.volumes[source] = 0
    #             self.steps += 1
    #         else:

    #             dest_diff = self.pitchers[dest] - self.volumes[dest]
    #             source_val = self.volumes[source]

    #             if source_val > 0 and dest_diff > 0:
    #                 print(source_val, dest_diff)
    #                 worst = min(source_val,dest_diff, )
    #                 to_move = dest_diff - (dest_diff-worst)
    #                 self.volumes[dest] += to_move
    #                 self.volumes[source] -= to_move

    #                 self.steps += 1
    #     self.get_h()

    def get_state(self):
        state = self.volumes.copy()
        state = np.append(state, self.steps)
        return state

    # def get_h(self):
    #     cur_dist = self.get_distance()

    #     # Get the distances for filling a pitcher
    #     for i in range(len(self.actions["Fill"])):
    #         if self.volumes[i] == self.pitchers[i]:
    #             self.actions["Fill"][i] = inf
    #             continue

    #         copy = self.volumes.copy()
    #         copy[i] = self.pitchers[i]
    #         self.actions["Fill"][i] = self.get_experimental_dist(copy)

    #     # Get the distance for emptying a pitcher
    #     for i in range(-1,len(self.pitchers)):
    #         if self.volumes[i] == 0:
    #             self.actions["Empty"][i] = inf
    #             continue

    #         # Add distance code
    #         copy = self.volumes.copy()
    #         copy[i] = 0
    #         self.actions["Empty"][i] = self.get_experimental_dist(copy)

    #     # Get the distance for transfering liquid
    #     for i in range(-1,len(self.pitchers)):
    #         # Cannot transfer if there is nothing in pitcher[i], so continue
    #         if self.volumes[i] == 0:
    #             for j in range(-1,len(self.pitchers)):
    #                 self.actions["Transfer"][i,j] = inf
    #             continue

    #         for j in range(-1,len(self.pitchers)):
    #             # Can not transfer volume to itsself
    #             if i == j:
    #                 continue

    #             # Cannot transfer to an already full container
    #             if j >= 0 and self.volumes[j] == self.pitchers[j]:
    #                 self.actions["Transfer"][i,j] = inf
    #                 continue

    #             if j == -1: # Add distance code copy = self.volumes.copy()
    #                 copy[j] += self.volumes[i] copy[i] = 0
    #                 self.actions["Transfer"][i,j] =
    #                 self.get_experimental_dist(copy) continue

    #             # Add distance code
    #             copy = self.volumes.copy() diff = self.pitchers[j] - copy[j]
    #             move = min(diff, copy[i]) copy[i] -= move copy[j] += move
    #             self.actions["Transfer"][i,j] =
    #             self.get_experimental_dist(copy)
