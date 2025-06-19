# Training Data Quick Start Guide
To generate training data, navigate to `/training-data`.
Ensure exported Mitsuba scene is located in `/training-data/blender/exported-scenes`
Execute `python generate_paths.py [xml scene name] [starting frame]`
Execute `python generate_labels.py`

# Model Quick Start Guide
To execute the model, navigate to `/model` and execute `model.py`.

This assumes training data and labels (either downloaded as part of the GitHub repository or generated) is located in the `/training-data/data` folder.

# Datasets Included
Individual CIR files for each file are not included due to their large size. However, the following CSI cache files are provided in `/model/.cache`, which will be loaded can be loaded by `/model/dataset.py` directly:
- scene1A_CSI: Calculated CSI using scene1_solid_drone and lines_pathA flightpath, and a scattered energy proportion of 0.02. Suitable for model training.
- scene1B_CSI: Calculated CSI using scene1_solid_drone and lines_pathB flightpath, and a scattered energy proportion of 0.02. Suitable for model training.
- scene2A_CSI: Calculated CSI using scene2_solid_drone and lines_pathA flightpath, and s scattered energy proportion of 0.02. Suitable for model training.
