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
    n = model().get_output_var_names()
    return list(n)


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
    return model().get_value(name, items).tolist()


def get_value_at_indices(name: str, indices: list):
    items = reserve_values_at_indices(model(), name, indices)
    return (
        model().get_value_at_indices(name, np.array(indices, dtype=int), items).tolist()
    )


def set_value(name: str, src: list):
    items = np.array(src)
    model().set_value(name, items)


def set_value_at_indices(name: str, indices: list, values: list):
    items = np.array(values)
    model().set_value_at_indices(name, np.array(indices, dtype=int), items)


def get_grid_rank(grid: int):
    return model().get_grid_rank(grid)


def get_grid_type(grid: int):
    return {"type": model().get_grid_type(grid)}


def get_grid_shape(grid: int):
    shape = reserve_grid_shape(model(), grid)
    return model().get_grid_shape(grid, shape).tolist()


def get_grid_size(grid: int):
    return model().get_grid_size(grid)


def get_grid_spacing(grid: int):
    spacing = reserve_grid_padding(model(), grid)
    return model().get_grid_spacing(grid, spacing).tolist()


def get_grid_origin(grid: int):
    origin = reserve_grid_padding(model(), grid)
    return model().get_grid_origin(grid, origin).tolist()


def get_grid_x(grid: int):
    items = reserve_grid_nodes(model(), grid, 0)
    return model().get_grid_x(grid, items).tolist()


def get_grid_y(grid: int):
    items = reserve_grid_nodes(model(), grid, 1)
    return model().get_grid_y(grid, items).tolist()


def get_grid_z(grid: int):
    items = reserve_grid_nodes(model(), grid, 2)
    return model().get_grid_z(grid, items).tolist()


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


def get_grid_edge_count(grid: int):
    return model().get_grid_edge_count(grid)


def get_grid_face_count(grid: int):
    return model().get_grid_face_count(grid)


def get_grid_edge_nodes(grid: int):
    items = reserve_grid_edge_nodes(model(), grid)
    return model().get_grid_edge_nodes(grid, items).tolist()


def get_grid_face_edges(grid: int):
    items = reserve_grid_face_(model(), grid)
    return model().get_grid_face_edges(grid, items).tolist


def get_grid_face_nodes(grid: int):
    items = reserve_grid_face_(model(), grid)
    return model().get_grid_face_nodes(grid, items).tolist()


def get_grid_nodes_per_face(grid: int):
    items = reserve_grid_nodes_per_face(model(), grid)
    return model().get_grid_nodes_per_face(grid, items).tolist


def get_grid_node_count(grid: int):
    return model().get_grid_node_count(grid)
