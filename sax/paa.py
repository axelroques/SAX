
import pandas as pd


def PAA_step(df_INT, w):
    """
    Piecewise Aggregate Approximation (PAA) (Keogh et. al., 2001) for multivariate 
    time series.

    This function assigns an equal (often floating) number of points to each
    of the w segments.

    Inputs:
    - df_INT = Resulting DataFrame from the normalization step 
    - w = number of segments
    """

    n = len(df_INT)

    # Resample dataframe
    new_index = df_INT.index.repeat(w)
    df_temp = df_INT.iloc[:, 1:].reindex(
        new_index)  # Do not apply on the time column

    # Create new re-indexed dataframe from the previously re-indexed dataframe
    df_PAA = pd.DataFrame(data=df_temp.to_numpy(),
                          index=[i for i in range(w) for k in range(n)],
                          columns=df_INT.columns[1:])

    # Average segments
    df_PAA = df_PAA.groupby(df_PAA.index).mean()

    # Create a new correct time column
    new_t = pd.date_range(start=df_INT['t'].iloc[0],
                          end=df_INT['t'].iloc[-1],
                          periods=w+1)
    df_PAA['t'] = new_t[:-1]

    # Reorder columns
    cols = df_PAA.columns.tolist()
    new_cols = cols[-1:] + cols[:-1]
    df_PAA = df_PAA[new_cols]

    return df_PAA
