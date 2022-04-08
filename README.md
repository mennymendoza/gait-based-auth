
# gait-based-auth

### Steps for Gait Based Authentication

1. Determine if a person is walking using a Walking Detection Algorithm. The algorithm simply analyzes the magnitude of the acceleration and searches for peaks at each step. Once 8 consecutive steps are found, a “gait segment” is extracted.
2. Extract the x, y, z, m, v, and h vectors from the original acceleration vector <x, y, z>.
3. Extract the relevant features from the extracted vectors.
4. Features are then used to distinguish between authorized and unauthorized user using semi-supervised anomaly detection. Essentially, we find the nearest neighbor to a new user and calculate    the Euclidean distance between them. This distance is then normalized on the distances of all training examples and used to generate an anomaly score. This score is then used to classify the new user. The threshold is determined by minimizing false positives. 
