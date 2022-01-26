"""
    Parser to open a file and split it into the size (contents) of jugs and some goal
"""

import numpy as np

def parse(path):
    file = open(path, 'r')
    lines = file.readlines()

    pitchers = np.array(list(map(int,lines[0].replace(' ','').replace('\n','').split(','))))
    target = int(lines[1])

    file.close()

    print(f'Pitchers: {pitchers}, Target volume: {target}')

    return (pitchers,target)