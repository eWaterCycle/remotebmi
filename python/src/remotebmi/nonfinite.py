"""Encode non-finite BMI values for JSON exchange.

Non-finite values use the strings defined by the IEEENumber schema in
server/openapi.yaml. Finite values are preserved.

Python's `float() <https://docs.python.org/3/library/functions.html#float>`_
and `assignment into NumPy floating-point arrays
<https://numpy.org/doc/stable/user/basics.indexing.html#assigning-values-to-indexed-arrays>`_
convert "NaN", "Infinity", and "-Infinity" strings to non-finite values, so no
decoder is needed.
"""

from math import isnan
from typing import Literal

import numpy as np
from numpy import ndarray

NonFiniteSymbols = Literal["NaN", "Infinity", "-Infinity"]
IEEENumber = int | float | NonFiniteSymbols
RawNumber = int | float


def encode(value: RawNumber) -> IEEENumber:
    """Encode a model value for a server response.

    Args:
        value: Model value to encode.

    Returns:
        "NaN", "Infinity", or "-Infinity" for a non-finite value; otherwise,
        the original value.
    """
    if isnan(value):
        return "NaN"
    if value == float("inf"):
        return "Infinity"
    if value == float("-inf"):
        return "-Infinity"
    return value


def encode_many(values: ndarray) -> list[IEEENumber]:
    """Encode model values for a server response.

    Args:
        values: One-dimensional array of model values to encode.

    Returns:
        A list of values encoded according to the IEEENumber schema, in input order.
    """
    if np.isfinite(values).all():
        result: list[IEEENumber] = values.tolist()
        return result
    out = values.astype(object)
    out[np.isnan(values)] = "NaN"
    out[np.isposinf(values)] = "Infinity"
    out[np.isneginf(values)] = "-Infinity"
    encoded: list[IEEENumber] = out.tolist()
    return encoded
