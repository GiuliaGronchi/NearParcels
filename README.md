# UWORM-1

UWORM-1 is a Python-based simulator for subsurface oil spills with a plume model approach.

To run UWORM-1, install a pre-configured conda virtual environment. To create the environment:

    conda env create -n uworm environment.yml

To set up an oil spill experiment, go to the namelist directory (UWORM-1/namelist), where you fill the following files: define the release parameters of your spill, such as spill location and nozzle diameter (Release.yaml), and select the ambient ocean conditions (Ambient.yaml) to be gathered from Coperinus Marine Service (make sure to have a registered account!). You can also choose some key numerical parameters in the file NumericalSimulation.yaml. Finally, you can choose the visualizations to be rendered in the namelist Render.yaml.

To launch a UWORM-1 simulation, run the MAIN.py from the UWORM-1 directory. This will do:

1 - Download the ocean data from Copernicus Marine Service
2 - Interpolate the ocean data at the spill location, obtaining vertical profiles of u,v,T,S
3 - Run the plume simulation, obtaining the time-evolution of the spill
4 - Visualize the plume variables and the ocean data

To run the 2 test cases (called respectively MEDSEA, NORTHSEA): fill the namelists with values related to the respective experiment, change the StaticPaths.yaml with the chosen experiment folder, run the MAIN.py. This will create a data folder and a product folder for the selected experiment.



UWORM-1 was developed at the Euro-Mediterranean Center on Climate Change Foundation (CMCC) in Lecce, Italy

Giulia Gronchi, Nadia Pinardi,
Megi Hoxhaj, Yordany Morejon Loyola, Mario Salinas, Igor Atake
