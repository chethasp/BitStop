import numpy as np
from numpy.typing import ArrayLike as ArrayLike

def dot(a: ArrayLike, b: np.ndarray) -> np.ndarray:
    """Take arrays `a` and `b` and form the dot product between the last axis
    of `a` and the first of `b`.
    """
def outer(a: ArrayLike, b: ArrayLike) -> np.ndarray:
    """Compute the outer product of two arrays `a` and `b` such that the shape
    of the resulting array is `(*a.shape, *b.shape)`.
    """
def solve(A: np.ndarray, x: np.ndarray) -> np.ndarray:
    """Solves a linear equation system with a matrix of shape (n, n) and an array of
    shape (n, ...). The output has the same shape as the second argument.
    """
def sum_at(a: ArrayLike, indices: ArrayLike, minlength: int):
    """Sums up values `a` with `indices` into an output array of at least
    length `minlength` while treating dimensionality correctly. It's a lot
    faster than numpy's own np.add.at (see
    https://github.com/numpy/numpy/issues/5922#issuecomment-511477435).

    Typically, `indices` will be a one-dimensional array; `a` can have any
    dimensionality. In this case, the output array will have shape (minlength,
    a.shape[1:]).

    `indices` may have arbitrary shape, too, but then `a` has to start out the
    same. (Those dimensions are flattened out in the computation.)
    """
def add_at(a: ArrayLike, indices: ArrayLike, b: ArrayLike): ...
def subtract_at(a: ArrayLike, indices: ArrayLike, b: ArrayLike): ...
