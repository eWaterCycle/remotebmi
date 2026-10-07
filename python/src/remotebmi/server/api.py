from typing import Literal

import numpy as np
from bmipy import Bmi
from connexion import problem, request
from connexion.lifecycle import ConnexionResponse

from remotebmi._http import JSON, prefers_octet_stream, wire_dtype
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


def initialize(body: dict[Literal["config_file"], str]) -> tuple[None, int]:
    model().initialize(body["config_file"])
    return None, 201


def update() -> None:
    model().update()


def update_until(body: float) -> None:
    model().update_until(body)


def finalize() -> None:
    model().finalize()


def get_component_name() -> dict[str, str]:
    return {"name": model().get_component_name()}


def get_input_var_names() -> list[str]:
    n = model().get_input_var_names()
    return list(n)


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


def get_value(name: str) -> bytes | tuple[list[int | float], int, dict[str, str]]:
    items = reserve_values(model(), name)
    values = model().get_value(name, items)
    if prefers_octet_stream(request.headers.get("accept", "")):
        return values.astype(values.dtype.newbyteorder("<")).tobytes()
    return values.tolist(), 200, {"Content-Type": JSON}


def get_value_at_indices(name: str, body: list[int]) -> list[int | float]:
    indices = np.array(body, dtype=np.int64)
    items = reserve_values_at_indices(model(), name, indices)
    return model().get_value_at_indices(name, items, indices).tolist()  # type: ignore[no-any-return]


def set_value(name: str, body: list | bytes) -> ConnexionResponse | None:  # type: ignore[no-any-unimported]
    if not body:
        # connexion passes an empty octet-stream body as empty dict
        return problem(400, "Bad Request", "Request body must not be empty")
    if isinstance(body, bytes):
        dtype = wire_dtype(model().get_var_type(name))
        if len(body) % dtype.itemsize:
            detail = f"Body length {len(body)} is not a multiple of item size {dtype.itemsize} of {dtype}"
            return problem(400, "Bad Request", detail)
        items = np.frombuffer(body, dtype=dtype).astype(dtype.newbyteorder("="))
    else:
        items = np.array(body)
    model().set_value(name, items)
    return None


def set_value_at_indices(name: str, body: dict[str, list]) -> None:
    indices = np.array(body["indices"], dtype=np.int64)
    model().set_value_at_indices(name, indices, np.array(body["values"]))


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
