import numpy as np
from sklearn.neighbors import NearestNeighbors


class CachedKnn:
    """
    Precomputed Nearest-Neighbors model so that different values of k
    don't require extra computation time.

    Note that this model assumes class labels follow a LabelEncoder format,
    i.e. {0, 1, 2, ..., n_classes - 1}.
    """

    def __init__(self, max_k, X_train, X_test, distance="euclidean"):
        self.max_k = max_k
        self.distance = distance
        self.X_train = X_train
        self.X_test = X_test
        self.knn = NearestNeighbors(
            metric=self.distance, n_jobs=-1, n_neighbors=self.max_k
        ).fit(self.X_train)

        dist_mat, idx_mat = self.knn.kneighbors(self.X_test)
        self.dist_mat = dist_mat
        self.idx_mat = idx_mat

    def fit(self, labels):
        assert len(self.X_train) == len(labels)

        self.n_classes = len(np.unique(labels))
        self.label_mat = np.empty_like(self.idx_mat, dtype=np.uint8)

        # use each row, to access the labels array
        for idx in range(self.idx_mat.shape[0]):
            row = self.idx_mat[idx, :]
            self.label_mat[idx] = labels[row]

    def predict_proba(self, k=np.inf, weighting="uniform"):
        VALID_WEIGHTINGS = {"uniform", "inverse", "root-inverse"}
        assert weighting in VALID_WEIGHTINGS

        k = min(k, self.max_k)
        label_mat = self.label_mat
        distance_mat = self.dist_mat

        # if needed, restrict to first k_neighbors columns
        if k < self.label_mat.shape[1]:
            label_mat = label_mat[:, :k]
            distance_mat = distance_mat[:, :k]

        # generate weight matrix
        if weighting == "uniform":
            weight_mat = np.ones_like(label_mat, dtype=float)
        elif weighting == "inverse":
            weight_mat = 1 / distance_mat
        elif weighting == "root-inverse":
            weight_mat = 1 / np.sqrt(distance_mat)
        else:
            raise ValueError(f"weight should be one of {VALID_WEIGHTINGS}")

        # row-wise normalized
        weight_mat /= weight_mat.sum(axis=1).reshape(-1, 1)

        # build probability matrix column-wise
        probas_mat = np.empty(shape=(label_mat.shape[0], self.n_classes))
        for cluster_idx in range(self.n_classes):
            presence_mat = label_mat == cluster_idx
            probas_mat[:, cluster_idx] = (presence_mat * weight_mat).sum(axis=1)
        return probas_mat

    def predict(self, k=np.inf, weighting="uniform"):
        probas = self.predict_proba(k=k, weighting=weighting)
        return np.argmax(probas, axis=1)
