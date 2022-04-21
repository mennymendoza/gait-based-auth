import pandas as pd
import numpy as np
import sys

def get_anomaly_score(new_entry: np.ndarray, filepath: str, verbose=False) -> float:
    
    ''' Gets the anomaly score (AS) of the features of a single gait instance. '''

    # Unpack data from csv to numpy array
    df = pd.read_csv(filepath)
    training_examples = df.to_numpy()
    num_examples, num_features = training_examples.shape
    
    # Dump some data and do some input vetting.
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
    if verbose:
        print(f"min-dist {min_dist} M: {mean} SD: {std_dev} AS: {anomaly_score}")

    return anomaly_score

# Testing

