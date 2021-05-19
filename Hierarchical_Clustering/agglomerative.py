import numpy as np
import pandas as pd
from scipy.spatial.distance import pdist, squareform

#I tried to make it decent, but end up needing a bunch of for loops
#instead of vectorized opeartions
def aglm_hier_clustering(df, k, kernel=F, dist_metric='wards'):
    '''
    Gets k clusters of the data point in an aglomerative manner

    Parameters
    ----------

    kernel (bool) <<<<<<<< Not implemented
        If True, `df` is considered to be a suitable kernel matrix for
        the data set.

    dist_metric (str) <<<<<<<<<<<<<<<<< Not fully implemented
        Which metric to use to compute the cluster distances.
        If not provided, defults to 
    
    Returns
    -------
    A pd.Series in which the index represents the data points and the
    values are integers which identify unique clusters.
    '''
    n = df.shape[0]
    k = 1 if not k
    metrics = {
            #all functions have parameters (df, cluster_ind1, cluster_ind2)
            'single_link': (lambda x : pass),
            'complete_link': (lambda x : pass),
            'group_average': (lambda x : pass),
            'centroid_distance': (lambda x : pass),
            'wards': wards_method
            }

    #create sequences of clusterings
    #first assign each data point to a cluster
    clustering = pd.Series(np.arange(df.shape[0]))
    distances = pd.DataFrame(squareform(pdist(df.values, 'euclidean')))
    
    cluster_indices = clustering.unique()
    while len(cluster_indices) > k:
        #find closest pair of clusters
        closest = distances.values.argmin()
        i = min(closest % n, closest // n)
        j = max(closest % n, closest // n)

        #merge clusters
        clustering[clustering == j] = i
        distances.drop(j, inplace=True)
        distances.drop(j, axis=1, inplace=True)
        
        cluster_indices = clustering.unique()
        #update distance matrix
        for t in cluster_indices:
            dist = wards_method(df,
                     clustering == i,
                     clustering == t)
            distances[i, t] = distances[t, i] = dist
    return clustering



def wards_method(df, cluster1, cluster2):
    """
    Computes the distance of two clusters by ward's method
    

    Parameters
    ----------
    
    df (pd.DataFrame)
        Data points
    cluster1, cluster 2 (pd.Index)
        The elements of two clusters

    Returns
    -------
    The change of the sum of squared erros after clusters merge
    """

    mean_vec1 = df.loc[cluster1].mean()
    mean_vec2 = df.loc[cluster2].mean()
    n1, n2 = len(cluster1), len(cluster2)
    w = (n1 * n2 / (n1 + n2))

    return  w * ((mean_vec1.values - mean_vec2.values) ** 2).sum()
