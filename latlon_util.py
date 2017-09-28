import numpy as np
from math import floor
def find_dir(pos1, pos2):
    lon1, lat1 = np.radians(pos1)
    lon2, lat2 = np.radians(pos2)
    Y = np.cos(lat2) * np.sin(lon2 - lon1)
    X = (np.cos(lat1) * np.sin(lat2)) - (np.sin(lat1) * np.cos(lat2) * np.cos(lon2 - lon1))
    dir = np.arctan2(Y, X)
    dir = np.degrees(dir) + 360 % 360
    if dir < 0:
        dir = dir + 360
    return dir

def find_dist2(pos1, pos2):
    """
    Calculates distance between two lat lon points using the haversine formula
    """
    lon1, lat1 = np.radians(pos1)
    lon2, lat2 = np.radians(pos2)
    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = (np.sin(dlat / 2)** 2) + (np.cos(lat1) * np.cos(lat2) * (np.sin(dlon / 2) ** 2))
    r = 6378.137 * 1000  # Radius of earth in kilometers
    d = 2 * r * np.arcsin(np.sqrt(a))
    return d


def find_dist3(pos1, pos2):
    """
    Calculates distance between two lat lon points using the haversine formula then pythag for z
    """
    dist_xy = find_dist2((pos1[0], pos1[1]), (pos2[0], pos2[1]))
    dist_xyz = np.sqrt((dist_xy ** 2) + ((pos1[2] - pos2[2])**2))
    return dist_xyz

def find_relative(datum, loc):
    """
    Finds the position of loc relative to datum in x/y meter coordinates.
    """
    loc1 = datum
    loc2 = loc

    # finds change in lon and lat using haversine formula to determine loc relative to datum
    dlon = find_dist2(loc1, (loc2[0], loc1[1]))
    dlat = find_dist2(loc1, (loc1[0], loc2[1]))

    relloc2 = (dlon, dlat)

    return relloc2