
from scipy.stats import rankdata, norm
import pandas as pd


def INT(S, c):
    """
    Rank-based inverse normal transformation is a nonparametric transformation to 
    convert a sample distribution to the normal distribution.
    NaN values are ignored.

    Inputs:
    - S = pandas series 
    - c = Bloms constant

    Output:
    - transformed = normally distributed pandas series 
    """

    # Get rank, ties are averaged
    rank = rankdata(S, method="average")

    # Convert rank to normal distribution
    n = len(rank)
    transformed = norm.ppf((rank-c)/(n-2*c+1))

    return transformed


def INT_step(df, c=3.0/8):
    """
    Transforms all series in a dataframe using the rank-based inverse normal
    transformation.
    """

    # Initialize data structure
    data = {col: [] for col in df.columns}
    data['t'] = df['t']

    # Process each column of the input dataframe
    for col in df.columns[1:]:
        data[col] = INT(df[col], c)

    return pd.DataFrame(data=data, index=df.index)
