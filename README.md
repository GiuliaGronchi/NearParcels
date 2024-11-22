# UWORM-1

UWORM-1 is a Python-based simulator for subsurface oil spills with a plume model approach.

To run UWORM-1, install a pre-configured conda virtual environment. To create the environment:

    conda env create -n uworm environment.yml

To set up an oil spill experiment, go to the namelist directory (UWORM-1/namelist). Here, fill the namelists yaml files. 

Define the spill release parameters (i.e. the initial condition), such as spill location and nozzle diameter within the namelist file Release.yaml. 

Then, select the spill location and the relative ambient ocean data (temperature, salinity, zonal and meridional currents) within the namelist file Ambient.yaml. The ocean data is gathered and downloaded from the Coperinus Marine Service (make sure to have a registered account!). 

Some other relevant numerical parameters can be tuned in the file NumericalSimulation.yaml. 

Finally, choose the visualizations to be rendered in the namelist file Render.yaml.

To launch a UWORM-1 simulation, run the MAIN.py from the UWORM-1 directory.

    python MAIN.py

Inside the MAIN.py, you can decide which ones of the following actions to be undertaken. Of course, the first time an experiment is launched, you should run them all :

1 - Download the ocean data from Copernicus Marine Service

2 - Interpolate the ocean data at the spill location, obtaining vertical profiles of u,v,T,S

3 - Run the plume simulation, obtaining the time-evolution of the spill

4 - Visualize the plume variables and the ocean data

To run the 2 test cases (called respectively MEDSEA, NORTHSEA): fill the namelists with values related to the respective experiment, change the StaticPaths.yaml with the chosen experiment folder, run the MAIN.py. This will create a data folder and a product folder for the selected experiment.



UWORM-1 was developed at the Euro-Mediterranean Center on Climate Change Foundation (CMCC) in Lecce, Italy

Giulia Gronchi, Nadia Pinardi,
Megi Hoxhaj, Yordany Morejon Loyola, Mario Salinas, Igor Atake
