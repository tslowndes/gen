from Config_class import *
import csv
import numpy as np

def main_set_up():
    config = sim_config('../Voronoi/3D/config/sim_config_DO_NOT_DELETE.csv')
    swarm_size_range = (5, 30)
    sim_no = 0

    for i in range(swarm_size_range[0], swarm_size_range[1]):
        config.no = sim_no
        config.repeats = 10
        config.run_time = 10000
        config.swarm_size = i
        config.seed = [0, 1, 2, 3, 4, 5, 7, 8, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 21, 24, 25, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57]

        filename = '../Voronoi/3D/config/sim_config_%03i.csv' % sim_no
        write_class_attributes(config, filename)

        sim_no += 1


def write_class_attributes(wr_class, filename):
    attributes = [i for i in dir(wr_class) if '__' not in i]
    attributes.remove('read_config')

    f = open(filename, 'w', newline='')
    wr = csv.writer(f)
    for attr in attributes:
        wr.writerow([attr, getattr(wr_class, attr)])
    f.close()


if __name__=='__main__': main_set_up()