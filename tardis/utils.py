"""Utilities module.

This module collects some utility functions, making them accessible to
a wider number of modules.
"""

import logging
import os

import numpy as np

from tardis.data import sample_vision_data_set


def load_data(filename, batch_size, n_query_points, seed=None):
    """Load data from filename, depending on input type.

    Parameters
    ----------
    filename : str
        If this points to a file name, the function will attempt to load
        said file and parse it. Else, the function will consider this as
        the name of a data set to load.

    batch_size : int
        Number of points to sample from data set.

    n_query_points : int
        Number of points to use for the subsequent Euclidicity
        calculations. It is possible to use the full data set.

    seed : int, instance of `np.random.Generator`, or `None`
        Seed for the random number generator, or an instance of such
        a generator. If set to `None`, the default random number
        generator will be used.

    Returns
    -------
    Tuple of np.array, np.array
        The (subsampled) data set along with its query points is
        returned.
    """
    if os.path.exists(filename):
        ext = os.path.splitext(filename)[1]
        if ext == ".txt" or ext == ".gz":
            X = np.loadtxt(filename)
        elif ext == ".npz":
            X = np.load(filename)["data"]
    else:
        X = sample_vision_data_set(filename, batch_size)

    assert X is not None, RuntimeError(
        f"Unable to handle input file {filename}"
    )

    logger = logging.getLogger()

    logger.info(f"Sampling a batch of {batch_size} points")
    logger.info(f"Using {n_query_points} query points")

    rng = np.random.default_rng(seed)

    X = X[rng.choice(X.shape[0], batch_size, replace=False)]
    query_points = X[rng.choice(X.shape[0], n_query_points, replace=False)]

    return X, query_points
