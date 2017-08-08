from itertools import count
import os
import csv
import numpy as np
from math import atan, degrees
from dist import dist
from find_dir import *
import getpass
import os

def get_file_number(path):
    inds = []
    for filename in os.listdir(path):
        if filename.startswith("result"):
            print(filename)
            i = filename.split('_')[1].split('.')[0]
            print(i)
            inds.append(int(i))
    if inds != []:
        return max(inds)+1
    else:
        return 0


def write_results(Flock, Evaluate, config):
    filename = 'results/sim_%03i' % config.no
    count = get_file_number(filename)
    filename = filename + '/result_%i.csv' % count
    print(filename)
    if getpass.getuser() == 'tsl1g12' and os.path.exists('/noc/users/tsl1g12'):
        f = open(filename, 'wb')
    else:
        f = open(filename, 'w', newline='')
    wr = csv.writer(f)

    headers = ['t', 'flock_dists', 'AUVs in Feature', 'No of Vor Nbours', 'dist_to_target']
    for AUV in Flock:
        headers.append('x%i' % AUV.ID)
        headers.append('y%i' % AUV.ID)
        headers.append('z%i' % AUV.ID)
        headers.append('m%i' % AUV.ID)
    wr.writerow(headers)

    temp = [[i for i in range(len(Flock[0].log.x))]]
    Evaluate.flock_dists.append(0)
    Evaluate.AUVs_in_feature.append(0)
    Evaluate.voronoi_neighbours.append(0)
    Evaluate.dists_to_target.append(0)
    temp.append(Evaluate.flock_dists)
    temp.append(Evaluate.AUVs_in_feature)
    temp.append(Evaluate.voronoi_neighbours)
    temp.append(Evaluate.dists_to_target)

    for AUV in Flock:
        temp.append(AUV.log.x)
        temp.append(AUV.log.y)
        temp.append(AUV.log.z)
        temp.append(AUV.log.measurement)

    temp = np.array(temp)
    temp = np.transpose(temp)

    for i in range(len(temp)):
        wr.writerow(temp[i])

    f.close()

def write_solo(AUV, config):
    filename = 'results/sim_%03i' % config.no + '/solo.csv'
    if getpass.getuser() == 'tsl1g12':
        f = open(filename, 'wb')
    else:
        f = open(filename, 'w', newline='')
    wr = csv.writer(f)

    headers = ['t']
    for i in range(config.swarm_size):
        headers.append('x%i' % i)
        headers.append('y%i' % i)
        headers.append('z%i' % i)
    wr.writerow(headers)
    temp = [[] for i in range(config.run_time)]
    for i in range(config.run_time):
        temp[i].append(i)
        for pos in AUV.log.loc_pos[i]:
            temp[i].append(pos[0])
            temp[i].append(pos[1])
            temp[i].append(pos[2])

    temp = np.array(temp)
    wr.writerows(temp)
    f.close()

