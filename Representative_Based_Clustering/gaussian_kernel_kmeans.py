import pandas as pd
import scipy
from kernel_kmeans import kernel_kmeans
from scipy.spatial.distance import pdist, squareform

def gaussian_kmeans(df, var, num_clusters):
    kernel_matrix = scipy.exp(- squareform(pdist(df, 'euclidean')) / var ** 2)
    kernel_matrix = pd.DataFrame(kernel_matrix, columns = range(df.shape[0]))
    return kernel_kmeans(kernel_matrix, num_clusters)
    

