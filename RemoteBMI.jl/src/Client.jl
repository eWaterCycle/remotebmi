module Client

using HTTP
using JSON
using OpenAPI
import OpenAPI.Clients
include("client/BmiClient.jl")
using .BmiClient

import BasicModelInterface as BMI

Base.@kwdef mutable struct BMIClient
  base_url::String
end

# Model control functions

# in https://github.com/csdms/bmi-example-julia/blob/b5d963e6bf864f5d42769e6cc0814dd7bffc9264/src/bmi.jl#L5
# and https://github.com/Deltares/Wflow.jl/blob/788eaad5848e4e02d5357a7c17df363fcfd7d7b7/src/bmi.jl#L23
# the initialize first argument is a class not an instance
# here we use an instance that has be setup with the base_url
# TODO is this ok? Could move base_url arg here, but will need other args like timeouts.
function BMI.initialize(m::BMIClient, config_file::String)
  # TODO store api instance inside m so we dont recreate it each time
  api = IRFApi(OpenAPI.Clients.Client(m.base_url))
  data, response = initialize(api, InitializeRequest(config_file))
  # TODO check response status code is OK
  return m
end

function BMI.update(m::BMIClient)
  api = IRFApi(OpenAPI.Clients.Client(m.base_url))
  data, response = update(api)
  return nothing
end

function BMI.update_until(m::BMIClient, time::Float64)
  api = IRFApi(OpenAPI.Clients.Client(m.base_url))
  data, response = update_until(api, time)
  return nothing
end

function BMI.finalize(m::BMIClient)
  api = IRFApi(OpenAPI.Clients.Client(m.base_url))
  data, response = BmiClient.finalize(api)
  return nothing
end

# Model information functions

function BMI.get_component_name(m::BMIClient)
  api = ExchangeItemsApi(OpenAPI.Clients.Client(m.base_url))
  data, response = get_component_name(api)
  response.status == 200 || throw(OpenAPI.Clients.APIError(response))
  return data.name
end

function BMI.get_input_var_names(m::BMIClient)::Vector{String}
  api = ExchangeItemsApi(OpenAPI.Clients.Client(m.base_url))
  data, response = get_input_var_names(api)
  return data
end

function BMI.get_input_item_count(m::BMIClient)
  api = ExchangeItemsApi(OpenAPI.Clients.Client(m.base_url))
  data, response = get_input_item_count(api)
  return data
end

function BMI.get_output_var_names(m::BMIClient)
  api = ExchangeItemsApi(OpenAPI.Clients.Client(m.base_url))
  data, response = get_output_var_names(api)
  return data
end

function BMI.get_output_item_count(m::BMIClient)
  api = ExchangeItemsApi(OpenAPI.Clients.Client(m.base_url))
  data, response = get_output_item_count(api)
  return data
end

# Variable information functions

function BMI.get_var_grid(m::BMIClient, name)
  api = VariableInformationApi(OpenAPI.Clients.Client(m.base_url))
  data, response = get_var_grid(api, name)
  return data
end

function BMI.get_var_type(m::BMIClient, name::String)
  api = VariableInformationApi(OpenAPI.Clients.Client(m.base_url))
  data, response = get_var_type(api, name)
  # Map openapi type to julia type
  type_map =
    Dict("float" => "Float32", "double" => "Float64", "int32" => "Int32", "int64" => "Int64")
  return type_map[data.type]
end

function BMI.get_var_units(m::BMIClient, name::String)
  api = VariableInformationApi(OpenAPI.Clients.Client(m.base_url))
  data, response = get_var_units(api, name)
  return data.units
end

function BMI.get_var_itemsize(m::BMIClient, name::String)
  api = VariableInformationApi(OpenAPI.Clients.Client(m.base_url))
  data, response = get_var_itemsize(api, name)
  return data
end

function BMI.get_var_nbytes(m::BMIClient, name::String)
  api = VariableInformationApi(OpenAPI.Clients.Client(m.base_url))
  data, response = get_var_nbytes(api, name)
  return data
end

function BMI.get_var_location(m::BMIClient, name::String)
  api = VariableInformationApi(OpenAPI.Clients.Client(m.base_url))
  data, response = get_var_location(api, name)
  return data.location
end

# Time functions

function BMI.get_current_time(m::BMIClient)
  api = TimeInformationApi(OpenAPI.Clients.Client(m.base_url))
  data, response = get_current_time(api)
  return data
end

function BMI.get_start_time(m::BMIClient)
  api = TimeInformationApi(OpenAPI.Clients.Client(m.base_url))
  data, response = get_start_time(api)
  return data
end

function BMI.get_end_time(m::BMIClient)
  api = TimeInformationApi(OpenAPI.Clients.Client(m.base_url))
  data, response = get_end_time(api)
  return data
end

function BMI.get_time_units(m::BMIClient)
  api = TimeInformationApi(OpenAPI.Clients.Client(m.base_url))
  data, response = get_time_units(api)
  return data.units
end

function BMI.get_time_step(m::BMIClient)
  api = TimeInformationApi(OpenAPI.Clients.Client(m.base_url))
  data, response = get_time_step(api)
  return data
end

# Variable getter and setter functions

function BMI.get_value(m::BMIClient, name::String, dest::AbstractArray{T}) where {T}
  api = GettersApi(OpenAPI.Clients.Client(m.base_url))
  data, response = get_value(api, name)
  copyto!(dest, data)
  return dest
