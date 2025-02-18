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

## Study-case

[Here](/examples/MEDSEA) you have a pre-run study-case, representing a potential deep oil spill scenario in the Mediterranean Sea.

### Mediterranean Sea
In the Adriatic Sea, right above the Otranto Strait, a potential threat for an oil spill event is the AQUILA2 ENI platform (18.327114 E ; 40.930188 N) at a depth of 800 m:
![med](/examples/MEDSEA/MED0min.png)

Let us consider a potential oil spill, starting on 1st August 1995 at 12 am. 
The near-field simulation predicts a plume phase of 40 min, reaching a depth of -580 m and a horizontal spreading of 200 m, together with a south-eastward drift:
![med](/examples/MEDSEA/run000000/PICS/traj_env_xz.png)

While rising, the oil increasingly incorporates water, increasing its density and slowing down to a neutral buoyancy level. While the oil concentration diminishes in time, the plume velocity decreases to zero:
![med](/examples/MEDSEA/run000000/PICS/oilconc_vel.png)

Due to loss of momentum, the plume corporate behavior is then lost and single oil parcels evolve independently. The second-stage of the deep spill evolution is modelled with a [Far-field simulator](https://github.com/GiuliaGronchi/FarParcels).

