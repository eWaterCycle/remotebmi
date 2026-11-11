"""Encode and decode non-finite BMI values for JSON exchange.

Non-finite values use the strings defined by the IEEENumber schema in
openapi.yaml. Finite values are preserved.
"""

from math import isnan
from typing import Literal

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
    return [encode(v) for v in values.tolist()]


def decode(value: IEEENumber) -> RawNumber:
    """Decode a value from a server response for the client.

    Args:
        value: Value encoded according to the IEEENumber schema.

    Returns:
        The corresponding non-finite value for "NaN", "Infinity", or
        "-Infinity"; otherwise, the original value.
    """
    if value == "NaN":
        return float("nan")
    if value == "Infinity":
        return float("inf")
    if value == "-Infinity":
        return float("-inf")
    return value


def decode_many(
    values: list[IEEENumber],
    *,
    dest: ndarray,
) -> None:
    """Decode values and assign them into dest.

    Args:
        values: Values encoded according to the IEEENumber schema.
        dest: One-dimensional destination array, modified in place.
    """
    dest[:] = [decode(v) for v in values]
