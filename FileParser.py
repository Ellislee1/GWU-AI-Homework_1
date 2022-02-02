import numpy as np


def formatter(string, chars):
    for c in chars:
        string.replace(c, "")
    return string.split(",")


class Parser:
    def parse(self, path):
        file = open(path, "r")
        lines = file.readlines()

        pitchers = np.array(list(map(int, formatter(lines[0], [" ", "\n"]))))
        target = int(lines[1])

        file.close()

        print(f"Pitchers: {pitchers}, Target volume: {target}")

        return (pitchers, target)
