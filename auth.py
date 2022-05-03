import anomaly
import feature
import numpy as np
import random
import cycledetection
import sys

# Constants
USERNAME = "user47"
DATA_POINTS = 200
VECTOR_SIZE = 3
NUM_SEGMENTS = 4

# Get data segments from raw data csv.
segments = cycledetection.cyclegenerator(f"{USERNAME}pocketacc")
print("Data segmented.")

# Extract features from segments.
feature.build_training_data(USERNAME, segments)
print("Feature csv built.")

# Get anomaly score from new entry
new_entry = np.array([random.randrange(-10, 10) for _ in range(36)])
print("Entry:", new_entry)
as_score = anomaly.get_anomaly_score(new_entry, f"training-data/{USERNAME}-training-data.csv")
print("Anomaly Score:", as_score)

