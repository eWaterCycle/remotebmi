import numpy as np
from bmipy import Bmi
from httpx import Client, Limits
from numpy import ndarray

from .utils import validate_url


class RemoteBmiClient(Bmi):
    def __init__(
        self,
        base_url: str,
        timeout: int = 60 * 60 * 24,
        max_keepalive_connections: int = 0,
        client: Client | None = None,
    ):
        """RemoteBmiClient constructor

        Args:
            base_url: Where the remote BMI server is running.
            timeout: How long a response can take.
                Defaults to 1 day. Set to None to disable timeout.
            max_keepalive_connections: How many connections to keep alive. "keepalive
                connections" allow reusing of connections which is more efficient.
                However, the R server implementation can break when they are used.
            client: An optional httpx.Client instance to use. Mainly used for testing.

        Raises:
            ValueError: If the base_url is invalid.
        """
        validate_url(base_url)
        # In some Python environments the reusing connection causes `illegal status line: bytesarray(b'14')` error
        # So we need to disable keepalive connections to be more reliable, but less efficient
        limits = Limits(max_keepalive_connections=max_keepalive_connections)
        if client is None:
            self.client = Client(base_url=base_url, timeout=timeout, limits=limits)
        else:
            self.client = client

    def __del__(self) -> None:
        if hasattr(self, "client"):
            self.client.close()

    def initialize(self, config_file: str) -> None:
        response = self.client.post("/initialize", json={"config_file": config_file})
        response.raise_for_status()

    def update(self) -> None:
        response = self.client.post("/update")
        response.raise_for_status()

    def update_until(self, until: float) -> None:
        response = self.client.post("/update_until", json={"until": until})
        response.raise_for_status()

    def finalize(self) -> None:
        response = self.client.delete("/finalize")
        response.raise_for_status()

    def get_component_name(self) -> str:
        response = self.client.get("/get_component_name")
        response.raise_for_status()
        # TODO validate response, with pydantic or similar, should be done for all responses
        # see github.com/eWaterCycle/remotebmi/issues/33
        return str(response.json()["name"])  # note: cast to str to please mypy

    def get_input_var_names(self) -> tuple[str, ...]:  # type: ignore[override]
        response = self.client.get("/get_input_var_names")
        response.raise_for_status()
        return tuple(response.json())

    def get_output_var_names(self) -> tuple[str, ...]:  # type: ignore[override]
        response = self.client.get("/get_output_var_names")
        response.raise_for_status()
        return tuple(response.json())

    def get_input_item_count(self) -> int:
        response = self.client.get("/get_input_item_count")
        response.raise_for_status()
        return int(response.json())

    def get_output_item_count(self) -> int:
        response = self.client.get("/get_output_item_count")
        response.raise_for_status()
        return int(response.json())

    def get_var_grid(self, name: str) -> int:
        response = self.client.get(f"/get_var_grid/{name}")
        response.raise_for_status()
        return int(response.json())

    def get_var_type(self, name: str) -> str:
        response = self.client.get(f"/get_var_type/{name}")
        response.raise_for_status()
        raw_type = response.json()["type"]
        lookup = {
            "double": "float",
            "float": "float",
            "int64": "int",
            "int32": "int",
        }
        return lookup[raw_type]

    def get_var_units(self, name: str) -> str:
        response = self.client.get(f"/get_var_units/{name}")
        response.raise_for_status()
        return str(response.json()["units"])

    def get_var_nbytes(self, name: str) -> int:
        response = self.client.get(f"/get_var_nbytes/{name}")
        response.raise_for_status()
        return int(response.json())

    def get_var_location(self, name: str) -> str:
        response = self.client.get(f"/get_var_location/{name}")
        response.raise_for_status()
        return str(response.json()["location"])

    def get_var_itemsize(self, name: str) -> int:
        response = self.client.get(f"/get_var_itemsize/{name}")
        response.raise_for_status()
        return int(response.json())

    def get_current_time(self) -> float:
        response = self.client.get("/get_current_time")
        response.raise_for_status()
        return float(response.json())

    def get_start_time(self) -> float:
        response = self.client.get("/get_start_time")
        response.raise_for_status()
        return float(response.json())

    def get_end_time(self) -> float:
        response = self.client.get("/get_end_time")
        response.raise_for_status()
        return float(response.json())

    def get_time_units(self) -> str:
        response = self.client.get("/get_time_units")
        response.raise_for_status()
        return str(response.json()["units"])

    def get_time_step(self) -> float:
        response = self.client.get("/get_time_step")
        response.raise_for_status()
        return float(response.json())

    def get_value(self, name: str, dest: ndarray) -> ndarray:
        response = self.client.get(f"/get_value/{name}")
        response.raise_for_status()
        items = np.array(response.json())
        np.copyto(dest, items)
        return items

    def get_value_at_indices(self, name: str, dest: ndarray, inds: ndarray) -> ndarray:
        response = self.client.post(f"/get_value_at_indices/{name}", json=inds.tolist())
        response.raise_for_status()
        items = np.array(response.json())
        np.copyto(dest, items)
        return items

    def set_value(self, name: str, src: ndarray) -> None:
        response = self.client.post(f"/set_value/{name}", json=src.tolist())
        response.raise_for_status()

    def set_value_at_indices(self, name: str, inds: ndarray, src: ndarray) -> None:
        response = self.client.post(
            f"/set_value_at_indices/{name}",
            json={"indices": inds.tolist(), "values": src.tolist()},
        )
        response.raise_for_status()

    def get_value_ptr(self, name: str) -> ndarray:
        raise NotImplementedError

    def get_grid_rank(self, grid: int) -> int:
        response = self.client.get(f"/get_grid_rank/{grid}")
        response.raise_for_status()
        return int(response.json())

    def get_grid_size(self, grid: int) -> int:
        response = self.client.get(f"/get_grid_size/{grid}")
        response.raise_for_status()
        return int(response.json())

    def get_grid_type(self, grid: int) -> str:
        response = self.client.get(f"/get_grid_type/{grid}")
        response.raise_for_status()
        return str(response.json()["type"])

    def get_grid_origin(self, grid: int, origin: ndarray) -> ndarray:
        response = self.client.get(f"/get_grid_origin/{grid}")
        response.raise_for_status()
        items = np.array(response.json())
        np.copyto(origin, items)
        return items

    def get_grid_spacing(self, grid: int, spacing: ndarray) -> ndarray:
        response = self.client.get(f"/get_grid_spacing/{grid}")
        response.raise_for_status()
        items = np.array(response.json())
        np.copyto(spacing, items)
        return items

    def get_grid_shape(self, grid: int, shape: ndarray) -> ndarray:
        response = self.client.get(f"/get_grid_shape/{grid}")
        response.raise_for_status()
        items = np.array(response.json())
        np.copyto(shape, items)
        return items

    def get_grid_x(self, grid: int, x: ndarray) -> ndarray:
        response = self.client.get(f"/get_grid_x/{grid}")
        response.raise_for_status()
        items = np.array(response.json())
        np.copyto(x, items)
        return items

    def get_grid_y(self, grid: int, y: ndarray) -> ndarray:
        response = self.client.get(f"/get_grid_y/{grid}")
        response.raise_for_status()
        items = np.array(response.json())
        np.copyto(y, items)
        return items

    def get_grid_z(self, grid: int, z: ndarray) -> ndarray:
        response = self.client.get(f"/get_grid_z/{grid}")
        response.raise_for_status()
        items = np.array(response.json())
        np.copyto(z, items)
        return items

    def get_grid_node_count(self, grid: int) -> int:
        response = self.client.get(f"/get_grid_node_count/{grid}")
        response.raise_for_status()
        return int(response.json())

    def get_grid_face_nodes(self, grid: int, face_nodes: ndarray) -> ndarray:
        response = self.client.get(f"/get_grid_face_nodes/{grid}")
        response.raise_for_status()
        items = np.array(response.json())
        np.copyto(face_nodes, items)
        return items

    def get_grid_edge_count(self, grid: int) -> int:
        response = self.client.get(f"/get_grid_edge_count/{grid}")
        response.raise_for_status()
        return int(response.json())

    def get_grid_edge_nodes(self, grid: int, edge_nodes: ndarray) -> ndarray:
        response = self.client.get(f"/get_grid_edge_nodes/{grid}")
        response.raise_for_status()
        items = np.array(response.json())
        np.copyto(edge_nodes, items)
        return items

    def get_grid_face_count(self, grid: int) -> int:
        response = self.client.get(f"/get_grid_face_count/{grid}")
        response.raise_for_status()
        return int(response.json())

    def get_grid_face_edges(self, grid: int, face_edges: ndarray) -> ndarray:
        response = self.client.get(f"/get_grid_face_edges/{grid}")
        response.raise_for_status()
        items = np.array(response.json())
        np.copyto(face_edges, items)
        return items

    def get_grid_nodes_per_face(self, grid: int, nodes_per_face: ndarray) -> ndarray:
        response = self.client.get(f"/get_grid_nodes_per_face/{grid}")
        response.raise_for_status()
        items = np.array(response.json())
        np.copyto(nodes_per_face, items)
        return items
