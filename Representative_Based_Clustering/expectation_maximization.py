import pandas as pd
import numpy as np
from scipy.stats import multivariate_normal as mvnorm
from functools import reduce

def expect_max(df, k):
    n = df.shape[0]
    dim = df.shape[1]

    #initalize the random centroids
    mean_vectors = pd.DataFrame(np.random.uniform(size = (k, dim)),
                    columns = df.columns)
    min_val = df.min()
    max_val = df.max()
    mean_vectors = mean_vectors * (max_val - min_val) + min_val

    #initialize the covariance matricesfor each cluster
    cov_matrices = np.empty(k, np.ndarray)
    for i in range(k):
        cov_matrices[i] = np.identity(dim)

    cluster_probs= np.full(k, 1 / k)
    cond_probs = np.empty((k, n)) # P(C_i | x_j)
    density_values = np.empty((n, k)) # f(x_j|mu_a, Sigma_a)

    error = float('inf')
    too_big = True

    while too_big:
        #calculates the relevant density values for each point
        for i in range(k):
            density_values[:, i] = mvnorm.pdf(df.values, mean_vectors.loc[i],
                                            cov_matrices[i])

        #f(x_j| mu_a, Sigma_a)*P(C_a) vector for each point
        point_cluster_density = (density_values * cluster_probs).sum(axis = 1)
        #computes posterior probabilities
        for i in range(k):
            cond_probs[i, :] = ((density_values[:, i] * cluster_probs[i]) / 
                        point_cluster_density)

        #sum of the weights
        weight_sums = density_values * cluster_probs
        #re-estimate mean vectors
        new_means = ((cond_probs @ df.values).T /
                                weight_sums.sum(axis=1))).T
        #re-estimate cluster probabilities
        cluster_prob = cond_probs.sum(axis = 1) / n
        #re-estimate covariance matrices
        for i in range(k):
            df_centered = df.values - mean_vectors[i]
            cov_matrices[i] = reduce(redc_func,
                                     df_centered.values,
                                     np.zeros((dim, dim))) / (
                                             weight_sums[i].sum()
                                             )
        
        new_error = ((mean_vectors.values - new_means) ** 2).sum() 
        if not new_error < error:
            too_big = False

        mean_vectors.values = new_means
        error = new_error
    
    return mean_vectors, cov_matrices

def redc_func(total, arr):
    mat = arr.reshape(arr.shape[0], 1).dot(np.asmatrix(arr))
    total += mat
    return total
