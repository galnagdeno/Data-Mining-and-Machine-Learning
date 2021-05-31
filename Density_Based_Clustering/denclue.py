import pandas as pd
import numpy as np

def denclue(df, rad, min_density, conv_treshold):
    '''
    Performs density based clustering with Gaussian kernel probability
    density function estimator.
    Data is clustered by local maxima of an estimation of the pdf of 
    the distribution which are found by gradient ascent.
    

    Parameters
    ----------
    df: pd.DataFrame
        A data set of items to be clustered.
    rad: float
        Radius of the neighborhood of each point in df. Smaller radius
        implies greater number of local maxima in the density function, 
        thus greater number of smaller clusters -- many of which can
        be part of the same cluster -- whereas bigger radius implies 
        smoother density functions, thus smaller number of clusters --
        which can comprise more than one real cluster.
    min_density: float
        The minimum density value for which a local maxima can be called an
        density attractor.
    conv_treshold: float
        The maximum absolute change from one iteration of the gradient ascent
        to the next one for which a point is said to have converged.

    Returns
    -------
    A pd.Series in which each element represents the respective point in df
    and its value is an integer identifier of the cluster it was assigned to.
    '''
    #sets up a matrix for the attractors and an array that indicates
    #which attractor index each point is assigned to
    attractors = np.full(df.shape, np.nan)
    which_attractor = np.empty(df.shape[0], dtype=int)
    
    j = 0
    for i in range(df.shape[0]);
        point = df.iloc[i]
        local_max = find_attractor(point, df, rad, conv_treshold)

        centered = (local_max - df.values) / rad
        dot_centerd = (centered * centered).sum(axis = 1)
        kernel_values = np.exp(- dot_centerd / 2) / (2 * np.pi) ** (d / 2)
        den_val = (kernel_values.sum()) / (df.shape[0] * rad ** df.shape[1])

        #if local maximum is dense enough, call it an attractor and assign
        #it as x's attractor
        if den_val >= min_density:
            attractors[j, :] = local_max
            which_attractor[i] = j
            j += 1

    #merge attractors which are too close
    which_attractor = _merge_atractors(attractors)

    def find_density_based_clusters(atr):
        pass

    return which_attractor

def find_attractor(point, df, radius, conv_treshold):
    '''
    Parameters
    ----------
    point: pd.Series
        The point we want to find an attractor to.
    df: pd.DataFrame
        A data set of items to be clustered.
    rad: float
        Radius of the neighborhood of each point in df. Smaller radius
        implies greater number of local maxima in the density function, 
        thus greater number of smaller clusters -- many of which can
        be part of the same cluster -- whereas bigger radius implies 
        smoother density functions, thus smaller number of clusters --
        which can comprise more than one real cluster.
    conv_treshold: float
        The maximum absolute change from one iteration of the gradient ascent
        to the next one for which a point is said to have converged.
    '''
    current = point.values
    too_big = True
    d = df.shape[1]

    while too_big:
        centered = (current - df.values) / radius
        dot_centerd = (centered * centered).sum(axis = 1)
        kernel_values = np.exp(- dot_centerd / 2) / (2 * np.pi) ** (d / 2)

        next_point = ((kernel_values * df.values.T).T.sum(axis = 0) /
                                kernel_values.sum())

        error = ((next_point - current) ** 2).sum()
        too_big =  erro <= conv_treshold ** 2

        current = next_point

    return pd.Series(current, index = point.index)



