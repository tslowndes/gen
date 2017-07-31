import numpy as np
def dist(pos1, pos2, nd):
    if nd == 2:
        return np.sqrt(((pos1[0] - pos2[0])**2) + ((pos1[1] - pos2[1])**2))
    elif nd == 3:
        return np.sqrt(((pos1[0] - pos2[0]) ** 2) + ((pos1[1] - pos2[1]) ** 2) + ((pos1[2] - pos2[2]) ** 2))