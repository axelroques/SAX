
import pandas as pd
import numpy as np


def discretization_step(df_PAA, alphabet, breakpoints):
    """
    Symbolic representation of df_PAA.

    Inputs:
    - df_PAA = PAA of a pandas dataframe
    - a = alphabet size.
    """

    # Initialize data structure
    data = {col: [] for col in df_PAA.columns}
    data['t'] = df_PAA['t']

    # Process each column of the input dataframe
    n = len(df_PAA)
    for col in df_PAA.columns[1:]:

        # Convert each value into a letter
        discretization = []
        for t in range(n):
            discretization.append(alphabet[np.searchsorted(breakpoints,
                                                           df_PAA[col].iloc[t],
                                                           side='left')])

        # Store this column's results
        data[col] = discretization

    return pd.DataFrame(data=data, index=df_PAA.index)
