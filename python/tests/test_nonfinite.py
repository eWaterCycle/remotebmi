import json

import numpy as np
import pytest
from numpy.testing import assert_array_equal

from remotebmi.nonfinite import IEEENumber, RawNumber, encode, encode_many


@pytest.mark.parametrize("value", [0, -1, 2**53 + 1, 1.5, -2.5, 0.0, -0.0])
def test_encode_finite(value: RawNumber) -> None:
    assert encode(value) is value


@pytest.mark.parametrize(
    "value, expected",
    [
        (float("nan"), "NaN"),
        (float("inf"), "Infinity"),
        (float("-inf"), "-Infinity"),
    ],
)
def test_encode_nonfinite(value: float, expected: str) -> None:
    result = encode(value)

    assert result == expected
    assert json.loads(json.dumps(result, allow_nan=False)) == expected


@pytest.mark.parametrize("dtype", [np.float32, np.float64])
@pytest.mark.parametrize(
    "values, expected",
    [
        ([], []),
        ([1.5, -2.0, 0.0], [1.5, -2.0, 0.0]),
        (
            [1.5, np.nan, np.inf, -np.inf, 2.0],
            [1.5, "NaN", "Infinity", "-Infinity", 2.0],
        ),
    ],
)
def test_encode_many(
    values: list[float], expected: list[IEEENumber], dtype: type[np.floating]
) -> None:
    src = np.array(values, dtype=dtype)
    original = src.copy()

    result = encode_many(src)

    assert json.loads(json.dumps(result, allow_nan=False)) == expected
    assert_array_equal(src, original)


def test_encode_many_integers() -> None:
    src = np.array([0, -1, 2**53 + 1], dtype=np.int64)

    result = encode_many(src)

    assert result == [0, -1, 2**53 + 1]
    assert all(isinstance(value, int) for value in result)
