module Client

using HTTP
using JSON
using OpenAPI
import OpenAPI.Clients
include("client/BmiClient.jl")
using .BmiClient

import BasicModelInterface as BMI

Base.@kwdef mutable struct ClientModel
    base_url::String
end

# TODO can we get rid of this? Or rename it?
function setup(base_url::String)
    return ClientModel(base_url)
end

# Model control functions

# in https://github.com/csdms/bmi-example-julia/blob/b5d963e6bf864f5d42769e6cc0814dd7bffc9264/src/bmi.jl#L5
# and https://github.com/Deltares/Wflow.jl/blob/788eaad5848e4e02d5357a7c17df363fcfd7d7b7/src/bmi.jl#L23
# the initialize first argument is a class not an instance
# here we use an instance that has be setup with the base_url
# TODO is this ok? Could move base_url arg here, but will need other args like timeouts.
function BMI.initialize(m::ClientModel, config_file::String)
    # TODO store api instance inside m so we dont recreate it each time
    api = IRFApi(OpenAPI.Clients.Client(m.base_url))
    data, response = initialize(api, InitializeRequest(config_file))
    # TODO check response status code is OK
    return m
end

function BMI.update(m::ClientModel)
    api = IRFApi(OpenAPI.Clients.Client(m.base_url))
    data, response = update(api)
    return nothing
end

function BMI.update_until(m::ClientModel, time::Float64)
    api = IRFApi(OpenAPI.Clients.Client(m.base_url))
    data, response = update_until(api, time)
    return nothing
end

function BMI.finalize(m::ClientModel)
    api = IRFApi(OpenAPI.Clients.Client(m.base_url))
    data, response = finalize(api)
    return nothing
end

# Model information functions

function BMI.get_component_name(m::ClientModel)
    api = ExchangeItemsApi(OpenAPI.Clients.Client(m.base_url))
    data, response = get_component_name(api)
    response.status == 200 || throw(OpenAPI.Clients.APIError(response))
    return data.name
end

function BMI.get_input_var_names(m::ClientModel)
    api = ExchangeItemsApi(OpenAPI.Clients.Client(m.base_url))
    data, response = get_input_var_names(api)
    return data
end

function BMI.get_input_item_count(m::ClientModel)
    api = ExchangeItemsApi(OpenAPI.Clients.Client(m.base_url))
    data, response = get_input_item_count(api)
    return data
end

function BMI.get_output_var_names(m::ClientModel)
    api = ExchangeItemsApi(OpenAPI.Clients.Client(m.base_url))
    data, response = get_output_var_names(api)
    return data
end

function BMI.get_output_item_count(m::ClientModel)
    api = ExchangeItemsApi(OpenAPI.Clients.Client(m.base_url))
    data, response = get_output_item_count(api)
    return data
end

# Variable information functions

function BMI.get_var_grid(m::ClientModel, name)
    api = VariableInformationApi(OpenAPI.Clients.Client(m.base_url))
    data, response = get_var_grid(api, name)
    return data.units
end

function BMI.get_var_type(m::ClientModel, name::String)
    api = VariableInformationApi(OpenAPI.Clients.Client(m.base_url))
    data, response = get_var_type(api, name)
    type_map = Dict(
        "float" => Float32,
        "double" => Float64,
        "int32" => Int32,
        "int64" => Int64
        )
        return type_map[data]
end

function BMI.get_var_units(m::ClientModel, name::String)
    api = VariableInformationApi(OpenAPI.Clients.Client(m.base_url))
    data, response = get_var_units(api, name)
    return data.units
end

function BMI.get_var_itemsize(m::ClientModel, name::String)
    api = VariableInformationApi(OpenAPI.Clients.Client(m.base_url))
    data, response = get_var_itemsize(api, name)
    return data
end

function BMI.get_var_nbytes(m::ClientModel, name::String)
    api = VariableInformationApi(OpenAPI.Clients.Client(m.base_url))
    data, response = get_var_nbytes(api, name)
    return data
end

function BMI.get_var_location(m::ClientModel, name::String)
    api = VariableInformationApi(OpenAPI.Clients.Client(m.base_url))
    data, response = get_var_location(api, name)
    return data.location
end

# Time functions

function BMI.get_current_time(m::ClientModel)
    api = TimeInformationApi(OpenAPI.Clients.Client(m.base_url))
    data, response = get_current_time(api)
    return data
end

function BMI.get_start_time(m::ClientModel)
    api = TimeInformationApi(OpenAPI.Clients.Client(m.base_url))
    data, response = get_start_time(api)
    return data
end

function BMI.get_end_time(m::ClientModel)
    api = TimeInformationApi(OpenAPI.Clients.Client(m.base_url))
    data, response = get_end_time(api)
    return data
end

function BMI.get_time_units(m::ClientModel)
    api = TimeInformationApi(OpenAPI.Clients.Client(m.base_url))
    data, response = get_time_units(api)
    return data
end

function BMI.get_time_step(m::ClientModel)
    api = TimeInformationApi(OpenAPI.Clients.Client(m.base_url))
    data, response = get_time_step(api)
    return data
end

# Variable getter and setter functions

function BMI.get_value(m::ClientModel, name::String, dest::AbstractArray{T}) where {T}
    api = GettersApi(OpenAPI.Clients.Client(m.base_url))
    data, response = get_value(api, name)
    copyto!(dest, data)
    return dest
