from connexion import AsyncApp
from connexion.resolver import RelativeResolver
from connexion.options import SwaggerUIOptions

def initialize(config_file: str):
    print(config_file)

def update():
    print('update')

def update_until(until: float):
    print('update_until')
    print(until)

def finalize():
    print('finalize')

def get_component_name():
    print('get_component_name')

def get_input_var_names():
    print('get_input_names')

def get_output_var_names():
    print('get_output_names')

def get_input_item_count():
    print('get_input_item_count')

def get_output_item_count():
    print('get_output_item_count')

def get_var_grid(name: str):
    print('get_var_grid')
    print(name)

def get_var_type(name: str):
    print('get_var_type')
    print(name)

def get_var_units(name: str):
    print('get_var_units')
    print(name)

def get_var_nbytes(name: str):
    print('get_var_nbytes')
    print(name)

def get_var_location(name: str):
    print('get_var_location')
    print(name)

def get_var_itemsize(name: str):
    print('get_var_itemsize')
    print(name)

def get_var_shape(name: str):
    print('get_var_shape')
    print(name)

def get_value(name: str):
    print('get_value')
    print(name)

def get_value_at_indices(name: str, indices: list):
    print('get_value_at_indices')
    print(name, indices)

def set_value(name: str, new_value: float):
    print('set_value')
    print(name, new_value)

def set_value_at_indices(name: str, indices: list, values: list):
    print('set_value_at_indices')
    print(name, indices, values)

def get_grid_rank(name: str):
    print('get_grid_rank')
    print(name)

def get_grid_type(name: str):
    print('get_grid_type')
    print(name)

def get_grid_shape(name: str): 
    print('get_grid_shape')
    print(name)

def get_grid_size(name: str):
    print('get_grid_size')
    print(name)

def get_grid_spacing(name: str):
    print('get_grid_spacing')
    print(name)

def get_grid_origin(name: str):
    print('get_grid_origin')
    print(name)

def get_grid_x(name: str):
    print('get_grid_x')
    print(name)

def get_grid_y(name: str):
    print('get_grid_y')
    print(name)

def get_grid_z(name: str):
    print('get_grid_z')
    print(name)

def get_start_time():
    print('get_start_time')

def get_end_time():
    print('get_end_time')

def get_current_time():
    print('get_current_time')

def get_time_step():
    print('get_time_step')

def get_time_units():
    print('get_time_units')

def get_grid_edge_count(name: str):
    print('get_grid_edge_count')
    print(name)

def get_grid_face_count(name: str):
    print('get_grid_face_count')
    print(name)

def get_grid_edge_nodes(name: str):
    print('get_grid_edge_nodes')
    print(name)

def get_grid_face_edges(name: str):
    print('get_grid_face_edges')
    print(name)

def get_grid_face_nodes(name: str):
    print('get_grid_face_nodes')
    print(name)

def get_grid_nodes_per_face(name: str):
    print('get_grid_nodes_per_face')
    print(name)

def get_grid_node_count(grid: int):
    print('get_grid_node_count')
    print(grid)


app = AsyncApp(__name__, strict_validation=True, swagger_ui_options=SwaggerUIOptions(swagger_ui=False))

app.add_api(
    "openapi.yaml", 
    resolver=RelativeResolver('remotebmi.server')
)