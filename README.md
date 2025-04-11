# Near-field 

In the near-field region of an oil spill, oil parcels behave collectively, expanding like a plume in the surrounding ocean.
The near-field version 1.0 is a Python-based simulator for subsurface oil spills with a plume model approach.

### Pre-configuration
Create a pre-configured conda environment:

    conda env create -n uworm environment.yml
    
### Set up a spill 
To set up a new oil spill scenario, fill the relevant fields in the namelist files _.yaml_

- Fill up the spill **release**, spill location and nozzle diameter values in _Release.yaml_
- Choose the time-relevant **ambient ocean** data (temperature, salinity, zonal and meridional currents) in _Ambient.yaml_. It will automatically be collected and downloaded from [Copernicus Marine](https://data.marine.copernicus.eu/products) (make sure to have a registered account!)

- Choose visuals and plots in _Render.yaml_

### Run oil transport simulation 

Run a near-field simulation:

    python MAIN.py 
    
This will do:

1. Download the ocean data (u zonal current, v meridional current, T temperature, S salinity)

2. Interpolate horizontally the ocean data on the spill location, obtaining depth-profiles of u,v,T,S

3. Run the plume evolution

4. Obtain the model output and visualize the plume trajectory, shape evolution, oil concentration, velocity

Depending on the oil and ambient condition, the near-field simulation is run up to a **neutral-buoyancy** depth.

# Study-case

[Here](/examples/MEDSEA) you have all the data and code for a pre-run study-case, representing a potential deep oil spill scenario in the Mediterranean Sea.

In the Otranto Strait in the Adriatic Sea, a potential threat for an oil spill event is 

- AQUILA2 ENI platform (18.327114 E ; 40.930188 N) at a depth of about 800 m. 

The spill starts on 1st August 1995 at 12 am. 

<center>
<img src="/examples/MEDSEA/MED0min.png" width="500" class="center">
</center>

The near-field simulation is run and predicts a plume phase output:

- reaching buoyant depth of -580 m with total lateral spreading of approximately 200 m
  
- with a south-eastward currents drift
  
- total approximate duration 40 min

<center>
<img src="/examples/MEDSEA/run000000/PICS/traj_env_xz.png" width="600">
</center>

Key: The rising plume incorporates water, increasing density and decelerating up to a neutral buoyancy depth below the surface. 

Together with loss of momentum, oil concentration inside the plume decreases in favour of water concentration:

<center>
<img src="/examples/MEDSEA/run000000/PICS/oilconc_vel.png" width="600" class="center">
</center>

After this moment, the plume collective behavior is lost and oil parcels start to move independently. 
The second-stage of the deep spill evolution is modelled [here](https://github.com/GiuliaGronchi/FarParcels).

