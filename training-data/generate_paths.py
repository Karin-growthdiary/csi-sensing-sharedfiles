# Adapted from Sionna's "Hello World" Example Notebook: https://nvlabs.github.io/sionna/examples/Hello_World.html
# Usage: python model.py [xml scene name] [starting frame]

import matplotlib.pyplot as plt
import numpy as np
import os
import sionna
from sionna.rt import load_scene, PlanarArray, Transmitter, Receiver, Camera
import sys

from interpolation import interpolate_path

SCATTERING = True
DIFFRACTION = True
SCAT_KEEP_PROB = 0.005 # Probability of Sionna keeping generated scattered path. Default is 0.001
FREQUENCY = 2.4e9
UNAUTH_DRONE_ALTITUDE = 10 # Altitude in metres
SCATTERING_COEFFICIENTS = {"itu_concrete": 0.2, "itu_medium_dry_ground": 0.3, "itu_metal":0.02}

MITSUBA_FNAME = "scene2_solid_drone" # Name of exported Mitsuba file to load in
SCENE_NAME = "scene2A" # Name to save generated CIR files as

FLIGHPATH_FNAME = "lines_pathA"
START_TIMESTAMP = 0
END_TIMESTAMP = 1000 # longlines_path1 goes from 0 to 1000 seconds long
NUM_FRAMES = 20_000 # There should be 20,000 frames (20 frames per second)

# Load in the numpy flightpath
flightpath = np.load(f"flightpaths/{FLIGHPATH_FNAME}.npy")
# Copmute the path of the unauthroized drone. Array shape: (frames, x position, y position, z position)
interpolated_path = interpolate_path(flightpath, START_TIMESTAMP, END_TIMESTAMP, NUM_FRAMES)

print("Setting CUDA variables")

if os.getenv("CUDA_VISIBLE_DEVICES") is None:
    gpu_num = 0 # Use "" to use the CPU
    os.environ["CUDA_VISIBLE_DEVICES"] = f"{gpu_num}"
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

# Load starting index from input (defaults to 0)
START_NUM = int(sys.argv[1]) if len(sys.argv)>1 else 0
print(f"Scene: {MITSUBA_FNAME}, Starting frame: {START_NUM}")

scene = load_scene(f"blender/exported-scenes/{MITSUBA_FNAME}/{MITSUBA_FNAME}.xml")
scene.frequency = FREQUENCY

# Print the radio materials in the scene for debugging
print("Materials in scene: ")
for i, obj in enumerate(scene.objects.values()):
    print(f"    {obj.name}: {obj.radio_material.name}")
    if SCATTERING:
        obj.radio_material.scattering_coefficient = SCATTERING_COEFFICIENTS[obj.radio_material.name]
        obj.radio_material.scattering_pattern = sionna.rt.DirectivePattern(alpha_r=4)

# Setup the transmitter
scene.tx_array = PlanarArray(
    num_rows=1,
    num_cols=1,
    vertical_spacing=0.5,
    horizontal_spacing=0.5,
    pattern="iso",
    polarization="V"
)

# Setup the receiver
scene.rx_array = PlanarArray(
    num_rows=2,
    num_cols=2,
    vertical_spacing=1, # Wavelengths
    horizontal_spacing=1, # Wavelengths
    pattern="iso",
    polarization="V"
)

# Position the authorized drones
scene.objects["auth_drone_0"].position = [ -5.0, -8.66, 20.0]
scene.objects["auth_drone_1"].position = [ -5.0,  8.66, 20.0]
scene.objects["auth_drone_2"].position = [ 10.0,  0.00, 20.0]

# Create and position the transmitters for each authorized drone
tx1 = Transmitter("tx1", scene.objects["auth_drone_0"].position + np.array([0,0,-0.25]), [0.0, 0.0, 0.0])
tx2 = Transmitter("tx2", scene.objects["auth_drone_1"].position + np.array([0,0,-0.25]), [0.0, 0.0, 0.0])
tx3 = Transmitter("tx3", scene.objects["auth_drone_2"].position + np.array([0,0,-0.25]), [0.0, 0.0, 0.0])

# Create and position the receiver
rx = Receiver   ("rx", [0.0, 0.0, 0.5], [0.0, 0.0, 0.0])

# Add the transmitters and receiver to the scene
scene.add(tx1)
scene.add(tx2)
scene.add(tx3)
scene.add(rx)

# Iterate through each frame:
for frame in range(START_NUM, interpolated_path.shape[0]):
  print(f"Computing frame {frame} of {interpolated_path.shape[0]}")
  
  # Move unauthorized drone position
  scene.objects["unauth_drone"].position = np.array([interpolated_path[frame][0], interpolated_path[frame][1], UNAUTH_DRONE_ALTITUDE])
  # Compute paths for the current scene
  paths = scene.compute_paths(
    scattering = SCATTERING,
    diffraction = DIFFRACTION,
    max_depth = 3,
    check_scene = False, # Disable scene checking to speed up computation
    num_samples = 1e6, # Default 1e6
    scat_keep_prob = SCAT_KEEP_PROB,
  )

  # Extract CIR for these paths
  a = paths.a
  tau = paths.tau
  types = paths.types
  
  # Save CIR for this frame
  np.savez_compressed(f"data/{SCENE_NAME}_{frame}.npz", a=a, tau=tau, types=types)
