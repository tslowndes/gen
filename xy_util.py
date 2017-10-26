from math import atan, degrees
from numpy import abs
import numpy as np

def find_dir(pos1, pos2):
    dx = pos2[0] - pos1[0]
    dy = pos2[1] - pos1[1]

    if dy == 0:
        if pos2[0] > pos1[0]:
            return 90
        else:
            return 270
    else:
        theta = np.degrees(np.arctan2(dx,dy))
        if theta >= 0:
            return theta
        else:
            return theta + 360

def find_dist(pos1, pos2):
    return np.sqrt(np.sum((pos1 - pos2)**2))
