"""
@author: msalinas
@email: mario.salinas@cmcc.it

Set of functions to manage experiment saving
"""

import os
import json
import numpy as np
import pandas as pd

from src.utils.logging import copy_namelists
from src.utils.utils import dict_to_lists, get_ntime, print_ntime


def create_exp_dir_and_log_namelist(prod_path):
    """
    Function that:
        1. looks for the next experiment name available in `prod_path`directory, in increasing order.
            The format is: <prod_path>/runXXXX/

        2. creates the all the output folders

        3. logs all the input namelists

        4. returns the newly created experiment output directory and runId (runXXXX)
    """
    os.makedirs(prod_path, exist_ok=True)

    runId = str(len([filen for filen in os.listdir(prod_path) if 'run' in filen])).zfill(6)

    exp_dir = f'{prod_path}/run{runId}/'

    if os.path.exists(exp_dir):
        err_msg = f'[ERROR] folder {exp_dir} already exists. Exit to prevent overwrite.'
        print_ntime(err_msg)
        raise Exception(err_msg)

    os.makedirs(exp_dir, exist_ok=True)
    os.makedirs(os.path.join(exp_dir, 'LOG'))
    os.makedirs(os.path.join(exp_dir, 'PICS'))

    # Copy the namelists in the experiment folder
    copy_namelists(exp_dir)

    return exp_dir, runId


def compute_metrics(exp_dir, numerical_namelist, release_namelist):
    """
    Compute metrics from input namelists and output csvs,
    and returns:
        - metrics:        list containing the metrics values
        - metrics_name:   list containing the metrics names
    """

    metrics, metrics_name = [], []

    z0 = release_namelist.z0
    b0 = release_namelist.b0
    w0 = release_namelist.w0
    dt = numerical_namelist.dt
    oil_volume0 = np.pi * b0 **2 * w0 * dt
    tmax = int(numerical_namelist.time_max*60/dt)
    oil_volume = round(oil_volume0*tmax)

    # compute metrics here
    # final_depth = ...

    # read csv
    # fname = 'oceanProfilesInput.csv'
    # opdf = pd.read_csv(exp_dir+fname, sep=',')
    # fname = 'parameters.csv'
    # pmdf = pd.read_csv(exp_dir+fname, sep='\t')
    # fname = 'plumeState.csv'
    # psdf = pd.read_csv(exp_dir+fname, sep='\t')

    # add metrics to output lists
    # metrics      += [metric1, ...]
    # metrics_name += ['metric1', ...]
    metrics      += [oil_volume0, tmax, oil_volume]
    metrics_name += ['oil_volume0', 'tmax', 'oil_volume']





    return metrics, metrics_name


def compute_and_save_product_summary(exp_dir, runId, numerical_namelist, release_namelist, ambient_namelist):
    """
    Function that computes and writes on disk the summary json file
    """
    runDate = get_ntime()
    # read parameters from namelists
    namelist_cols, namelist_vals = ['runId', 'runDate'], [runId, runDate]
    for namelist, namelist_str in zip(
                        [numerical_namelist, release_namelist, ambient_namelist],
                        ['numerical_', 'release_', 'ambient_']):
        tmpc, tmpv = dict_to_lists(namelist, prefix=namelist_str)
        namelist_cols += tmpc
        namelist_vals += tmpv

    # compute metrics
    metrics_vals, metrics_cols = compute_metrics(exp_dir, numerical_namelist, release_namelist)

    out_cols = namelist_cols+metrics_cols
    out_vals = namelist_vals+metrics_vals

    # write summary as json
    opath = exp_dir+'/summary.json'
    with open(opath, 'w') as fout:
        json.dump(dict(zip(out_cols, out_vals)), fout)
        print_ntime(f'Summary file saved in {opath}')


def merge_product_summary(prod_path, save_df=False):
    """
    Function that:
        1. searches for runXXXXX folders inside the provided `prod_path`
        2. merges all summary.json files inside those folders
        3. returns a pandas dataframe containing all the runs

    `prod_path` can be the default product path,
    or any directory that contains runXXXXX folders with summary.json inside.
    """

    if not os.path.exists(prod_path):
        print_ntime(f"[ERROR] The provided product directory doesn't exist.\n\tProvided folder:\n\t{prod_path}")
        return None

    exp_dir_list = sorted([edir for edir in os.listdir(prod_path) if 'run' in edir])

    summary_list = []
    summary_df = pd.DataFrame()

    for edir in exp_dir_list:
        try:
            fpath = f'{prod_path}/{edir}/summary.json'
            with open(fpath, 'r') as fin:
                # load summary
                esumm = json.load(fin)
                summary_list.append(esumm)
        except Exception as e:
            print_ntime(f'[ERROR] reading {fpath}:\n{str(e)}')

    nruns = len(summary_list)

    if nruns>0:
        summary_df = pd.DataFrame(summary_list)
        print_ntime(f'{nruns} run(s) loaded.')
        if save_df:
            today_str = get_ntime(fmt='%Y%m%dT%H%M%SZ')
            opath = f'{prod_path}/summary_list_{today_str}.csv'
            summary_df.to_csv(opath, index=False)
            print_ntime(f'csv saved in {opath}')
    else:
        print_ntime(f'No runs to load from {prod_path}.')
    
    
    return summary_df