import numpy as np
import os
import random

class FlightPath:
  def __init__(self, bounding_box: tuple[tuple[float,float,float], tuple[float,float,float]] = ((-5,-5,5),(5,5,5))):
    self.bounding_box = bounding_box

  def lines_path_path(
      self,
      duration: float = 1000,
      max_velocity: float = 5):
    
    origin = np.mean(np.array(self.bounding_box), axis=0) # Set start of flightpath to centre of bounding box

    t: float = 0 # Timestep
    path: list[np.array] = [origin] # Begin flightpath at origin
    timestamps: list[float] = [0] # Begin flightpath at t=0
    while t < duration:
      next_location = np.random.uniform( np.array(self.bounding_box[0]), np.array(self.bounding_box[1]) )
      dist = np.sqrt(np.sum((next_location - path[-1])**2))
      max_dist = (max_velocity*(duration-t))
      if dist > max_dist:
        scale_factor = max_dist / dist
        path.append( path[-1] + (next_location-path[-1])*scale_factor )
        timestamps.append(duration)
        break

      # Distance is closer than the furthest reachable distance
      t += dist / max_velocity
      path.append(next_location)
      timestamps.append(t)
    
    return np.concatenate([np.array(timestamps)[:,None],np.array(path)], axis=1)

if __name__ == "__main__":
  path = FlightPath(bounding_box=((-5,-5,5),(5,5,5))).lines_path_path(duration=1000, max_velocity=5)
  np.save("flightpaths/lines_path3.npy", path)