end

function BMI.get_value_at_indices(
  m::BMIClient,
  name::String,
  dest::AbstractArray{T},
  inds::Vector{Int},
) where {T}
  api = GettersApi(OpenAPI.Clients.Client(m.base_url))
  oinds = inds .- 1
  data, response = get_value_at_indices(api, name, oinds)
  copyto!(dest, data)
  return dest
end

function BMI.set_value(m::BMIClient, name::String, src::AbstractArray{T}) where {T}
  api = SettersApi(OpenAPI.Clients.Client(m.base_url))
  data, response = set_value(api, name, src)
  return nothing
end

function BMI.set_value_at_indices(
  m::BMIClient,
  name::String,
  inds::Vector{Int},
  src::AbstractArray{T},
) where {T}
  api = SettersApi(OpenAPI.Clients.Client(m.base_url))
  oinds = inds .- 1
  request = SetValueAtIndicesRequest(; indices = oinds, values = src)
  data, response = set_value_at_indices(api, name, request)
  return nothing
end

# Model grid functions

function BMI.get_grid_type(m::BMIClient, grid)
  api = GridInformationApi(OpenAPI.Clients.Client(m.base_url))
  data, response = get_grid_type(api, grid)
  return data.type
end

function BMI.get_grid_rank(m::BMIClient, grid)
  api = GridInformationApi(OpenAPI.Clients.Client(m.base_url))
  data, response = get_grid_rank(api, grid)
  return data
end

function BMI.get_grid_size(m::BMIClient, grid)
  api = GridInformationApi(OpenAPI.Clients.Client(m.base_url))
  data, response = get_grid_size(api, grid)
  return data
end

function BMI.get_grid_shape(m::BMIClient, grid)
  api = UniformRectilinearApi(OpenAPI.Clients.Client(m.base_url))
  data, response = get_grid_shape(api, grid)
  return data
end

function BMI.get_grid_spacing(m::BMIClient, grid, spacing::Vector{T}) where {T <: AbstractFloat}
  api = UniformRectilinearApi(OpenAPI.Clients.Client(m.base_url))
  data, response = get_grid_spacing(api, grid)
  copyto!(spacing, data)
  return spacing
end

function BMI.get_grid_origin(m::BMIClient, grid, origin::Vector{T}) where {T <: AbstractFloat}
  api = UniformRectilinearApi(OpenAPI.Clients.Client(m.base_url))
  data, response = get_grid_origin(api, grid)
  copyto!(origin, data)
  return origin
end

function BMI.get_grid_x(m::BMIClient, grid, x::Vector{T}) where {T <: AbstractFloat}
  api = NURCApi(OpenAPI.Clients.Client(m.base_url))
  data, response = get_grid_x(api, grid)
  copyto!(x, data)
  return x
end

function BMI.get_grid_y(m::BMIClient, grid, y::Vector{T}) where {T <: AbstractFloat}
  api = NURCApi(OpenAPI.Clients.Client(m.base_url))
  data, response = get_grid_y(api, grid)
  copyto!(y, data)
  return y
end

function BMI.get_grid_z(m::BMIClient, grid, z::Vector{T}) where {T <: AbstractFloat}
  api = NURCApi(OpenAPI.Clients.Client(m.base_url))
  data, response = get_grid_z(api, grid)
  copyto!(z, data)
  return z
end

function BMI.get_grid_node_count(m::BMIClient, grid)
  api = UnstructuredApi(OpenAPI.Clients.Client(m.base_url))
  data, response = get_grid_node_count(api, grid)
  return data
end

function BMI.get_grid_edge_count(m::BMIClient, grid)
  api = UnstructuredApi(OpenAPI.Clients.Client(m.base_url))
  data, response = get_grid_edge_count(api, grid)
  return data
end

function BMI.get_grid_face_count(m::BMIClient, grid)
  api = UnstructuredApi(OpenAPI.Clients.Client(m.base_url))
  data, response = get_grid_face_count(api, grid)
  return data
end

function BMI.get_grid_edge_nodes(m::BMIClient, grid, edge_nodes::Vector{Int})
  api = UnstructuredApi(OpenAPI.Clients.Client(m.base_url))
  data, response = get_grid_edge_nodes(api, grid)
  copyto!(edge_nodes, data)
  return edge_nodes
end

function BMI.get_grid_face_edges(m::BMIClient, grid, face_edges::Vector{Int})
  api = UnstructuredApi(OpenAPI.Clients.Client(m.base_url))
  data, response = get_grid_face_edges(api, grid)
  copyto!(face_edges, data)
  return face_edges
end

function BMI.get_grid_face_nodes(m::BMIClient, grid, face_nodes::Vector{Int})
  api = UnstructuredApi(OpenAPI.Clients.Client(m.base_url))
  data, response = get_grid_face_nodes(api, grid)
  copyto!(face_nodes, data)
  return face_nodes
end

function BMI.get_grid_nodes_per_face(m::BMIClient, grid, nodes_per_face::Vector{Int})
  api = UnstructuredApi(OpenAPI.Clients.Client(m.base_url))
  data, response = get_grid_nodes_per_face(api, grid)
  copyto!(nodes_per_face, data)
  return nodes_per_face
end

end
