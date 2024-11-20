# mypy: disable-error-code="no-untyped-def"

import numpy as np
import pytest
from numpy.testing import assert_array_equal

from remotebmi import RemoteBmiClient
from remotebmi.reserve import (
    reserve_grid_nodes,
    reserve_grid_shape,
)
from remotebmi.server import make_app

from .fake_models import Rect3DGridModel


@pytest.fixture
def fake_app():
    return make_app(Rect3DGridModel())


@pytest.fixture
def fake_client(fake_app):
    with fake_app.test_client() as httpclient:
        yield RemoteBmiClient(base_url="http://testserver", client=httpclient)


def test_initialize(fake_client):
    fake_client.initialize("test.cfg")
    # TODO model func is a noop, use smarter model to test this better


def test_get_output_var_names(fake_client):
    names = fake_client.get_output_var_names()
    assert names == ("plate_surface__temperature",)


def test_get_output_item_count(fake_client):
    count = fake_client.get_output_item_count()
    assert count == 1


def test_var_grid(fake_client):
    grid = fake_client.get_var_grid("plate_surface__temperature")
    assert grid == 0


def test_get_grid_type(fake_client):
    gtype = fake_client.get_grid_type(1)
    assert gtype == "rectilinear"


def test_grid_size(fake_client):
    size = fake_client.get_grid_size(1)
    assert size == 24


def test_grid_rank(fake_client):
    rank = fake_client.get_grid_rank(1)
    assert rank == 3


def test_grid_shape(fake_client):
    out = reserve_grid_shape(fake_client, 1)

    result = fake_client.get_grid_shape(1, out)

    expected = np.array([2, 3, 4], dtype=np.int64)
    assert_array_equal(result, expected)
    assert_array_equal(out, expected)


def test_get_grid_x(fake_client):
    out = reserve_grid_nodes(fake_client, 1)

    result = fake_client.get_grid_x(1, out)

    expected = np.array([0.1, 0.2, 0.3, 0.4])
    assert_array_equal(result, expected)
    assert_array_equal(out, expected)


def test_get_grid_y(fake_client):
    out = reserve_grid_nodes(fake_client, 1, 1)

    result = fake_client.get_grid_y(1, out)

    expected = np.array([1.1, 1.2, 1.3])
    assert_array_equal(result, expected)
    assert_array_equal(out, expected)


def test_get_grid_z(fake_client):
    out = reserve_grid_nodes(fake_client, 1, 2)

    result = fake_client.get_grid_z(1, out)

    expected = np.array([2.1, 2.2])
    assert_array_equal(result, expected)
    assert_array_equal(out, expected)


# TODO test all BMI functions
