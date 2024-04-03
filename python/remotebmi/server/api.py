from bmipy import Bmi
from connexion import request
import numpy as np


def model() -> Bmi:
    # get bmi model from context
    return request.state.model


def initialize(config_file: str):
    model().initialize(config_file)


def update():
    model().update()


def update_until(until: float):
    model().update_until(until)


def finalize():
    model().finalize()


def get_component_name():
    return model().get_component_name()


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
    return model().get_var_type(name)


def get_var_units(name: str):
    return model().get_var_units(name)


def get_var_nbytes(name: str):
    return model().get_var_nbytes(name)


def get_var_location(name: str):
    return model().get_var_location(name)


def get_var_itemsize(name: str):
    return model().get_var_itemsize(name)


def get_value(name: str):
    # TODO size correctly
    items = np.array()
    return model().get_value(name, items)


def get_value_at_indices(name: str, indices: list):
    items = np.array()
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
    return model().get_grid_type(name)


def get_grid_shape(name: str):
    return model().get_grid_shape(name)


def get_grid_size(name: str):
    return model().get_grid_size(name)


def get_grid_spacing(name: str):
    return model().get_grid_spacing(name)


def get_grid_origin(name: str):
    return model().get_grid_origin(name)


def get_grid_x(name: str):
    items = np.array()
    return model().get_grid_x(name, items)


def get_grid_y(name: str):
    items = np.array()
    return model().get_grid_y(name, items)


def get_grid_z(name: str):
    items = np.array()
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
    return model().get_time_units()


def get_grid_edge_count(name: str):
    return model().get_grid_edge_count(name)


def get_grid_face_count(name: str):
    return model().get_grid_face_count(name)


def get_grid_edge_nodes(name: str):
    items = np.array()
    return model().get_grid_edge_nodes(name, items)


def get_grid_face_edges(name: str):
    items = np.array()
    return model().get_grid_face_edges(name, items)


def get_grid_face_nodes(name: str):
    items = np.array()
    return model().get_grid_face_nodes(name, items)


def get_grid_nodes_per_face(name: str):
    items = np.array()
    return model().get_grid_nodes_per_face(name, items)


def get_grid_node_count(grid: int):
    return model().get_grid_node_count(grid)
