from Config_class import *
import csv

def main_set_up():
    config = sim_config('../Voronoi/3D/config/sim_config_DO_NOT_DELETE.csv')
    swarm_size_range = (5, 31)
    sim_no = 0

    for i in range(swarm_size_range[0], swarm_size_range[1]):
        config.no = sim_no
        config.repeats = 50
        config.run_time = 6000
        config.swarm_size = i
        config.random_seed = np.random.randint(100)

        filename = '../Voronoi/3D/config/sim_config_%03i.csv' % sim_no
        write_class_attributes(config)

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