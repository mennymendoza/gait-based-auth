
# gait-based-auth

### Steps for Gait Based Authentication

1. Determine if a person is walking using a Walking Detection Algorithm. The algorithm simply analyzes the magnitude of the acceleration and searches for peaks at each step. Once 8 consecutive steps are found, a “gait segment” is extracted.
2. Extract the x, y, z, m, v, and h vectors from the original acceleration vector <x, y, z>.
3. Extract the relevant features from the extracted vectors.
4. Features are then used to distinguish between authorized and unauthorized user using semi-supervised anomaly detection. Essentially, we find the nearest neighbor to a new user and calculate the Euclidean distance between them. This distance is then normalized on the distances of all training examples and used to generate an anomaly score. This score is then used to classify the new user. The threshold is determined by minimizing false positives. 

## Documentation

### Feature Module

There are two important functions in the feature.py script. The first is `build_feature_dataset`. All it does is look for files in the `raw-data` directory and extracts the features from any raw data file that has the users from the users list at the front. This feature data is split up and appropriately placed into the `training-data` directory and the `testing-data` directory.

Parameters:
The only required parameter is a segment size. This will determine how large the segments will be when the raw data is segmented and summarized. There's an optional parameter `training_split` which must be a float between 0 and 1; this determines the ratio of the data that will go to training. The remaining data will go to testing.

Here's an example of how to properly use the `build_feature_dataset` function.
```python
build_feature_dataset(300) # This will have a segment size of 300.
```

The other important function is `build_label_file`. This function simply appends all of the data in `testing-data` into one single dataframe and then labels the rows as 1 if they belongs to the `target_user` and 0 if the rows do not belong to the `target_user`. Another column containing the user names is also added for convenience.

Parameters:
The only required parameter is the `target_user`, which should just be a string. All users must have numerical names. For example, an acceptable user name is "42".

Here's an example of how to properly use the `build_label_file` function.
```python
build_feature_dataset(300)
build_label_file("1")
```
