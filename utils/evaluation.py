import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.metrics import precision_recall_curve
from sklearn.base import BaseEstimator, TransformerMixin
from matplotlib.axes._axes import Axes
from typing import Iterator
from .itertools import pairs


class PRCurveRegistry:
    """
    Just a simple dict for saving and comparing PR curves of different models
    on a common validation set.
    """

    def __init__(self, X, y):
        self.d = {}
        self.X = X
        self.y = y

    def save(
        self, model_name: str, model: BaseEstimator, transform: TransformerMixin = None
    ):
        if model_name in self.d:
            raise KeyError(f"key {model_name} already exists")
        X = transform.transform(self.X) if transform is not None else self.X
        prec, rec, _ = precision_recall_curve(self.y, model.predict_proba(X)[:, 1])
        self.d[model_name] = rec, prec

    def compare(self, model_names: list[str], **kwargs) -> Axes:
        not_found = set(model_names) - self.d.keys()
        if len(not_found) > 1:
            raise KeyError(f"keys {','.join(not_found)} not found in the registry")

        fig, ax = plt.subplots(**kwargs)

        for model_name in model_names:
            ax.plot(*self.d[model_name], label=model_name)
        ax.set_xlabel("Recall")
        ax.set_ylabel("Precision")
        ax.legend()
        return ax


def split_expanding_date_window(
    y: pd.Series | np.ndarray,
    step: pd.Timedelta,
    min_date: pd.Timestamp,
    max_date: pd.Timestamp,
) -> Iterator[tuple[np.ndarray, np.ndarray]]:
    """
    Given a timestamp-valued pandas Series or numpy array, give step-long pairs (a,b)
    of indices where the first a value gives y[a] >= min_date and the last b value gives
    y[b] <= max_date and y[b]+step > max_date.
    Note: y is EXPECTED to be sorted.
    """
    vals = y if isinstance(y, np.ndarray) else y.values
    assert np.all(vals[:-1] <= vals[1:]), "array is not sorted"
    n_steps = (max_date - min_date) // step
    assert n_steps > 0, "parameters resulted in 0 steps"
    idxs = [(y >= min_date + step * n).argmax() for n in range(n_steps + 1)]
    return pairs(idxs)
