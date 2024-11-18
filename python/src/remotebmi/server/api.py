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
    return request.state.model  # type: ignore[no-any-return]


def initialize(body: dict[Literal["config_file"], str]) -> None:
    model().initialize(body["config_file"])


def update() -> None:
    model().update()


def update_until(until: float) -> None:
    model().update_until(until)


def finalize() -> None:
    model().finalize()


def get_component_name() -> dict[str, str]:
    return {"name": model().get_component_name()}


def get_input_var_names() -> tuple[str, ...]:
    return model().get_input_var_names()


def get_output_var_names() -> list[str]:
    n = model().get_output_var_names()
    return list(n)


def get_input_item_count() -> int:
    return model().get_input_item_count()


def get_output_item_count() -> int:
    return model().get_output_item_count()


def get_var_grid(name: str) -> int:
    return model().get_var_grid(name)


def get_var_type(name: str) -> dict[str, str]:
    return {"type": model().get_var_type(name)}


def get_var_units(name: str) -> dict[str, str]:
    return {"units": model().get_var_units(name)}


def get_var_nbytes(name: str) -> int:
    return model().get_var_nbytes(name)


def get_var_location(name: str) -> dict[str, str]:
    return {"location": model().get_var_location(name)}


def get_var_itemsize(name: str) -> int:
    return model().get_var_itemsize(name)


def get_value(name: str) -> list[int | float]:
    items = reserve_values(model(), name)
    return model().get_value(name, items).tolist()  # type: ignore[no-any-return]


def get_value_at_indices(name: str, indices: list) -> list[int | float]:
    items = reserve_values_at_indices(model(), name, indices)
    return (  # type: ignore[no-any-return]
        model().get_value_at_indices(name, np.array(indices, dtype=int), items).tolist()
    )


def set_value(name: str, src: list) -> None:
    items = np.array(src)
    model().set_value(name, items)


def set_value_at_indices(name: str, indices: list, values: list) -> None:
    items = np.array(values)
    model().set_value_at_indices(name, np.array(indices, dtype=int), items)


def get_grid_rank(grid: int) -> int:
    return model().get_grid_rank(grid)


def get_grid_type(grid: int) -> dict[str, str]:
    return {"type": model().get_grid_type(grid)}


def get_grid_shape(grid: int) -> list[int]:
    shape = reserve_grid_shape(model(), grid)
    return model().get_grid_shape(grid, shape).tolist()  # type: ignore[no-any-return]


def get_grid_size(grid: int) -> int:
    return model().get_grid_size(grid)


def get_grid_spacing(grid: int) -> list[float]:
    spacing = reserve_grid_padding(model(), grid)
    return model().get_grid_spacing(grid, spacing).tolist()  # type: ignore[no-any-return]


def get_grid_origin(grid: int) -> list[float]:
    origin = reserve_grid_padding(model(), grid)
    return model().get_grid_origin(grid, origin).tolist()  # type: ignore[no-any-return]


def get_grid_x(grid: int) -> list[float]:
    items = reserve_grid_nodes(model(), grid, 0)
    return model().get_grid_x(grid, items).tolist()  # type: ignore[no-any-return]


def get_grid_y(grid: int) -> list[float]:
    items = reserve_grid_nodes(model(), grid, 1)
    return model().get_grid_y(grid, items).tolist()  # type: ignore[no-any-return]


def get_grid_z(grid: int) -> list[float]:
    items = reserve_grid_nodes(model(), grid, 2)
    return model().get_grid_z(grid, items).tolist()  # type: ignore[no-any-return]


def get_start_time() -> float:
    return model().get_start_time()


def get_end_time() -> float:
    return model().get_end_time()


def get_current_time() -> float:
    return model().get_current_time()


def get_time_step() -> float:
    return model().get_time_step()


def get_time_units() -> dict[str, str]:
    return {"units": model().get_time_units()}


def get_grid_edge_count(grid: int) -> int:
    return model().get_grid_edge_count(grid)


def get_grid_face_count(grid: int) -> int:
    return model().get_grid_face_count(grid)


def get_grid_edge_nodes(grid: int) -> list[int]:
    items = reserve_grid_edge_nodes(model(), grid)
    return model().get_grid_edge_nodes(grid, items).tolist()  # type: ignore[no-any-return]


def get_grid_face_edges(grid: int) -> list[int]:
    items = reserve_grid_face_(model(), grid)
    return model().get_grid_face_edges(grid, items).tolist()  # type: ignore[no-any-return]


def get_grid_face_nodes(grid: int) -> list[int]:
    items = reserve_grid_face_(model(), grid)
    return model().get_grid_face_nodes(grid, items).tolist()  # type: ignore[no-any-return]


def get_grid_nodes_per_face(grid: int) -> list[int]:
    items = reserve_grid_nodes_per_face(model(), grid)
    return model().get_grid_nodes_per_face(grid, items).tolist()  # type: ignore[no-any-return]


def get_grid_node_count(grid: int) -> int:
    return model().get_grid_node_count(grid)
