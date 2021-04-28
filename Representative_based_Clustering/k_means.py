import numpy as np
import pandas as pd

def k_means(data, k):
    #initialize centroids
    centroids = np.empty((k,data.shape[1]))
    centroids = pd.DataFrame(centroids, columns=data.columns)
    centroids = pd.DataFrame(generate_random_centroids(data, k))
    
    #for each point, indicates which centroid it is associated with and their distance
    group = pd.DataFrame({'distance': np.full(data.shape[0], float('inf')),
                          'centroid': np.arange(data.shape[0])})
    error = group['distance'].sum()
    prev_error = 0
    
    too_big = True
    #minimizes SSE
    while too_big:
        #asign points to closest centroid
        for i in range(centroids.shape[0]):
            centroid = centroids.loc[i]
            distances = ((data - centroid) ** 2).sum(axis=1) #finds distances from points to centroid
            #if else to replace all distances at every iteration of while
            if i == 0:
                group['centroid'] = i
                group['distance'] = distances
            else:
                closer_points = group['distance'] > distances
                group.loc[closer_points, 'centroid'] = i
                group.loc[closer_points, 'distance'] = distances[closer_points]
                
        #computes new centroids
        for i in range(k):
            cluster = data[group['centroid'] == i]
            if cluster.empty:
                centroids.loc[i] = next(generate_random_centroids(data, 1))
                #this does not guarantee that the new centroid will be
                #different from all other vectors, but the probability
                #of such occurence is slim
            else:
                centroids.loc[i] = cluster.sum() / cluster.shape[0]

        prev_error = error
        error = group['distance'].sum()
        too_big = error < prev_error
    
    return group['centroid'], error, centroids


def generate_random_centroids(df, k):
    for i in range(k):
        num = np.random.rand(df.shape[0], 1)
        yield (df * num).sum() / num.sum()
