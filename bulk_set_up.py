from Config_class import *
import csv

config = sim_config('../Voronoi/3D/config/sim_config_DO_NOT_DELETE.csv')
attributes = [i for i in dir(config) if '__' not in i]
attributes.remove('read_config')
swarm_size_range = (5, 31)
sim_no = 0

for i in range(swarm_size_range[0], swarm_size_range[1]):
    config.no = sim_no
    config.repeats = 50
    config.run_time = 6000
    config.swarm_size = i
    filename = '../Voronoi/3D/config/sim_config_%03i.csv' % sim_no

    f = open(filename, 'w', newline='')
    for attr in attributes:
        wr = csv.writer(f)
        wr.writerow([attr, getattr(config, attr)])
    f.close()

    sim_no += 1
