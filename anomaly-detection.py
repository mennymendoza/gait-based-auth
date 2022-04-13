import random
import pandas as pd
import numpy as np
import sys

USER_EXAMPLES_FILENAME = "raw-data/fake_user_features.csv"

features = [
    "AAV",
    "AC_C1",
    "AC_C2",
    "AC_DP2",
    "duration",
    "IQR",
    "kurtosis",
    "MAD",
    "max",
    "MCR",
    "mean",
    "median",
    "min",
    "P2P",
    "RMS",
    "SD",
    "skewness"
]
means = [70, 8, 66, 13, 93, 68, 52, 36, 58, 74, 4, 18, 9, 75, 72, 31, 90]

def get_anomaly_score(new_entry: np.ndarray) -> float:
    
    ''' Gets the anomaly score (AS) of the features of a single gait instance. '''

    # Unpack data from csv to numpy array
    df = pd.read_csv(USER_EXAMPLES_FILENAME)
    training_examples = df.to_numpy()
    num_examples, num_features = training_examples.shape
    
    # Dump some data and do some input vetting.
    print(f"Training shape: {training_examples.shape}")
    if len(new_entry) != num_features:
        print("Error: Entry length should match the number of features.")
        sys.exit()
    
    # Find the smallest euclidean between our entry and a training example.
    min_dist = np.amin(np.sqrt(np.sum((training_examples - new_entry)**2, axis=1)))

    # Calculate the mean and standard deviation of the training data
    all_nn_distances = np.zeros(num_examples)
    for index in range(num_examples):
        diff_matrix = np.sqrt(np.sum((training_examples - training_examples[index])**2, axis=1))
        diff_matrix = diff_matrix[diff_matrix != diff_matrix[index]]
        if (len(diff_matrix) != num_examples - 1):
            print("Simple fix failed. Issue with mean and standard deviation calculations.")
            sys.exit()
        all_nn_distances[index] = np.amin(diff_matrix)
    mean = all_nn_distances.mean()
    std_dev = all_nn_distances.std()

    # Take that smallest distance and find its z-score
    anomaly_score = (min_dist - mean) / std_dev
    
    # Dump data
    print(f"min-dist {min_dist} M: {mean} SD: {std_dev} AS: {anomaly_score}")

    return anomaly_score

# Testing

# Generate new random entry and tests AS function
new_entry = np.array([means[i] + random.randrange(-10, 10) for i in range(len(means))])
print(f"Entry: {new_entry}")
get_anomaly_score(new_entry)
