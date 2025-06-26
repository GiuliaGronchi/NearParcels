# Near-field: Subsurface Oil Spill Simulation

**Python-based simulation framework for modelling near-field dynamics of deep oil spills in the ocean.**

In the **near-field** region of an oil spill, oil parcels exhibit collective plume-like behavior as they rise and interact with ambient ocean stratification.  
This model (v1.0) captures the evolution of a subsurface plume driven by buoyancy, momentum, and entrainment processes.

---

## Quick Start

### 1. Pre-configure the Environment

Create a conda environment using the provided environment file:

```bash
conda env create -n uworm environment.yml
```

Activate it with:

```bash
conda activate uworm
```

---

### 2. Configure a Spill Scenario

Simulation inputs are provided via editable `.yaml` files:

- **`Release.yaml`**  
  Set the release parameters: location, start time, nozzle diameter, oil type.

- **`Ambient.yaml`**  
  Specify the ocean background data (temperature, salinity, zonal and meridional currents).  
  Data is automatically retrieved from [Copernicus Marine](https://data.marine.copernicus.eu/products).  
  _Note: A registered Copernicus Marine account is required._

- **`Render.yaml`**  
  Select output plots and figures for visualization.

---

### 3. Run the Simulation

Run the main simulation script:

```bash
python MAIN.py
```

The model will:

1. Download ambient ocean data (u, v, T, S)
2. Interpolate the data at the spill location to build depth profiles
3. Simulate plume evolution up to a **neutral-buoyancy** depth
4. Output visualizations of the plume trajectory, shape, oil concentration, and vertical velocity

---

## Model Physics

This near-field model captures the **collective dynamics** of oil parcels rising as a coherent plume.  
Processes included:

- Momentum-driven plume rise  
- Water entrainment and mixing  
- Buoyancy adjustment and deceleration  
- Transition to independent parcel behavior at neutral buoyancy  

---

## Example: Deep Spill in the Mediterranean Sea

An example study case is provided in [`examples/MEDSEA`](examples/MEDSEA), representing a hypothetical release scenario at the **AQUILA2 ENI platform** in the Otranto Strait (Adriatic Sea).

- **Location:** 40.930188°N, 18.327114°E  
- **Depth:** 800 meters  
- **Start time:** 1 August 1995, 12:00 AM

### Initial Spill Snapshot

<img src="/examples/MEDSEA/MED0min.png" alt="Initial condition" width="400"/>

---

### Plume Simulation Results

- Plume rises to a depth of approximately **-580 m**
- Horizontal spreading reaches **~200 m**
- Drift direction is **southeastward**, guided by local currents
- Duration of the plume phase: **~40 minutes**

<img src="/examples/MEDSEA/run000000/PICS/traj_env_xz.png" alt="Trajectory XZ" width="500"/>

---

### Entrainment and Concentration Dynamics

During ascent, the plume entrains water, increasing total density and slowing upward motion.  
This leads to dilution of oil concentration and a shift toward neutral buoyancy.

<img src="/examples/MEDSEA/run000000/PICS/oilconc_vel.png" alt="Oil concentration and velocity" width="500"/>

---

### Transition to Far-Field Phase

Once the plume reaches its neutral buoyancy, it disperses into independent oil parcels.  
This **post-plume phase** is simulated using the [FarParcels model](https://github.com/GiuliaGronchi/FarParcels).

---


