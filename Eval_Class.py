import sys
sys.path.insert(0, "/noc/users/tsl1g12/gen")
sys.path.insert(0, 'C:/users/tsl1g12/desktop/phd_sim/gen')
sys.path.insert(0, 'D:/Desktop/PhD_sim/PhD_sim/gen')
import numpy as np
from scipy.spatial import Voronoi, voronoi_plot_2d
from dist import dist
from numba import jitclass

class Evaluator:

    def evaluate(self, Flock, elps_time):
        self.collisions(Flock, elps_time)
        self.flock_dist(Flock)
        self.AUV_in_feature(Flock)
        self.dist_to_target(Flock)

    # Number of collisions between vehicles, collision defined as closer than 0.5m
    def collisions(self, Flock, elps_time):
        collisions = []

        for AUV in Flock:
            collision = np.where(AUV.loc_dist < 0.5)[0]
            for i in collision:
                if [i, AUV.ID, elps_time] not in collisions:
                    collisions += [[AUV.ID, i, elps_time] for i in collision if [i, AUV.ID, elps_time] not in collisions]

        self.no_of_colls.append(len(collisions))

    # Average distance to voronoi neighbours & Number of voronoi neighbours
    def flock_dist(self, Flock):
        n_regs = []
        loc_dists = []
        for AUV in Flock:
            n_reg = []

            loc_vehicles = np.append(AUV.loc_pos[np.where(AUV.loc_vehicles == 1)[0]][:, 0:2], np.reshape([AUV.x, AUV.y],(1,2)), axis = 0 )
            v_region = Voronoi(loc_vehicles, qhull_options='Qbb Qc Qx')

            ind = np.where(loc_vehicles == [AUV.x, AUV.y])[0][0]
            # Find AUVs Region
            reg_ind = v_region.point_region[ind]
            # Find vertices of AUVs region
            vert_ind = v_region.regions[reg_ind]
            # Which regions are joined by these vertices
            for reg in v_region.regions:
                check = []
                for vert in reg:
                    # if a region has a vertex -1 it means it is an external region
                    # Before excluding this it would think all external regions were neighbours because they all had the vertex -1
                    if vert != -1:
                        if vert in vert_ind:
                            check.append(1)
                        else:
                            check.append(0)
                    else:
                        check.append(0)
                # check must include at least 1 0, if check is all 1s it uses all the same vertices as the current region i.e. it is the current region
                if 0 in check and 1 in check:
                    n_reg.append(v_region.regions.index(reg))

            # voronoi_plot_2d(v_region)
            # plt.scatter(np.array(loc_vehicles)[:,0], np.array(loc_vehicles)[:,1])
            # plt.scatter(AUV.x, AUV.y, facecolor = 'r', marker = 'x', linewidth = 10)
            # for n in n_reg:
            #     plt.plot([AUV.x, loc_vehicles[np.where(v_region.point_region==n)[0][0]][0]], [AUV.y, loc_vehicles[np.where(v_region.point_region==n)[0][0]][1]])
            # plt.show()

            # Take the mean of the distances to vehicles in neighbouring regions
            dists = [dist([AUV.x, AUV.y], loc_vehicles[np.where(v_region.point_region == n)[0][0]], 2) for n in n_reg]

            if 0 in dists:
                dists.remove(0)
            loc_dists.append(np.mean(dists))
            # Builds a list of the number of voronoi neighbours for each vehicle in the flock
            n_regs.append(len(n_reg))
        self.flock_dists.append(np.median(loc_dists))
        self.voronoi_neighbours.append(np.mean(n_regs))

    # How many AUVs are in the feature - idea of how well feature tracking is working
    def AUV_in_feature(self, Flock):
        count = 0
        for AUV in Flock:
            if AUV.measurement != 0:
                count = count + 1
        self.AUVs_in_feature.append(count)

    # Average distance to next waypoint
    def dist_to_target(self, Flock):
        dists = []
        for AUV in Flock:
            dists.append(dist([AUV.x, AUV.y, AUV.z], AUV.waypoints[0], 3))
        self.dists_to_target.append(np.mean(dists))

    def settling_time(self, config):
        mask = np.where(self.flock_dists < config.desired_d * 1.05 and self.flock_dists > config.desired_d * 0.95)
        print(mask)
        settle_t = 0
        for i in range(2, mask[0].shape[0]):
            if mask[i] == 1 and mask[i-1] == 0:
                settle_t = i

        print(settle_t)


    def __init__(self):
        self.flock_dists = []
        self.voronoi_neighbours = []
        self.dists_to_target = []
        self.no_of_colls = []
        self.AUVs_in_feature = []