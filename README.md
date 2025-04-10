# Near-field 

In the near-field region of an oil spill, oil parcels behave collectively, expanding like a plume in the surrounding ocean.

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

# Study-case

[Here](/examples/MEDSEA) you have all the data and code for a pre-run study-case, representing a potential deep oil spill scenario in the Mediterranean Sea.

In the Otranto Strait in the Adriatic Sea, a potential threat for an oil spill event is 

- AQUILA2 ENI platform (18.327114 E ; 40.930188 N) at a depth of about 800 m. 

The spill starts on 1st August 1995 at 12 am. 

<img src="/examples/MEDSEA/MED0min.png" width="600">


The near-field simulation is run and predicts a plume phase output:

- reaching buoyant depth of -580 m with total lateral spreading of approximately 200 m
  
- with a south-eastward currents drift
  
- total approximate duration 40 min

<img src="/examples/MEDSEA/run000000/PICS/traj_env_xz.png" width="600">

Key: The rising plume incorporates water, increasing density and decelerating up to a neutral buoyancy depth below the surface. 

Together with loss of momentum, oil concentration inside the plume decreases in favour of water concentration:


<img src="/examples/MEDSEA/run000000/PICS/oilconc_vel.png" width="600">

After this moment, the plume collective behavior is lost and oil parcels start to move independently. 
The second-stage of the deep spill evolution is modelled [here](https://github.com/GiuliaGronchi/FarParcels).

