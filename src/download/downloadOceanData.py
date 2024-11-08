"""
This script runs a loop of motuclient command lines through a list of coordinates,
time and depth ranges via an input file (csv/xlsx).
"""
import os
import copernicusmarine as cm
from datetime import datetime
from src.utils.datasetInterface import get_data_interface


def download_data(ambient_namelist, static_paths):

    # Sea area data
    sea_area = ambient_namelist['SEA_AREA']

    # Products id
    product_id = ambient_namelist['PRODUCT_ID']

    # Input files
    input_files = static_paths['INPUT_FILES']

    # coordinates - northsea
    lon_min = ambient_namelist['LON_MIN']
    lon_max = ambient_namelist['LON_MAX']
    lat_min = ambient_namelist['LAT_MIN']
    lat_max = ambient_namelist['LAT_MAX']

    # Boundary dates
    start_date = datetime(ambient_namelist['START_YEAR'], ambient_namelist['START_MONTH'],
                          ambient_namelist['START_DAY'], ambient_namelist['START_HOUR'])
    end_date = datetime(ambient_namelist['END_YEAR'], ambient_namelist['END_MONTH'], ambient_namelist['END_DAY'],
                        ambient_namelist['END_HOUR'])

    # Create output directory if does not exist
    output_directory = os.path.join(input_files, start_date.strftime("%Y%m%d"), sea_area)

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # depth range
    depth_min = ambient_namelist['DEPTH_MIN']
    depth_max = ambient_namelist['DEPTH_MAX']

    # Product interface with the different datasets
    data_interface = get_data_interface(product_id)

    for product, datasets in data_interface.items():
        for dataset_id, variables in datasets.items():
            
            # download data
            cm.subset(
                dataset_id=dataset_id,
                #dataset_version="202012",
                variables=variables,
                minimum_longitude=lon_min,
                maximum_longitude=lon_max,
                minimum_latitude=lat_min,
                maximum_latitude=lat_max,
                start_datetime=start_date.strftime("%Y-%m-%dT%H:%M:%S"),
                end_datetime=end_date.strftime("%Y-%m-%dT%H:%M:%S"),
                minimum_depth=depth_min,
                maximum_depth=depth_max,
                output_directory=output_directory,
                force_download="true",
                overwrite_output_data="true"
                )
            
if __name__ == '__main__':
    download_data()