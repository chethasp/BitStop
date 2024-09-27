import numpy as np
from numpy.typing import ArrayLike as ArrayLike

def mean(x: ArrayLike, p: float = 1) -> np.ndarray:
    """Generalized mean.

    See <https://github.com/numpy/numpy/issues/19341> for the numpy issue.
    """