end

function BMI.get_value_ptr(m::ClientModel, name::String)
    # TODO is this the way? Or should function be absent?
   throw(NotImplementedError())
end

function BMI.get_value_at_indices(m::ClientModel, name::String, dest::AbstractArray{T}, inds::Vector{Int}) where {T}
    api = GettersApi(OpenAPI.Clients.Client(m.base_url))
    data, response = get_value_at_indices(api, name, inds)
    copyto!(dest, data)
    return dest
end

function BMI.set_value(m::ClientModel, name::String, src::AbstractArray{T}) where {T}
    api = SettersApi(OpenAPI.Clients.Client(m.base_url))
    data, response = set_value(api, name, src)
    return nothing
end

function BMI.set_value_at_indices(m::ClientModel, name::String, inds::Vector{Int}, src::AbstractArray{T}) where {T}
    api = SettersApi(OpenAPI.Clients.Client(m.base_url))
    data, response = set_value_at_indices(api, name, inds, src)
    return nothing
end

# Model grid functions

function BMI.get_grid_type(m::ClientModel, grid)
    api = GridInformationApi(OpenAPI.Clients.Client(m.base_url))
    data, response = get_grid_type(api,grid)
    return data.type
end

function BMI.get_grid_rank(m::ClientModel, grid)
    api = GridInformationApi(OpenAPI.Clients.Client(m.base_url))
    data, response = get_grid_rank(api, grid)
    return data
end

function BMI.get_grid_size(m::ClientModel, grid)
    api = GridInformationApi(OpenAPI.Clients.Client(m.base_url))
    data, response = get_grid_size(api, grid)
    return data
end

function BMI.get_grid_shape(m::ClientModel, grid)
    api = UniformRectilinearApi(OpenAPI.Clients.Client(m.base_url))
    data, response = get_grid_shape(api,grid)
    return data
end

function BMI.get_grid_spacing(m::ClientModel, grid, spacing::Vector{T}) where {T<:AbstractFloat}
    api = UniformRectilinearApi(OpenAPI.Clients.Client(m.base_url))
    data, response = get_grid_spacing(api, grid)
    copyto!(spacing, data)
    return spacing
end

function BMI.get_grid_origin(m::ClientModel, grid, origin::Vector{T}) where {T<:AbstractFloat}
    api = UniformRectilinearApi(OpenAPI.Clients.Client(m.base_url))
    data, response = get_grid_origin(api, grid)
    copyto!(origin, data)
    return origin
end

function BMI.get_grid_x(m::ClientModel, grid, x::Vector{T}) where {T<:AbstractFloat}
    api = NURCApi(OpenAPI.Clients.Client(m.base_url))
    data, response = get_grid_x(api, grid)
    copyto!(x, data)
    return x
end

function BMI.get_grid_y(m::ClientModel, grid, y::Vector{T}) where {T<:AbstractFloat}
    api = NURCApi(OpenAPI.Clients.Client(m.base_url))
    data, response = get_grid_y(api, grid)
    copyto!(y, data)
    return y
end

function BMI.get_grid_z(m::ClientModel, grid, z::Vector{T}) where {T<:AbstractFloat}
    api = NURCApi(OpenAPI.Clients.Client(m.base_url))
    data, response = get_grid_z(api, grid)
    copyto!(z, data)
    return z
end

function BMI.get_grid_node_count(m::ClientModel, grid)
    api = UnstructuredApi(OpenAPI.Clients.Client(m.base_url))
    data, response = get_grid_node_count(api, grid)
    return data
end

function BMI.get_grid_edge_count(m::ClientModel, grid)
    api = UnstructuredApi(OpenAPI.Clients.Client(m.base_url))
    data, response = get_grid_edge_count(api, grid)
    return data
end

function BMI.get_grid_face_count(m::ClientModel, grid)
    api = UnstructuredApi(OpenAPI.Clients.Client(m.base_url))
    data, response = get_grid_face_count(api, grid)
    return data
end

function BMI.get_grid_edge_nodes(m::ClientModel, grid, edge_nodes::Vector{Int})
    api = UnstructuredApi(OpenAPI.Clients.Client(m.base_url))
    data, response = get_grid_edge_nodes(api, grid)
    copyto!(edge_nodes, data)
    return edge_nodes
end

function BMI.get_grid_face_edges(m::ClientModel, grid, face_edges::Vector{Int})
    api = UnstructuredApi(OpenAPI.Clients.Client(m.base_url))
    data, response = get_grid_face_edges(api, grid)
    copyto!(face_edges, data)
    return face_edges
end

function BMI.get_grid_face_nodes(m::ClientModel, grid, face_nodes::Vector{Int})
    api = UnstructuredApi(OpenAPI.Clients.Client(m.base_url))
    data, response = get_grid_face_nodes(api, grid)
    copyto!(face_nodes, data)
    return face_nodes
end

function BMI.get_grid_nodes_per_face(m::ClientModel, grid, nodes_per_face::Vector{Int})
    api = UnstructuredApi(OpenAPI.Clients.Client(m.base_url))
    data, response = get_grid_nodes_per_face(api, grid)
    copyto!(nodes_per_face, data)
    return nodes_per_face
end

end