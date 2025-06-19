# User manual 

Dataset generation code is found in `training-data/`. To produce a scene:
1. Create a scene in Blender, and export using Mitsuba Blender according to the instructions [here](https://youtu.be/7xHLDxUaQ7c). Ensure exported scene folder is saved in `training-data/blender/exported_scenes`.
2. Generate a Flightpath by running `training-data/FlightPath.py`. Ensure the generated flightpath file is saved to `training-data/flightpaths`.
3. Modify file references and parameters in `training-data/generate_paths.py`, and then execute to generate CIR training data. This will be saved in consecutively numbered files to `training-data/data/`.
4. Modify flightpath filename in `training-data/generate_labels.py`, and then execute to generate labels for training data. This will be saved in a single file in `training-data/data/`.


