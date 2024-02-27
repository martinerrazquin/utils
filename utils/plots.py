import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np


def rolling_means_std(
    x,
    y,
    window,
    pd_rolling_kwargs={},
    ax=None,
    scatter_kwargs={},
    figsize=(10, 8),
    colors=("red", "grey"),
    alpha=0.4,
):
    """
    Scatterplot and rolling means +- std for Y|X=x.
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=figsize)
    sns.scatterplot(x=x, y=y, ax=ax, **scatter_kwargs)

    sorted_x_idxs = np.argsort(x)
    sorted_x = x[sorted_x_idxs]
    rolls = pd.Series(y[sorted_x_idxs]).rolling(window, **pd_rolling_kwargs)
    mus = rolls.mean().to_numpy()
    stds = rolls.std().to_numpy()

    ax.plot(sorted_x, mus, color=colors[0])
    ax.fill_between(sorted_x, mus - stds, mus + stds, alpha=alpha, color=colors[1])
    return ax
