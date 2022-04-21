import anomaly
import feature
import numpy as np
import random

# Constants
USERNAME = "rand"
DATA_POINTS = 200
VECTOR_SIZE = 3
NUM_SEGMENTS = 4

# Get data segments from raw data csv.

sample_segments = np.array([[[
    random.randrange(-10, 10)
    for _ in range(VECTOR_SIZE)]
    for _ in range(DATA_POINTS)]
    for _ in range(NUM_SEGMENTS)]
)

# Extract features from segments.
feature.build_training_data(USERNAME, sample_segments)

# Get anomaly score from new entry
new_entry = np.array([random.randrange(-10, 10) for _ in range(36)])
print("Entry:", new_entry)
as_score = anomaly.get_anomaly_score(new_entry, f"training-data/{USERNAME}-training-data.csv")
print("Anomaly Score:", as_score)

