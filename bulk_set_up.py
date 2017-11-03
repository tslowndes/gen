from Config_class import *
import csv
import numpy as np
from math import ceil

def main_set_up():
    config = sim_config('../Voronoi/3D/config/sim_config_DO_NOT_DELETE.csv')

    sim_no = 0
    comms = 2
    for i in range(5,21):

        # 0:Sat only, 1:Acc & Sat, 2:Ideal
        config.comms = comms
        # Range of accoustic communication
        if config.comms == 2:
            config.comms_range = 9999999999999999999
        else:
            config.comms_range = 500

        # Desired separation for voronoi algorithm in meters
        config.desired_d = 250
        # Dive depth for dive profile in meters
        config.dive_depth = -50
        # Max distance travelled between current location and waypoint in meters
        config.dive_dist = 0.5

        # Is the vehicle monitoring the feature
        config.feature_monitoring = 0
        # Is the feature moving?
        config.feature_move = 0

        # Fix locations for all vehicles but 0
        config.fixed = 0
        # sim identification number
        config.no = sim_no
        # Number of repeats to perform
        config.repeats = 10
        # Max run_time for simulation run
        config.run_time = 5000

        # Random seed for starting locations, paired seeds
        config.seed = [0, 1, 2, 3, 4, 5, 7, 8, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 21, 24, 25, 27, 28, 29, 30, 31,
                       32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57]

        # 0:1 = surface ops, 1:1-3 = validation scripts
        config.sim_sub_type = 0
        # Type 0 = normal, 1 = validation
        config.sim_type = 0

        # Number of vehicles in the swarm
        config.swarm_size = i

        # TDMA frame length
        config.t_acc = 0.5
        # time delay on surface simulating time required to attain satellite fix
        config.t_sat = 180
        # timeout
        config.t_uw = 1200

        # Time step length in seconds
        config.time_step = 0.5

        # Defining the start box in which the AUVs starting positions are randomly seeded
        config.start_box_nw_lat = -2.4220
        config.start_box_nw_lon = 51.2458
        config.start_box_se_lat = -2.4219
        config.start_box_se_lon = 51.2457

        filename = '../Voronoi/3D/config/sim_config_%03i.csv' % sim_no
        write_class_attributes(config, filename)

        sim_no += 1

    gen_bash_script(sim_no)

def gen_bash_script(sim_no):
    # we want to use 8 cores concurrently, we need 8 start files...
    # no we don't because we can launch the bulk function in start.py with arguments
    sims_per_core = ceil(sim_no / 8.0)

    with open('../Voronoi/3D/run_me.sh', 'w') as bashfile:
        start_sim = 0
        while start_sim < sim_no:
            end_sim = start_sim + sims_per_core
            if end_sim > sim_no:
                end_sim = sim_no
            bashfile.write('python start.py %i %i & \n' % (start_sim, end_sim))
            start_sim = end_sim


def write_class_attributes(wr_class, filename):
    attributes = [i for i in dir(wr_class) if '__' not in i]
    attributes.remove('read_config')

    # f = open(filename, 'w', newline='')
    f = open(filename, 'w')
    wr = csv.writer(f)
    for attr in attributes:
        wr.writerow([attr, getattr(wr_class, attr)])
    f.close()


if __name__=='__main__': main_set_up()
