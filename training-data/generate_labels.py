import numpy as np
import matplotlib.pyplot as plt

from interpolation import interpolate_path

GRID_SIZE = 3 # How many sectors into which to divide each dimension
AREA_SIZE = 5 # Unauthorised drone is assumed to move no further than AREA_SIZE from the origin in either dimension
CONTINUOUS_LABELS = False

DURATION = 1000 # Duration scene lasts for (seconds)
NUM_SAMPLES = 20000 # Number of samples acquired during this time

FNAME = "longlines_path2" # Name of path file to use and save as

flightpath = np.load(f"flightpaths/{FNAME}.npy")
interpolated_path = interpolate_path(flightpath, DURATION, NUM_SAMPLES)

if CONTINUOUS_LABELS:
    # Don't produce gride labels, instead produce single x-y labels with continuous coordinate values
    labels = np.zeros((NUM_SAMPLES,2))
    labels = interpolated_path[:,:2]
    print(labels)
else:
    grid_coords = np.floor((interpolated_path+AREA_SIZE) / (AREA_SIZE*2) * GRID_SIZE).astype(int)[:,:2]

    labels = np.zeros((NUM_SAMPLES, GRID_SIZE, GRID_SIZE))
    labels[np.arange(0,NUM_SAMPLES),grid_coords[:,0], grid_coords[:,1]] = 1

np.savez_compressed(f"data/{FNAME}_labels{'_continuous' if CONTINUOUS_LABELS else ''}.npz", labels=labels)