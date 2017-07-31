import numpy as np
import pandas as pd
from matplotlib import *
import matplotlib.pyplot as plt
import os
from Config_class import *
from math import ceil, floor

def import_data(filename):
    dfspec = pd.read_csv(filename, nrows = 1)
    dfresults = pd.read_csv(filename, header = 2 )
    return dfspec, dfresults

def import_all_data():
    dfs = []
    for i in range(1000):
        filename = 'results/result_%03i.csv' % i
        if os.path.isfile(filename):
            dfs.append(pd.DataFrame.from_csv(filename, header = 2))
    return dfs

def bin_data(data, bins):
    slices = [data[int(0+(i*ceil(len(data)/bins))):int(floor(len(data)/bins)+(i*floor(len(data)/bins)))] for i in range(bins)]
    binned_data = [np.mean(i) for i in slices]
    time = range(len(data))[0::len(data)/bins]
    return time, binned_data

def plot_flock_dists(fn, repeat_no):
    fig = plt.figure(figsize=(9,3))
    lines = ['-','--',':','-.']
    config = sim_config(fn + 'config/sim_config.csv')
    df = pd.read_csv(fn + 'result_%i.csv' % repeat_no)
    plt.plot(df.index.tolist()[0:-1], df.flock_dists.tolist()[0:-1], '-')
    plt.plot(df.index.tolist()[0:-1], abs(config.desired_d - np.array(df.flock_dists.tolist()[0:-1])), 'r--')
    lgnd = ['Average Separation / m', 'Absolute Error / m']
    plt.ylabel('Distance / m')
    plt.ylim([0, config.desired_d *1.1])
    plt.xlim([0, config.run_time])
    plt.xlabel('Time')
    if lgnd != 0:
        plt.legend(lgnd)
    # subplots_adjust(bottom=0.14)
    fig.tight_layout()
    fig.savefig(fn + 'figs/sep_dists.png', dpi=300)
    plt.close(fig)

def approximate_feature(dfspec, dfresults, swarm_size):
    x = [df['x%i'] for i in range(len(swarm_size))]

def plot_depths(df):
    z = df['z0'].tolist()
    t = range(len(z))
    plt.plot(t,z)
    plt.show()

def proofs(sim_no):
    fn ='results/sim_%03i' % sim_no + '/'
    config = sim_config(fn + 'config/sim_config.csv')
    dfresults = pd.read_csv(fn + 'proof.csv')
    plot_depth_proof(dfresults, config, save = True)

def plot_depth_proof(dfresults, config, save = False):
    f, ax = plt.subplots(3,1, sharex = True)

    ax[0].plot(dfresults['t'].tolist(), dfresults['dist_to_wp'].tolist())
    ax[0].plot([0,5000], [5,5], 'r--')
    ax[0].set_ylabel('Distance / m')
    ax[0].legend(['Distance to Waypoint', '5m Acceptence Radius'], loc = 4)
        # , prop={'size': 6}, bbox_to_anchor=(.5, 1.02, 0.5, .102), loc=3, ncol=2, mode="expand", borderaxespad=0.)

    ax[1].plot(dfresults['t'].tolist(), dfresults['t_uw'].tolist())
    ax[1].plot([0, 5000], [config.t_uw*0.5, config.t_uw*0.5], 'k--')
    ax[1].plot([0,5000], [config.t_uw,config.t_uw], 'r--')
    ax[1].set_ylabel('Time')
    ax[1].legend(['Time underwater','Start Surfacing', 'Surface Immediately'], loc = 4)

    ax[2].plot(dfresults['t'].tolist(), dfresults['z'].tolist(), 'r')
    ax[2].plot(dfresults['t'].tolist(), dfresults['wp_z'].tolist(), 'k--')
    sat_times = [t for t in dfresults['sat_times'].tolist() if t != 0]
    ax[2].plot(sat_times, [0 for i in range(len(sat_times))],  'ro')
    ax[2].set_ylabel('Depth')
    ax[2].legend(['Depth','Depth Demand', 'Sat Comm Event'], loc = 4)
    ax[2].set_xlabel('Time')

    ax[0].set_xlim([0,config.run_time])
    ax[1].set_xlim([0,config.run_time])
    ax[2].set_xlim([0,config.run_time])

    f.tight_layout()

    if save == True:
        f.savefig(fn + 'figs/depth.png', dpi=300)
    else:
        plt.show()

def plot_vel_proofs(dfresults, config, save=False):
    f = plt.figure(figsize=(9, 3))
    plt.plot(dfresults['t'].tolist(), dfresults['v'].tolist())
    plt.plot(dfresults['t'].tolist(), dfresults['v_demand'].tolist(), 'k.')
    plt.plot(dfresults['t'].tolist(), dfresults['v_calc'].tolist(), 'r--')
    plt.xlabel('Time')
    plt.ylabel('Speed / m/s')
    plt.legend(['AUV log v', 'v demand', 'Calculated v'], prop={'size':6}, bbox_to_anchor=(.5, 1.02, 0.5, .102), loc=3,
        ncol=3, mode="expand", borderaxespad=0.)
    plt.ylim([0,1])
    plt.tight_layout()
    if save == True:
        plt.savefig(fn + 'figs/speeds.png')
    else:
        plt.show()

    ################################## YAW PLOTS ###########################################

def plot_yaw_proofs(dfresults, config, save = False):
    f, ax = plt.subplots(3, sharex = True)
    ax[0].plot(dfresults['t'].tolist(), dfresults['yaw'].tolist(), 'k-')
    ax[0].plot(dfresults['t'].tolist(), dfresults['yaw_demand'].tolist(), 'r-')
    ax[0].set_ylabel('Yaw / degs')
    ax[0].legend(['Yaw', 'Yaw demand'], prop={'size':6}, bbox_to_anchor=(.5, 1.02, 0.5, .102), loc=3,
           ncol=2, mode="expand", borderaxespad=0.)


    ax[1].plot(dfresults['t'].tolist(), dfresults['yaw_demand'].tolist(), 'k-')
    ax[1].plot(dfresults['t'].tolist(), dfresults['yaw_demand_calc'].tolist(), 'r+')
    ax[1].set_ylabel('Yaw Demand / degs')
    ax[1].legend(['Yaw demand', 'Calculated Yaw demand'], prop={'size': 6}, bbox_to_anchor=(.5, 1.02, 0.5, .102), loc=3,
                 ncol=2, mode="expand", borderaxespad=0.)

    ax[2].plot(dfresults['t'].tolist(), dfresults['yaw_rate_calc'].tolist())
    ax[2].set_xlabel('Time')
    ax[2].set_ylim([-20,20])
    ax[2].set_ylabel('Yaw Rate / deg/s')
    f.tight_layout()

    if save == True:
        f.savefig(fn + 'figs/yaw.png')
    else:
        plt.show()