def  write_proof(AUV, config, fn = ' '):
    if config.sim_type == 1:
        if config.sim_sub_type == 1:
            filename = 'validation/vld_dive.csv'
        elif config.sim_sub_type == 2:
                filename = 'validation/vld_yaw.csv'
        elif config.sim_sub_type == 3:
                filename = 'validation/vld_vel.csv'

    elif config.sim_type == 0:
        if fn == ' ':
            filename = 'results/sim_%03i' % config.no + '/proof.csv'
        else:
            filename = fn
    if getpass.getuser() == 'tsl1g12' and os.path.exists('/noc/users/tsl1g12'):
        f = open(filename, 'wb')
    else:
        f = open(filename, 'w', newline='')
    wr = csv.writer(f)
    headers = ['t']

    headers.append('x')
    headers.append('y')
    headers.append('z')

    headers.append('wp_x')
    headers.append('wp_y')
    headers.append('wp_z')
    headers.append('dist_to_wp')
    headers.append('t_uw')

    headers.append('v')
    headers.append('v_demand')
    headers.append('v_calc')

    headers.append('yaw')
    headers.append('yaw_demand')
    headers.append('yaw_demand_calc')
    headers.append('yaw_rate_calc')

    headers.append('pitch')
    headers.append('pitch_demand')
    headers.append('pitch_demand_calc')
    headers.append('pitch_rate_calc')

    headers.append('sat_times')

    wr.writerow(headers)

    temp = [[] for i in range(len(AUV.log.x))]
    for i in range(len(AUV.log.x)):
        # time
        temp[i].append(i)
        # position
        temp[i].append(AUV.log.x[i])
        temp[i].append(AUV.log.y[i])
        temp[i].append(AUV.log.z[i])
        # current waypoint
        temp[i].append(AUV.log.x_demand[i])
        temp[i].append(AUV.log.y_demand[i])
        temp[i].append(AUV.log.z_demand[i])
        temp[i].append(dist([AUV.log.x[i], AUV.log.y[i], AUV.log.z[i]], [AUV.log.x_demand[i], AUV.log.y_demand[i], AUV.log.z_demand[i]], 3))

        # time spent underwater
        if i != 0 and config.sim_sub_type == 1:
            if AUV.log.z_demand[i] == config.dive_depth and AUV.log.z_demand[i-1] == 0:
                    start_ind = i
            temp[i].append(i - start_ind)
        else:
            temp[i].append(0)

        # velocity
        temp[i].append(AUV.log.v[i])
        temp[i].append(AUV.log.v_demand[i])
        if i == 0:
            temp[i].append(AUV.log.v[0])
        else:
            # Calculated velocity
            temp[i].append(dist([AUV.log.x[i], AUV.log.y[i], AUV.log.z[i]], [AUV.log.x[i - 1], AUV.log.y[i - 1], AUV.log.z[i - 1]], 3) / 0.5)

        #### Yaw
        temp[i].append(AUV.log.yaw[i])
        temp[i].append(AUV.log.yaw_demand[i])
        #### Calculated yaw demand
        if AUV.log.x[i] != AUV.log.x_demand[i] or AUV.log.y[i] != AUV.log.y_demand[i]:
            temp[i].append(find_dir(AUV.log.x[i], AUV.log.y[i], AUV.log.x_demand[i], AUV.log.y_demand[i]))
        else:
            temp[i].append(temp[i][-1])

        if i == 0:
            temp[i].append(0)
        else:
            #### Calculated Yaw Rate
            if AUV.log.yaw[i-1] > 350 and AUV.log.yaw[i] < 10:
                print
                temp[i].append((AUV.log.yaw[i] - (AUV.log.yaw[i-1] - 360)) / 0.5)
            elif AUV.log.yaw[i-1] < 10 and AUV.log.yaw[i] > 350:
                temp[i].append(((AUV.log.yaw[i] - 360) - AUV.log.yaw[i-1]) / 0.5)
            else:
                temp[i].append((AUV.log.yaw[i] - AUV.log.yaw[i-1])/0.5)

        # Pitch
        temp[i].append(AUV.log.pitch[i])
        temp[i].append(AUV.log.pitch_demand[i])

        # Pitch demand calc
        dist_xy = dist([AUV.log.x[i], AUV.log.y[i]], [AUV.log.x_demand[i], AUV.log.y_demand[i]], 2)
        if dist_xy == 0 and AUV.log.z[i] == AUV.log.z_demand[i]:
            p_demand = 0
        elif dist_xy == 0 and AUV.log.z[i] != AUV.log.z_demand[i]:
            p_demand = AUV.config.max_pitch
        else:
            p_demand = degrees(atan(( AUV.log.z_demand[i] - AUV.log.z[i] ) / dist_xy))
            if abs(p_demand) > AUV.config.max_pitch:
                p_demand = (abs(p_demand) / p_demand) * AUV.config.max_pitch
        temp[i].append(-1*p_demand)
        # Pitch rate calc
        if i == 0:
            temp[i].append(0)
        else:
            # Calculated Pitch Rate
            temp[i].append((AUV.log.pitch[i] - AUV.log.pitch[i-1])/0.5)


        if i < len(AUV.log.sat_time_stamps):
            temp[i].append(AUV.log.sat_time_stamps[i])
        else:
            temp[i].append(0)

    temp = np.array(temp)

    for i in range(len(temp)):
        wr.writerow(temp[i])

    f.close()
