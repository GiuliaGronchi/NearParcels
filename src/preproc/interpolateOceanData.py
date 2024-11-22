#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 15 14:35:14 2023

@author: ggronchi
"""
from glob import glob
import xarray as xr
import numpy as np
import pandas as pd
from datetime import datetime
import gsw
import os

cur_mag=1

def interp_oceanvar(ds, var, lat_fix, lon_fix):
    time_fix = ds['time'][0]
    offset = 1.0

    crop_var = ds[var].sel(time=time_fix).sel(latitude=slice(lat_fix - offset, lat_fix + offset), longitude=slice(lon_fix - offset, lon_fix + offset))
    var_depth = crop_var.interp(latitude=lat_fix, longitude=lon_fix).values

    return var_depth

def interpolate_data(exp_dir, ambient_namelist, release_namelist, static_paths):
    # Read downloaded ocean data
    date = datetime(ambient_namelist["START_YEAR"], ambient_namelist["START_MONTH"], ambient_namelist["START_DAY"], ambient_namelist["START_HOUR"]).strftime("%Y%m%d")
        
    # List of variables
    var_list = ['uo-vo', 'thetao', 'so']

    # Read depths from so data
    file0 = glob(os.path.join(static_paths['INPUT_FILES'], date, ambient_namelist['SEA_AREA'], '*so*.nc'))
    ds = xr.open_dataset(file0[0])
    depth = ds['depth'].values
    df = pd.DataFrame({'depth': -depth})

    # Retrieve spill location
    lat_fix = release_namelist['spill_lat']
    lon_fix = release_namelist['spill_lon']
    # print('release coords', lat_fix, lon_fix)

    # Iterate through the list of variables
    for var in var_list:
        file = glob(os.path.join(static_paths['INPUT_FILES'], date, ambient_namelist['SEA_AREA'], '*' + var + '*.nc'))
        print(file[0])
        ds = xr.open_dataset(file[0])

        if var == 'uo-vo':
            var_depth_uo = interp_oceanvar(ds, 'uo', lat_fix, lon_fix)
            df['uo'] = var_depth_uo * cur_mag
            var_depth_vo = interp_oceanvar(ds, 'vo', lat_fix, lon_fix)
            df['vo'] = var_depth_vo * cur_mag
        else:
            var_depth = interp_oceanvar(ds, var, lat_fix, lon_fix)
            df[var] = var_depth

    # Calculate density using the seawater library
    df['rhoa'] = gsw.density.rho(df['so'], df['thetao'],1)


    # Drop NaN values and save to CSV
    first_nan_idx = df[df.isna().any(axis=1)].index[0]
    last_valid_row = df.iloc[first_nan_idx - 1].copy()
    df.iloc[first_nan_idx, 1:] = last_valid_row[1:]
    oceanfile = df.iloc[:first_nan_idx + 1]
    oceanfile.to_csv(os.path.join(exp_dir, 'oceanProfilesInput.csv'), index=False, header=True, float_format='%.8f', mode='w')


    oceanfile=pd.DataFrame(df.dropna())
    oceanfile.to_csv('{}oceanProfilesInput.csv'.format((os.path.join(exp_dir + '/'))), index=False, header=True, float_format='%.8f', mode='w')





if __name__ == '__main__':
    interpolate_data()

