import numpy as np

def interpolate_path(flightpath, start_timestamp=0, end_timestamp=1000, num_frames=20_000):
  """ Takes a flightpath file and interpolates the position of the drone at each frame.
  
  Flightpath file is a list of [time, x position, y position, z position] samples at random
  positions in a square plane below the transmitting authorized drones and above the
  receiver on the ground.
  """
  
  interp = lambda dimension_idx: np.interp(np.linspace(start_timestamp, end_timestamp, num_frames), flightpath[:,0], flightpath[:,dimension_idx])
  interpolated_path = np.dstack([interp(1),interp(2),interp(3)])[0]
  return interpolated_path