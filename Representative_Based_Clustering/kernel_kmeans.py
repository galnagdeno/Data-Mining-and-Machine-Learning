import pandas as pd
import numpy as np
from itertools import product as cartesian

def kernel_kmeans(kernel_matrix, k):
    '''
    `kernel_matrix` (np.DataFrame)
    ------------------------------
    Symmetric square matrix. Columns are named the number of their
    position. Furthermore, each column name is an integer.
    '''
    #initial random clustering
    clustering = get_random_cluster(kernel_matrix, k)

    #array of sqnorms of each cluster's mean
    clusters_sqnorms = np.empty(k)

    #average kernel value of a point to a cluster
    average_kvalue = np.empty((kernel_matrix.shape[0], k))

    #distance from each point to each cluster in feature space
    distances = np.empty((kernel_matrix.shape[0], k))

    error = float('inf')
    prev_error = 0
    too_big = True
    
    #minimizes SSE
    while too_big:
        for i in range(k):
            cluster = clustering[i]
            cluster_size = cluster.shape[0]
            #computes squared norm of cluster means
            clusters_sqnorms[i] = kernel_matrix.loc[cluster, cluster].sum().sum() / cluster_size ** 2
            
            #average kernel value for each point and each cluster
            average_kvalue[:, i] = kernel_matrix[cluster].values.sum(axis=1) / cluster_size

            #computes the distance from each point to each cluster
            distances[i] = average_kvalue[i] - clusters_sqnorms[i]

        #gets the closest cluster to each point
        new_clusters = pd.Series(distances.argmin(axis = 1))

        #divides the new clustering
        clustering = []
        for i in range(k):
            clustering.append(new_clusters[new_clusters == i].index.values)

        #checks if the error has converged
        error = distances.sum()
        prev_error = error
        too_big = error < prev_error

    return new_clusters, error


def get_random_cluster(matrix, k):
    items = np.arange(1, matrix.shape[0])
    part = np.random.choice(items, k - 1, replace = False)
    part = np.sort(part)
    items = np.concatenate(([0], items))
    np.random.shuffle(items)

    clustering = []
    initial = 0
    final = part[0]
    for i in range(k):
        clustering.append(items[initial:final])
        initial = final
        if i == k-1:
            final = matrix.shape[1]
        else:
            final = part[i]
    if len(clustering) != k:
        raise Exception("Random cluster too small")
    else:
        return np.array(clustering)
