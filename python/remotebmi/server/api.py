from typing import Literal

import numpy as np
from bmipy import Bmi
from connexion import request

from remotebmi.reserve import (
    reserve_grid_edge_nodes,
    reserve_grid_face_,
    reserve_grid_nodes,
    reserve_grid_nodes_per_face,
    reserve_grid_padding,
    reserve_grid_shape,
    reserve_values,
    reserve_values_at_indices,
)


def model() -> Bmi:
    # get bmi model from context
    return request.state.model


def initialize(body: dict[Literal["config_file"], str]):
    model().initialize(body["config_file"])


def update():
    model().update()


def update_until(until: float):
    model().update_until(until)


def finalize():
    model().finalize()


def get_component_name():
    return {"name": model().get_component_name()}


def get_input_var_names():
    return model().get_input_var_names()


def get_output_var_names():
    return model().get_output_var_names()


def get_input_item_count():
    return model().get_input_item_count()


def get_output_item_count():
    return model().get_output_item_count()


def get_var_grid(name: str):
    return model().get_var_grid(name)


def get_var_type(name: str):
    return {"type": model().get_var_type(name)}


def get_var_units(name: str):
    return {"units": model().get_var_units(name)}


def get_var_nbytes(name: str):
    return model().get_var_nbytes(name)


def get_var_location(name: str):
    return {"location": model().get_var_location(name)}


def get_var_itemsize(name: str):
    return model().get_var_itemsize(name)


def get_value(name: str):
    items = reserve_values(model(), name)
    return model().get_value(name, items)


# TODO correct typings


def get_value_at_indices(name: str, indices: list):
    items = reserve_values_at_indices(model(), name, indices)
    return model().get_value_at_indices(name, indices, items)


def set_value(name: str, src: list):
    items = np.array(src)
    model().set_value(name, items)


def set_value_at_indices(name: str, indices: list, values: list):
    items = np.array(values)
    model().set_value_at_indices(name, indices, items)


def get_grid_rank(name: str):
    return model().get_grid_rank(name)


def get_grid_type(name: str):
    return {"type": model().get_grid_type(name)}


def get_grid_shape(name: str):
    shape = reserve_grid_shape(model(), name)
    return model().get_grid_shape(name, shape)


def get_grid_size(name: str):
    return model().get_grid_size(name)


def get_grid_spacing(name: str):
    spacing = reserve_grid_padding(model(), name)
    return model().get_grid_spacing(name, spacing)


def get_grid_origin(name: str):
    origin = reserve_grid_padding(model(), name)
    return model().get_grid_origin(name, origin)


def get_grid_x(name: str):
    items = reserve_grid_nodes(model(), name, 0)
    return model().get_grid_x(name, items)


def get_grid_y(name: str):
    items = reserve_grid_nodes(model(), name, 1)
    return model().get_grid_y(name, items)


def get_grid_z(name: str):
    items = reserve_grid_nodes(model(), name, 2)
    return model().get_grid_z(name, items)


def get_start_time():
    return model().get_start_time()


def get_end_time():
    return model().get_end_time()


def get_current_time():
    return model().get_current_time()


def get_time_step():
    return model().get_time_step()


def get_time_units():
    return {"units": model().get_time_units()}


def get_grid_edge_count(name: str):
    return model().get_grid_edge_count(name)


def get_grid_face_count(name: str):
    return model().get_grid_face_count(name)


def get_grid_edge_nodes(name: str):
    items = reserve_grid_edge_nodes(model(), name)
    return model().get_grid_edge_nodes(name, items)


def get_grid_face_edges(name: str):
    items = reserve_grid_face_(model(), name)
    return model().get_grid_face_edges(name, items)


def get_grid_face_nodes(name: str):
    items = reserve_grid_face_(model(), name)
    return model().get_grid_face_nodes(name, items)


def get_grid_nodes_per_face(name: str):
    items = reserve_grid_nodes_per_face(model(), name)
    return model().get_grid_nodes_per_face(name, items)


def get_grid_node_count(grid: int):
    return model().get_grid_node_count(grid)
