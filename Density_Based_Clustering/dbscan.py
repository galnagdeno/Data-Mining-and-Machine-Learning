import pandas as pd
from scipy.spatial.distance import pdist, squareform

def dbscan(df, rad, minpts):
    '''
    Gets a density-based clustering by assigning points to a core point.
    Points not assigned to core points are treated as noise.

    Parameters
    ----------
    df: pd.DataFrame
        The data set to be mined.

    rad: float
        The radius of the ball by each core point.

    minpts: int
        The number of the minimal cardinality for which a point is
        considered to be a core point.

    Returns
    -------
    A pd.Series im which each index is the respective data point and
    each respective value is a integer that represents a cluster.
    '''
    #checks which points are core points and computes neighbors
    dist_matrix = squareform(pdist(df.values, metric = 'euclidean'))
    is_neighbor = dist_matrix <= rad
    is_core = is_neighbor.sum(axis = 1) >= minpts
    clustering = pd.Series(np.full(df.shape[0], -1))

    t = -1
    i = 0
    while i < len(is_core[is_core].index):
        if clustering[i] == -1:
            t += 1
            clustering[dpoint] = t
            _density_connected(dpoint)
        i += 1
    return clustering

    def _density_connected(point):
        '''
        Gets core point, ranging from 0 to df.shape[0], and assigns its
        neighbors to it's cluster. If neighbor is a core point itself,
        call _density_connected recursivelly.
        '''
        k = clustering[point]
        neighbors = is_neighbor.loc[point].index #get neighbors of x
        clustering[neighbors] = k #assign them to x's cluster

        #locates core neighbors and apply recursively
        core_neighbors = is_core[is_core[neighbors] == True].index
        core_neighbors.to_series().apply(_density_connected)
