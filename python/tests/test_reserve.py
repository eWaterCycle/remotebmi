# mypy: disable-error-code="no-untyped-def"

import numpy as np

from remotebmi.reserve import reserve_values
from tests.fake_models import Float32Model


def test_reserve_values():
    model = Float32Model()
    result = reserve_values(model, "somevar")
    assert result.dtype == np.float32
    assert result.size == 3
