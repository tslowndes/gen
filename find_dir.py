from math import atan, degrees
from numpy import abs

def find_dir(x1, y1, x2, y2):
    if x2 < x1 and y2 < y1:
        dir = degrees(atan(abs(y1 - y2)/abs(x1 - x2))) + 180
    elif x2 < x1 and y2 > y1:
        dir = 180 - degrees(atan(abs(y1 - y2)/abs(x1 - x2)))
    elif x2 > x1 and y2 > y1:
        dir = degrees(atan(abs(y1 - y2)/abs(x1 - x2)))
    elif x2 > x1 and y2 < y1:
        dir = 360 - degrees(atan(abs(y1 - y2)/abs(x1 - x2)))
    elif x1 == x2 and y2 > y1:
        dir = 90
    elif x1 == x2 and y2 < y1:
        dir = 270
    elif x1 > x2 and y2 == y1:
        dir = 180
    elif x1 < x2 and y2 == y1:
        dir = 0

    return dir
