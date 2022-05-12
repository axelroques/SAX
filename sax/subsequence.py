
import numpy as np


def generate_subsequences(df, n, k):
    """
    Given a time series S as a numpy array, extract all 
    subsequences, of length n, with a stride of k.
    Returns a numpy array, each row corresponding to a 
    subsequence. 

    Uses an indexer matrix for faster computation time.
    """

    if not n or not k:
        raise RuntimeError('No segmentation parameters were given')

    N = len(df)

    window_indexer = np.array(
        np.expand_dims(np.arange(n), 0) +
        np.expand_dims(np.arange(0, N-n+1, k), 0).T
    )

    return [df.iloc[indices, :] for indices in window_indexer]
