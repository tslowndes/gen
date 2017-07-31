from __future__ import division
import sys
from math import ceil
from datetime import datetime
import time


def update_progress(curr, outof):
    prg = (curr/outof)*100
    sys.stdout.write("\r%i%%" % prg)
    sys.stdout.flush()

def print_time(elps_time):
    if elps_time == 0:
        print("Time started:  " + datetime.now().strftime("%I:%M%p"))
    else:
        print("Time Finished:  " + datetime.now().strftime("%I:%M%p"))

if __name__ =="__main__": test()
