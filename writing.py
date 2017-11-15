from itertools import count
import os
import csv
import numpy as np
from math import atan, degrees
import getpass
import os
import pandas as pd
from latlon_util import find_dist2, find_dist3, find_dir

def get_file_number(path):
    inds = []
    for filename in os.listdir(path):
        if filename.endswith(".sbd"):
            print(filename)
            i = filename.split('_')[1].split('.')[0]
            print(i)
            inds.append(int(i))
    if inds != []:
        return max(inds)+1
    else:
        return 0

def write_results(Flock, Evaluate, config, repeat):
    filename = 'results/sim_%03i' % config.no
    filename = filename + '/result_%i.csv' % repeat
    print(filename)

    dfresults = {'t':[i for i in range(config.run_time)],
                              'flock_dists':Evaluate.flock_dists,
                              'AUVs in Feature':Evaluate.AUVs_in_feature,
                              'vor_neighbours':Evaluate.voronoi_neighbours,
                              'dist_to_target':Evaluate.dists_to_target}

    for AUV in Flock:
        dfresults.update({'lon%i' % AUV.ID:AUV.log.lon[0:-1]})
        dfresults.update({'lat%i' % AUV.ID:AUV.log.lat[0:-1]})
        dfresults.update({'z%i' % AUV.ID:AUV.log.z[0:-1]})
        dfresults.update({'m%i' % AUV.ID:AUV.log.measurement[0:-1]})

    pd.DataFrame(dfresults).to_csv(filename)

def write_vehicle_perspective(AUV, config, repeat):
    df = {}
    loc_pos = np.array(AUV.log.loc_pos)
    for i in range(config.swarm_size):
        df.update({'lat%i' % i:loc_pos[:,i][:,1]})
        df.update({'lon%i' % i:loc_pos[:,i][:,0]})
        df.update({'z%i' % i:loc_pos[:,i][:,2]})
    pd.DataFrame(df).to_csv('results/sim_%03i/svp_%03i.csv' % (config.no, repeat))

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
            filename = 'results/sim_%03i' % config.no + '/proof_%i.csv' % AUV.ID
        else:
            filename = fn

    dfresults = {'t':[i for i in range(len(AUV.log.lat))],
                 'lat':AUV.log.lat,
                 'lon':AUV.log.lon,
                 'z':AUV.log.z,
                 'lat_demand':AUV.log.lat_demand,
                 'lon_demand':AUV.log.lon_demand,
                 'z_demand':AUV.log.z_demand,
                 'state':AUV.log.state,
                 'time_uw':AUV.log.time_uw,
                 'v':AUV.log.v,
                 'v_demand':AUV.log.v_demand,
                 'yaw':AUV.log.yaw,
                 'yaw_demand':AUV.log.yaw_demand,
                 'pitch':AUV.log.pitch,
                 'pitch_demand':AUV.log.pitch_demand,
                 'sat_times':AUV.log.sat_time_stamps + [0 for i in range(len(AUV.log.lat) - len(AUV.log.sat_time_stamps))]}

    dist_to_wp, v_calc, yr_calc, yd_calc, pd_calc, pr_calc = np.zeros((6, len(AUV.log.lat)))

    for i in range(len(AUV.log.lon)):
        dist_to_wp[i] = find_dist3((AUV.log.lon[i], AUV.log.lat[i], AUV.log.z[i]), (AUV.log.lon_demand[i], AUV.log.lat_demand[i], AUV.log.z_demand[i]))

        if i ==0:
            v_calc[i] = 0
            yr_calc[i] = 0
            pr_calc[i] = 0
        else:
            v_calc[i] = find_dist3((AUV.log.lon[i], AUV.log.lat[i], AUV.log.z[i]), (AUV.log.lon[i - 1], AUV.log.lat[i - 1], AUV.log.z[i - 1])) / config.time_step

            #### Calculated Yaw Rate
            if AUV.log.yaw[i-1] > 350 and AUV.log.yaw[i] < 10:
                yr_calc[i] = (AUV.log.yaw[i] - (AUV.log.yaw[i-1] - 360)) / config.run_time
            elif AUV.log.yaw[i-1] < 10 and AUV.log.yaw[i] > 350:
                yr_calc[i] = ((AUV.log.yaw[i] - 360) - AUV.log.yaw[i-1]) /  config.run_time
            else:
                yr_calc[i] = (AUV.log.yaw[i] - AUV.log.yaw[i-1])/ config.run_time

            # Calculated Pitch Rate
            pr_calc[i] = (AUV.log.pitch[i] - AUV.log.pitch[i-1])/ config.run_time

        # if AUV.log.lon[i] != AUV.log.lon_demand[i] or AUV.log.lat[i] != AUV.log.lat_demand[i]:
        yd_calc[i] = find_dir((AUV.log.lon[i], AUV.log.lat[i]), (AUV.log.lon_demand[i], AUV.log.lat_demand[i]))
        # else:
            # yd_calc.append(temp[i][-1])


        # # Pitch demand calc
        # dist_xy = find_dist2((AUV.log.lon[i], AUV.log.lat[i]), (AUV.log.lon_demand[i], AUV.log.lat_demand[i]))
        # # if dist_xy == 0 and AUV.log.z[i] == AUV.log.z_demand[i]:
        # #     pd_calc[i] = 0
        # if dist_xy == 0 and AUV.log.z[i] != AUV.log.z_demand[i]:
        #     pd_calc[i] = AUV.config.max_pitch
        # else:
        #     pd_calc[i] = degrees(atan((AUV.log.z_demand[i] - AUV.log.z[i]) / dist_xy))
        #     if abs(pd_calc[i]) > AUV.config.max_pitch:
        #         pd_calc[i] = (abs(pd_calc[i]) / pd_calc[i]) * AUV.config.max_pitch
        # pd_calc[i] = -1*pd_calc[i]

    # dfresults.update({'pitch_demand_calc':pd_calc})
    dfresults.update({'pitch_rate_calc': pr_calc})
    dfresults.update({'dist_to_wp': dist_to_wp})
    dfresults.update({'yaw_demand_calc': yd_calc})
    dfresults.update({'yaw_rate_calc': yr_calc})
    dfresults.update({'v_calc': v_calc})
    ### For checking lengths of all keys if making the data frame errors due to array length
    # print([len(v) for v in dfresults.values()])

    pd.DataFrame(dfresults).to_csv(filename)

