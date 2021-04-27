import numpy as np
import pandas as pd

def k_means(data, k, threshold=0):
    #initialize centroids
    centroids = np.empty((k,data.shape[1]))
    centroids = pd.DataFrame(centroids, columns=data.columns)
    for col in data.columns:
        centroid = np.random.uniform(data[col].min(), data[col].max, k)
        centroids[col] = centroid
    
    #for each point, indicates which centroid it is associated with and their distance
    group = pd.DataFrame({'distance': np.full(data.shape[0], float('inf')), 'centroid': np.arange(data.shape[0])})
    error = prev_error = group['distance'].sum()

    #minimizes SSE
    while error > threshold or error > prev_error:
        #asign points to closest centroid
        for i in range(centroids.shape[0]):
            centroid = centroids.loc[i]
            distances = ((data - centroid) ** 2).sum(axis=1) #finds distances from points to centroid
            closer_points = group['distance'] > distances
            group[closer_points]['centroid'] = i
            group[closer_points['distance']] = distances[closer_points]

        #computes new centroids
        for i in range(k):
            cluster = data[group['centroid'] == i]
            centroids.loc[i] = cluster.sum() / cluster.shape[0]

        prev_error = error
        error = group['distance'].sum()
    
    return group['centroid'], error
