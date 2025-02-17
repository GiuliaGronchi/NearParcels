## Near-field oil model

In the near-field of the release, polluting parcels behave collectively as a plume in the surrounding ocean.

UWORM (UnderWater Oil Release Model) version 1.0 is a Python-based simulator for subsurface oil spills with a plume model approach.

### Pre-configuration
To run the model, create a pre-configured conda environment:

    conda env create -n uworm environment.yml
    
### Set up a spill scenario
To set up a new oil spill scenario, fill the relevant fields in the UWORM-1/namelist files .yaml

- Define the spill **release**, such as spill location and nozzle diameter within Release.yaml
- Select the **ambient** ocean data (temperature, salinity, zonal and meridional currents) within Ambient.yaml
  
The ocean data will be automatically collected and downloaded from [Copernicus Marine Data Store](https://data.marine.copernicus.eu/products) (make sure to have a registered account!)

Decide which visuals and plots you want to see in Render.yaml.

### Run a spill simulation

Run a near-field simulation:

    python MAIN.py 
    
This will do:

1. Download the ocean data (u zonal current, v meridional current, T temperature, S salinity)

2. Interpolate horizontally the ocean data on the spill location, obtaining depth-profiles of u,v,T,S

3. Run the plume evolution

4. Obtain the model output and visualize the plume trajectory, shape evolution, oil concentration, velocity

The near-field simulation will run, depending on the oil and ambient conditions, up to a **neutral-buoyancy** depth.

## Study-cases

I prepared two show cases, in the Mediterranean Sea and in the North Sea. You can run these two experiment on your own to become familiar with the model.






