"""Helpers to reserve numpy arrays for use in some of the Bmi methods as output argument"""

import numpy as np
from bmipy import Bmi


def reserve_values(model: Bmi, name: str) -> np.ndarray:
    """Reserve dest for :func:`bmipy.Bmi.get_value`"""
    dtype = model.get_var_type(name)
    item_size = model.get_var_itemsize(name)
    total_size = model.get_var_nbytes(name)
    size = total_size // item_size
    return np.empty(size, dtype=dtype)


def reserve_grid_shape(model: Bmi, grid_id: int) -> np.ndarray:
    """Reserve shape for :func:`bmipy.Bmi.get_grid_shape`"""
    return np.empty(model.get_grid_rank(grid_id), dtype=np.int64)


def reserve_grid_padding(model: Bmi, grid_id: int) -> np.ndarray:
    """Reserve dest for :func:`bmipy.Bmi.get_grid_spacing` and :func:`bmipy.Bmi.get_grid_origin`"""
    return np.empty(model.get_grid_rank(grid_id), dtype=np.float64)


def reserve_grid_nodes(model: Bmi, grid_id: int, dim_index: int) -> np.ndarray:
    """Reserve dest for :func:`bmipy.Bmi.get_grid_x`, :func:`bmipy.Bmi.get_grid_y` and :func:`bmipy.Bmi.get_grid_z`

    The dim_index goes x,y,z and model.get_grid_shape goes z,y,x or y,x so index is inverted
    """
    model_type = model.get_grid_type(grid_id)
    if model_type in {"uniform_rectilinear", "rectilinear"}:
        grid_shape = model.get_grid_shape(grid_id, reserve_grid_shape(model, grid_id))
        shape = grid_shape[::-1][dim_index]
    else:
        shape = model.get_grid_size(grid_id)
    return np.empty(shape, dtype=np.float64)


def reserve_values_at_indices(model: Bmi, name: str, indices) -> np.ndarray:
    """Reserve dest for :func:`bmipy.Bmi.get_value_at_indices`"""
    dtype = model.get_var_type(name)
    return np.empty(len(indices), dtype=dtype)


def reserve_grid_edge_nodes(model: Bmi, grid_id: int) -> np.ndarray:
    """Reserve edge_nodes for :func:`bmipy.Bmi.get_grid_edge_nodes`"""
    edge_count = model.get_grid_edge_count(grid_id)
    return np.empty(2 * edge_count, dtype=np.int64)


def reserve_grid_nodes_per_face(model: Bmi, grid_id: int) -> np.ndarray:
    """Reserve nodes_per_face for :func:`bmipy.Bmi.get_grid_nodes_per_face`"""
    face_count = model.get_grid_face_count(grid_id)
    return np.empty(face_count, dtype=np.int64)


def reserve_grid_face_(model: Bmi, grid_id: int) -> np.ndarray:
    """Reserve face_edges or face_node in respectivly :func:`bmipy.Bmi.get_grid_face_edges` or :func:`bmipy.Bmi.get_grid_face_nodes`"""
    nodes_per_face = reserve_grid_nodes_per_face(model, grid_id)
    model.get_grid_nodes_per_face(grid_id, nodes_per_face)
    return np.empty(nodes_per_face.sum(), dtype=np.int64)
