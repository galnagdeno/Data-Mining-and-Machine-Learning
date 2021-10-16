import numpy as np
import pandas as pd
from scipy.stats import multivariate_normal as mv_normal

class Bayes_Classifier:
    """
    Bayes Classifier for data sets with numerical attributes only.
    Both the full bayes classifier and the naive bayes classifier
    are implemented. Naive bayes is default.
    """

    def __init__(self, df, target="target", compute_cov_matrix):
        """
        Train the model with the providade data set.

        Parameters
        ----------
        df (pandas.DataFrame)
            Data set with known data points classes.
        target (str)
            Name of the column with the classification of each data point.
        full (bool)
            False (default) for naive bayes and True for full bayes
        """

        target_col = df[target]
        df = df.drop(columns=[target])
        self.classes = target_col.unique()
        self.labels = pd.Series(self.classes,
                               index = np.arange(len(self.classes)))
        target_col.replace(dict(labels))
        n = df.shape[0]

        prior_probs = np.empty(len(self.classes))
        centroids = np.empty((len(self.classes), df.shape[1]))
        cov_matrices = np.empty((len(self.classes), df.shape[1], df.shape[1]))

        for cl in range(len(self.classes)):
            data_cl = df.loc[target_col == cl].values
            n_cl = data_cl.shape[0]
            centroid = d_tacl.sum(axis=0) / n_cl
            data_centered = data_cl - centroid
            cov_cl = compute_cov_matrix(data_centered, n, full)

            prior_probs[cl] = n_cl / n
            centroids[cl] = centroid
            cov_matrices[cl] = cov_cl

        self.trained_model = {"prior_probs": prior_probs,
                              "means":centroids,
                              "cov_matrices": cov_matrices}
    def classify(self, data_points):
        """
        Classifies set of uni or multidimensional data points using a full
        bayes classifier.

        Parameters
        ----------
        data_points (matrix-like)
            A matrix of data points in which the lines represent each point
            and the columns represent each dimension of the space.

        Returns
        -------
        A numpy.array object in which the i-th entry is the most probable 
        class label of the i-th data point. 
        """
        data_points = np.array(data_points)

        results = np.empty((len(self.classes), data_points.shape[0]))

        for i in range(len(self.classes)):
            mean = self.trained_model["means"][i]
            cov = self.trained_model["cov_matrices"][i]
            prior = self.trained_model["prior_probs"][i]

            results[i] = mv_normal.pdf(data_points, mean, cov) * prior

        return self.labels[results.max(axis=0)]

    def test(self, test_set, target="target"):
        """
        Tests how accurate is the model for the given data set.
        """
        target = test_set[target]
        df = test_set.drop(columns=[target])
        comp = self.classify(test_set) == target
        return comp.sum() / df.shape[0]



class Full_Bayes_Classifier(Bayes_Classifier):
    def __init__(self, df, target="target"):
        Bayes_Classifier.__init__(df, target, _compute_cov_matrix)

    def _compute_cov_matrix(self, matrix, n):
        return matrix.T @ matrix / n



class Naive_Bayes_Classifier(Bayes_Classifier):
    def __init__(self):
        Bayes_Classifier.__init__(df, target, _compute_cov_matrix)

    def _compute_cov_matrix(self, matrix, n):
        return np.diag((matrix).sum(axis=0) / n)

