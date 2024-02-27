import pandas as pd
from scipy.stats import binomtest


def uniques_modes_proportion(df: pd.DataFrame, decimals: int = 4) -> pd.DataFrame:
    """
    Calculates and returns some simple high-level statistics related to categorical-vs-numerical data
    such as cardinality and mode importance for a given DataFrame.
    """
    res = df.nunique().to_frame("uniques")
    res["uniques_ratio"] = (res["uniques"] / len(df)).round(decimals)
    res["mode"] = df.mode(dropna=False).iloc[0]
    res["mode_freq"] = [
        (df[col] == val).sum() for col, val in zip(df.columns, res["mode"])
    ]
    res["mode_ratio"] = (res["mode_freq"] / len(df)).round(decimals)
    return res


def value_count_prop(df: pd.DataFrame, var: str, decimals: int = 3) -> pd.DataFrame:
    """
    Calculates and returns count, proportion and cumulative proportion for a variable in a DataFrame.
    """
    res = (
        df[var]
        .value_counts()
        .reset_index()
        .rename(columns={"index": var, var: "count"})
    )

    res["prop"] = (res["count"] / len(df)).round(decimals)
    res["cumprop"] = res["prop"].cumsum()
    return res


def df_group_mean_ratio(df, feature, target, is_binary=True):
    """
    Calculates size, mean and ratio-to-global-mean target value for each unique value of feature
    for a given dataframe df.
    If is_binary is True, also calculate p-value for a two-tailed statistical test on whether
    the group mean is significantly different from the global one.
    """
    global_mean = df[target].mean()

    def bernoulli_p_val(bernoulli_series):
        return binomtest(
            k=sum(bernoulli_series),
            n=len(bernoulli_series),
            p=global_mean,
            alternative="two-sided",
        ).pvalue

    aggregations = ["size", "mean"]
    if is_binary:
        aggregations.append(bernoulli_p_val)
    res = (
        df[[feature, target]]
        .groupby(feature)[target]
        .agg(aggregations)
        .round(3)
        .sort_index()
        .reset_index()
    )
    res["ratio"] = (res["mean"] / global_mean).round(2)
    return res
