import copernicusmarine as cm
from src.download.downloadOceanData import download_data
from src.preproc.interpolateOceanData import interpolate_data
from src.plume import plume
from src.render.plotPlume import plot
from src.render.plotOceanData import plot_ocean
from src.utils.output_db import create_exp_dir_and_log_namelist, merge_product_summary
from src.utils.readNamelist import read_simulation_namelists
from src.utils.utils import print_ntime
import shutil
import os

UWORM1_ROOT = '.'

DO_DOWNLOAD = False
DO_PLUME = False
DO_PLOT = False
DO_MERGE = False

# De-comment what you want to run from the flag list below
DO_DOWNLOAD = True
DO_PLUME = True
DO_PLOT = True
#DO_MERGE = True


if __name__ == '__main__':
    print_ntime('Starting...')

    # login (By default, the configuration credential file is saved in your home directory)
    #cm.login()

    # Read namelist, constants, and static paths
    ambient_namelist, numerical_namelist, release_namelist, \
    render_namelist, constants, static_paths = read_simulation_namelists(UWORM1_ROOT=UWORM1_ROOT)
    prod_path = static_paths['EXP_PROD']
  


    # Download the ocean data from Copernicus Marine Service, which will serve as boundary condition to the oil spill motion
    if DO_DOWNLOAD:
        print_ntime('Downloading data...')
        download_data(ambient_namelist, static_paths)
        print_ntime('Done downloading data.')

    # Interpolate and run the plume simulation
    if DO_PLUME:
        # init output folder
        exp_dir, runId = create_exp_dir_and_log_namelist(prod_path)

        # Interpolate the ocean data at the spill location, obtaining vertical profiles of u,v,T,S,rhoa
        print_ntime('Interpolating...')
        interpolate_data(exp_dir, ambient_namelist, release_namelist, static_paths)
        print_ntime('Done interpolating.')

        # Run the plume simulation, obtaining the time-evolution of the spill
        print_ntime('Running the plume simulation...')
        plume(exp_dir, runId, ambient_namelist, numerical_namelist, release_namelist, constants)
        print_ntime('Plume simulation done.')

        # Visualize the plume variables and the ocean data
        if DO_PLOT:
            print_ntime('Plotting...')
            plot(exp_dir, render_namelist, ambient_namelist)
            plot_ocean(exp_dir, ambient_namelist)
            print_ntime('Done plotting.')

    # merge all summary in one csv
    if DO_MERGE:
        print_ntime('Merging summary.json files...')
        merge_product_summary(prod_path, save_df=True)
        print_ntime('Done merging summary.json files.')

    print_ntime('Done.')
