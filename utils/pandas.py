import pandas as pd
from collections import Counter


def flatten_col_labels(
    df: pd.DataFrame,
    suffix: str = "_",
    omit_unique_suffix: bool = True,
    inplace: bool = False,
) -> pd.DataFrame:
    """
    Flatten a MultiIndexed-column Pandas DataFrame and return it.
    Different levels' names are joined by `suffix`.
    If `omit_unique_suffix` is True, levels with only one sublevel will preserve base level name.
    If `inplace` is False, the work will be performed on a copy of the dataframe instead.
    Returns the flattened-column DataFrame, whether it's a copy or not.
    """
    if not isinstance(df.columns, pd.MultiIndex):
        raise ValueError("DataFrame columns have only one level")
    if not inplace:
        df = df.copy()
    col_labels = df.columns.values
    counts = Counter(label for label, *sub_labels in col_labels)
    df.columns = [
        (
            label
            if (omit_unique_suffix and counts[label] == 1)
            else suffix.join((label, *sub_levels)).strip()
        )
        for label, *sub_levels in col_labels
    ]
    return df
