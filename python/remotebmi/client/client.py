import json

import numpy as np
from bmipy import Bmi
from httpx import Client, HTTPStatusError, Response
from numpy import ndarray

def raise_for_status(response: Response):
    try:
        response.raise_for_status()
    except HTTPStatusError as e:
        # Create a response with problem details body
        body = {
            "title": str(e),
            "detail": e.response.text,
            "status": e.response.status_code,
        }
        response = Response(
            status_code=e.response.status_code,
            content=json.dumps(body),
            headers=e.response.headers,
        )
        raise response from e

class RemoteBmiClient(Bmi):
    def __init__(self, base_url, timeout=60 * 60 * 24):
        """RemoteBmiClient constructor

        Args:
            base_url: Where the remote BMI server is running.
            timeout: How long a response can take.
                Defaults to 1 day. Set to None to disable timeout.
        """
        self.client = Client(base_url=base_url, timeout=timeout)

    def __del__(self):
        self.client.close()

    def initialize(self, config_file):
        response = self.client.post("/initialize", json={"config_file": config_file})
        response.raise_for_status()

    def update(self):
        response = self.client.post("/update")
        response.raise_for_status()

    def update_until(self, until):
        response = self.client.post("/update_until", json={"until": until})
        response.raise_for_status()

    def finalize(self):
        response = self.client.delete("/finalize")
        response.raise_for_status()

    def get_component_name(self):
        response = self.client.get("/get_component_name")
        response.raise_for_status()
        return response.json()["name"]

    def get_input_var_names(self):
        response = self.client.get("/get_input_var_names")
        response.raise_for_status()
        return response.json()

    def get_output_var_names(self):
        response = self.client.get("/get_output_var_names")
        response.raise_for_status()
        return response.json()

    def get_input_item_count(self):
        response = self.client.get("/get_input_item_count")
        response.raise_for_status()
        return response.json()

    def get_output_item_count(self):
        response = self.client.get("/get_output_item_count")
        response.raise_for_status()
        return response.json()

    def get_var_grid(self, name):
        response = self.client.get(f"/get_var_grid/{name}")
        response.raise_for_status()
        return response.json()

    def get_var_type(self, name):
        response = self.client.get(f"/get_var_type/{name}")
        response.raise_for_status()
        raw_type = response.json()["type"]
        lookup = {
            "double": np.float64,
            "float": np.float32,
            "int64": np.int64,
            "int32": np.int32,
        }
        return lookup[raw_type]

    def get_var_units(self, name):
        response = self.client.get(f"/get_var_units/{name}")
        response.raise_for_status()
        return response.json()["units"]

    def get_var_nbytes(self, name):
        response = self.client.get(f"/get_var_nbytes/{name}")
        response.raise_for_status()
        return response.json()

    def get_var_location(self, name):
        response = self.client.get(f"/get_var_location/{name}")
        response.raise_for_status()
        return response.json()["location"]

    def get_var_itemsize(self, name):
        response = self.client.get(f"/get_var_itemsize/{name}")
        response.raise_for_status()
        return response.json()

    def get_current_time(self) -> float:
        response = self.client.get("/get_current_time")
        response.raise_for_status()
        return response.json()

    def get_start_time(self) -> float:
        response = self.client.get("/get_start_time")
        response.raise_for_status()
        return response.json()

    def get_end_time(self) -> float:
        response = self.client.get("/get_end_time")
        response.raise_for_status()
        return response.json()

    def get_time_units(self) -> str:
        response = self.client.get("/get_time_units")
        response.raise_for_status()
        return response.json()["units"]

    def get_time_step(self) -> float:
        response = self.client.get("/get_time_step")
        response.raise_for_status()
        return response.json()

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
        return response.json()

    def get_grid_size(self, grid: int) -> int:
        response = self.client.get(f"/get_grid_size/{grid}")
        response.raise_for_status()
        return response.json()

    def get_grid_type(self, grid: int) -> str:
        response = self.client.get(f"/get_grid_type/{grid}")
        response.raise_for_status()
        return response.json()["type"]

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
        return response.json()

    def get_grid_face_nodes(self, grid: int, face_nodes: ndarray) -> ndarray:
        response = self.client.get(f"/get_grid_face_nodes/{grid}")
        response.raise_for_status()
        items = np.array(response.json())
        np.copyto(face_nodes, items)
        return items

    def get_grid_edge_count(self, grid: int) -> int:
        response = self.client.get(f"/get_grid_edge_count/{grid}")
        response.raise_for_status()
        return response.json()

    def get_grid_edge_nodes(self, grid: int, edge_nodes: ndarray) -> ndarray:
        response = self.client.get(f"/get_grid_edge_nodes/{grid}")
        response.raise_for_status()
        items = np.array(response.json())
        np.copyto(edge_nodes, items)
        return items

    def get_grid_face_count(self, grid: int) -> int:
        response = self.client.get(f"/get_grid_face_count/{grid}")
        response.raise_for_status()
        return response.json()

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
